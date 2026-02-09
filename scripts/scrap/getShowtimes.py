"""
Metrograph Letterboxd Scraper

Scrapes film ratings from Letterboxd for Metrograph's current films
and combines the data with event information.
"""

import json
import csv
import re
from urllib.parse import quote_plus

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Local modules
from helpers import is_ci_environment, wait_for_delay
from debug import save_screenshot, save_debug_info
from progress import save_progress, create_save_state
from driver import create_driver, RESTART_EVERY_N_FILMS
from cloudflare import solve_challenge


# Phrases that indicate a non-film entry to skip
SKIP_PHRASES = [
    "ace presents",
    "afternoon cartoon",
    "best of nyc",
    "private event today",
    "preceded by",
    "presents",
    "short film program",
    "shorts program",
    "commissary closed",
    "part 1",
    "part 2",
    "for tots",
    "dcp"
]


def add_events_to_films():
    """
    Merge event data from raw_events.json with parsed film data.
    
    Reads the parsed films CSV and events JSON, matches by title,
    and writes the combined data to the final output CSV.
    """
    print("0️⃣ Adding events to parsed films")

    # Read films from CSV
    with open("./scripts/scrap/data/parsed_films.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        parsed_films = list(reader)

    # Read events from JSON
    with open("./scripts/scrap/data/raw_events.json", "r", encoding="utf-8") as f:
        raw_events = json.load(f)
    
    # Create lookup dict for O(1) matching
    films_by_title = {film["title"]: film for film in parsed_films}
    
    # Add event data to matching films
    for event in raw_events:
        if event["title"] in films_by_title:
            films_by_title[event["title"]]["event_description"] = event["description"]
            films_by_title[event["title"]]["event_time_date"] = event["time_date"]
        
    print("1️⃣ Successfully added events to parsed films")

    # Write final output
    films_with_events = list(films_by_title.values())
    
    fieldnames = [
        "title", "imageUrl", "directors", "synopsis", "year", 
        "rating", "letterboxd_url", "event_description", "event_time_date"
    ]
    
    with open("./src/lib/data/films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for film in films_with_events:
            film.setdefault("event_description", "")
            film.setdefault("event_time_date", "")
            film.setdefault("letterboxd_url", "")
            writer.writerow(film)
    
    print("2️⃣ Finish writing events to file")


def _load_already_processed() -> set:
    """Load titles of films already processed from progress files."""
    already_processed = set()
    
    # Load parsed films
    try:
        with open("./scripts/scrap/data/parsed_films_progress.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            already_processed = {row["title"] for row in reader}
        print(f"📂 Found existing progress: {len(already_processed)} films already processed")
    except FileNotFoundError:
        print("📂 No existing progress found, starting fresh")
    
    # Load skipped films
    try:
        with open("./scripts/scrap/data/skipped_films_progress.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            already_skipped = {row["title"] for row in reader}
            already_processed.update(already_skipped)
        print(f"📂 Found {len(already_skipped)} previously skipped films")
    except FileNotFoundError:
        pass
    
    return already_processed


def _should_skip_film(film: dict, film_title: str) -> tuple[bool, str]:
    """
    Check if a film should be skipped.
    
    Returns:
        Tuple of (should_skip, reason)
    """
    # Missing required data
    if film['directors'] == '' or film['title'] == '' or film['year'] == '':
        return True, "missing film data"
    
    # Bad title or multiple directors
    if any(phrase in film_title.lower() for phrase in SKIP_PHRASES):
        return True, "skip phrase in title"
    
    if 'multiple dirs' in film['directors']:
        return True, "multiple directors"
    
    return False, ""


def _scrape_film_from_letterboxd(driver, film: dict, film_title: str, is_ci: bool) -> bool:
    """
    Scrape a single film's rating from Letterboxd.
    
    Args:
        driver: SeleniumBase driver instance
        film: Film dict to update with rating/url
        film_title: Cleaned film title for search
        is_ci: Whether running in CI (headless) mode
    
    Returns:
        True if successful, False if failed
    """
    print(f"→ Start parsing {film_title}")
    
    # Search for film on Letterboxd
    search_url = "https://letterboxd.com/search/" + quote_plus(f"{film_title} {film['year']}")
    driver.get(search_url)
    
    # Save screenshot for debugging
    save_screenshot(driver, film_title)
    
    wait = WebDriverWait(driver, 20)
    wait_for_delay()
    solve_challenge(driver, is_headless=is_ci)
    
    # Find the first film result
    link_tag = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h2.headline-2 span.film-title-wrapper a")
        )
    )
    
    # Navigate to film page
    film_url = link_tag.get_attribute("href")
    film["letterboxd_url"] = film_url
    print(f"→ Found film url: {film_url}")
    
    print(f"→ Loading film page...")
    driver.get(film_url)
    print(f"→ Film page loaded")
    
    wait_for_delay()
    solve_challenge(driver, is_headless=is_ci)
    
    # Get rating
    print(f"→ Waiting for rating element...")
    rating = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.average-rating > a"))
    )
    print(f"→ Rating element found")
    film["rating"] = rating.text
    
    print(f"→ Successfully parsed {film_title}")
    return True


def parse_letterboxd():
    """
    Main scraping function.
    
    Loads films from raw_films.json, scrapes Letterboxd for ratings,
    and saves progress incrementally.
    """
    # Load input data
    with open("./scripts/scrap/data/raw_films.json", "r", encoding="utf-8") as f:
        parsed_films = json.load(f)

    # Check for existing progress
    already_processed = _load_already_processed()
    
    # Filter to unprocessed films
    films_to_process = [
        film for film in parsed_films 
        if film["title"] not in already_processed
    ]
    
    print(f"📊 Total: {len(parsed_films)}, Done: {len(already_processed)}, Remaining: {len(films_to_process)}")
    
    if not films_to_process:
        print("✅ All films already processed!")
        return

    # Set up browser
    is_ci = is_ci_environment()
    print(f"🖥️  Running in {'CI/headless' if is_ci else 'local/visible'} mode")
    
    driver = create_driver(is_ci)
    films_since_restart = 0
    
    # Track results
    done_films = []
    skipped_films = []
    save_state = create_save_state(len(already_processed))

    print(f"4️⃣ Start parsing film info: {len(films_to_process)} films remaining")

    # Process each film
    for idx, film in enumerate(films_to_process, 1):
        film_title = re.sub(r"[^\w\s]", "", film["title"])
        
        # Check if should skip
        should_skip, reason = _should_skip_film(film, film_title)
        if should_skip:
            skipped_films.append(film)
            print(f"→ Purposefully skipped {film_title} - {reason}")
        else:
            # Attempt to scrape
            try:
                _scrape_film_from_letterboxd(driver, film, film_title, is_ci)
                done_films.append(film)
                
            except TimeoutException:
                save_debug_info(driver, film_title)
                skipped_films.append(film)
                print(f"→ Skipped {film_title} (timeout)")
                
            except WebDriverException:
                save_debug_info(driver, film_title)
                skipped_films.append(film)
                print(f"→ Skipped {film_title} (webdriver error)")
                
            except Exception as e:
                save_debug_info(driver, film_title)
                skipped_films.append(film)
                print(f"→ Skipped {film_title} (error: {type(e).__name__})")
        
        # Rate limiting delay
        wait_for_delay(10, 30)
        
        # Periodic saves
        if idx % 10 == 0:
            save_progress(done_films, skipped_films, save_state)
        
        # Restart browser periodically to prevent memory issues
        films_since_restart += 1
        if films_since_restart >= RESTART_EVERY_N_FILMS and idx < len(films_to_process):
            print(f"🔄 Restarting browser after {films_since_restart} films...")
            save_progress(done_films, skipped_films, save_state)
            
            try:
                driver.quit()
            except Exception as e:
                print(f"⚠️  Error quitting driver: {e}")
            
            driver = create_driver(is_ci)
            films_since_restart = 0
            print("✅ Browser restarted successfully")

    # Cleanup
    driver.quit()
    print("4️⃣ Finish parsing film info")

    # Final save
    save_progress(done_films, skipped_films, save_state)
    print(f"5️⃣ Final save complete - {len(done_films)} films parsed")


# Run main functions
parse_letterboxd()
add_events_to_films()
