from bs4 import BeautifulSoup
import json
import csv
import re
import time
import random
import os
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.parse import quote_plus

def solve_challenge(driver, timeout=30):
    """
    Handle Cloudflare Turnstile challenge by clicking the checkbox if present.
    
    Args:
        driver: Selenium WebDriver instance
        timeout: How long to wait for page to be ready (default 30 seconds)
    """
    try:
        print(f"⏳ Checking for Cloudflare challenge...")
        
        # First check if we're already on the actual page (no challenge)
        try:
            element = driver.find_element(By.CSS_SELECTOR, "h2.headline-2, body.not-found")
            print(f"✅ No challenge detected, page already loaded")
            return
        except:
            pass
        
        # Check if there's a Turnstile challenge on the page
        page_source = driver.page_source.lower()
        if "verify you are human" not in page_source and "turnstile" not in page_source:
            print(f"ℹ️  No Turnstile challenge detected in page source, waiting for content...")
            WebDriverWait(driver, timeout=timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.headline-2, body.not-found"))
            )
            print(f"✅ Page loaded")
            return
        
        print(f"🔄 Turnstile challenge detected, attempting to solve...")
        
        # Method 1: Try SeleniumBase's built-in method
        try:
            driver.uc_gui_click_captcha()
            print(f"✅ uc_gui_click_captcha succeeded")
        except Exception as e:
            print(f"⚠️  uc_gui_click_captcha failed: {e}")
            
            # Method 2: Try to click using uc_click on the iframe
            try:
                print(f"🔄 Trying uc_click on Turnstile iframe...")
                driver.uc_click("iframe[src*='turnstile'], iframe[src*='challenge']", timeout=5)
                print(f"✅ uc_click on iframe succeeded")
            except Exception as e2:
                print(f"⚠️  uc_click failed: {e2}")
                
                # Method 3: Manual iframe interaction
                try:
                    print(f"🔄 Trying manual iframe click...")
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    for iframe in iframes:
                        src = iframe.get_attribute("src") or ""
                        if "turnstile" in src.lower() or "challenge" in src.lower():
                            driver.switch_to.frame(iframe)
                            time.sleep(1)
                            checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox'], .checkbox, body")
                            driver.execute_script("arguments[0].click();", checkbox)
                            driver.switch_to.default_content()
                            print(f"✅ Manual iframe click succeeded")
                            break
                except Exception as e3:
                    print(f"⚠️  Manual iframe click failed: {e3}")
                    driver.switch_to.default_content()
        
        # Wait for the challenge to complete and page to load
        print(f"⏳ Waiting for page to load after challenge attempt...")
        WebDriverWait(driver, timeout=timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.headline-2, body.not-found"))
        )
        print(f"✅ Challenge resolved, page loaded")
    except TimeoutException:
        print(f"⚠️  Challenge did not resolve within {timeout} seconds")
    except Exception as e:
        print(f"⚠️  Error waiting for challenge: {e}")

def wait_for_delay(start_time=0, end_time=15):
    delay = random.uniform(start_time, end_time) # add a random delay to avoid rate limiting
    print(f"⏱️  Waiting {delay:.1f} seconds before next film...")
    time.sleep(delay)

def add_events_to_films():
    print("0️⃣ Adding events to parsed films")

    # Read films from CSV and convert to list
    with open("./scripts/scrap/data/parsed_films.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        parsed_films = list(reader)  # Convert iterator to list

    # Read events from JSON
    with open("./scripts/scrap/data/raw_events.json", "r", encoding="utf-8") as f:
        raw_events = json.load(f)
    
    # Create a dictionary indexed by title for O(1) lookups
    films_by_title = {film["title"]: film for film in parsed_films}
    
    # Add event description and time_date to matching films
    for event in raw_events:
        if event["title"] in films_by_title:
            # Add event description and time as separate fields
            films_by_title[event["title"]]["event_description"] = event["description"]
            films_by_title[event["title"]]["event_time_date"] = event["time_date"]
        
    print("1️⃣ Successfully added events to parsed films")

    # Convert films_by_title back to list for output
    films_with_events = list(films_by_title.values())
    
    # Write to CSV with event fields as separate columns
    with open("./src/lib/data/films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "synopsis", "year", "rating", "letterboxd_url", "event_description", "event_time_date"])
        writer.writeheader()
        
        for film in films_with_events:
            # Ensure event fields exist (empty string if no event)
            film.setdefault("event_description", "")
            film.setdefault("event_time_date", "")
            film.setdefault("letterboxd_url", "")
            writer.writerow(film)
    
    print("2️⃣ Finish writing events to file")

def save_screenshot(driver, film_title, prefix=""):
    """
    Save a screenshot of the current page.
    
    Args:
        driver: Selenium WebDriver instance
        film_title: Title of the film for the filename
        prefix: Optional prefix for the filename (e.g., "ERROR_")
    """
    try:
        screenshot_dir = "./scripts/scrap/data/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in film_title)
        screenshot_path = f"{screenshot_dir}/{prefix}{safe_filename[:50]}.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"⚠️  Could not save screenshot: {e}")

def save_page_html(driver, film_title, prefix=""):
    """
    Save the HTML source of the current page.
    
    Args:
        driver: Selenium WebDriver instance
        film_title: Title of the film for the filename
        prefix: Optional prefix for the filename (e.g., "ERROR_")
    """
    try:
        html_dir = "./scripts/scrap/data/page_html"
        os.makedirs(html_dir, exist_ok=True)
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in film_title)
        html_path = f"{html_dir}/{prefix}{safe_filename[:50]}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"📄 Page HTML saved: {html_path}")
    except Exception as e:
        print(f"⚠️  Could not save page HTML: {e}")

def save_progress(done_films, skipped_films, state):
    """Save progress to CSV files.
    
    Args:
        done_films: List of successfully parsed films
        skipped_films: List of skipped films
        state: Dict with 'first_save', 'last_saved_done_count', 'last_saved_skipped_count'
    """
    if state['first_save']:
        # First save: overwrite and write header
        mode = "w"
        write_header = True
        state['first_save'] = False
    else:
        # Subsequent saves: append only new films
        mode = "a"
        write_header = False
    
    # Write only new done films to BOTH progress and final files
    new_done_films = done_films[state['last_saved_done_count']:]
    if new_done_films or mode == "w":
        for filename in ["./scripts/scrap/data/parsed_films_progress.csv", "./scripts/scrap/data/parsed_films.csv"]:
            with open(filename, mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "synopsis", "year", "rating", "letterboxd_url"])
                if write_header:
                    writer.writeheader()
                writer.writerows(new_done_films)
    
    # Write only new skipped films to BOTH progress and final files
    new_skipped_films = skipped_films[state['last_saved_skipped_count']:]
    if new_skipped_films or mode == "w":
        for filename in ["./scripts/scrap/data/skipped_films_progress.csv", "./scripts/scrap/data/skipped_films.csv"]:
            with open(filename, mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "year", "synopsis", "letterboxd_url"], extrasaction='ignore')
                if write_header:
                    writer.writeheader()
                writer.writerows(new_skipped_films)
    
    state['last_saved_done_count'] = len(done_films)
    state['last_saved_skipped_count'] = len(skipped_films)
    
    print(f"💾 Progress saved: {len(done_films)} done, {len(skipped_films)} skipped")

def create_driver(is_ci=None):
    """Create a new SeleniumBase driver instance.
    
    Args:
        is_ci: Whether running in CI environment. If None, auto-detects.
    """
    if is_ci is None:
        is_ci = os.environ.get('CI', 'false').lower() == 'true' or os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'
    
    print(f"🚀 Starting new browser instance...")
    new_driver = Driver(
        browser="chrome",
        uc=True,  # Undetected Chrome mode
        headless2=is_ci,  # Headless on CI, visible locally for debugging
        incognito=True,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        do_not_track=True,
        undetectable=True
    )
    new_driver.set_page_load_timeout(120)  # 120 second timeout for page loads
    return new_driver

def parse_letterboxd():
    with open("./scripts/scrap/data/raw_films.json", "r", encoding="utf-8") as f:
        parsed_films = json.load(f)

    # Use separate progress tracking files that won't interfere with final output
    # These files track progress during the current run only
    already_processed = set()
    try:
        with open("./scripts/scrap/data/parsed_films_progress.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            already_processed = {row["title"] for row in reader}
        print(f"📂 Found existing progress: {len(already_processed)} films already processed")
    except FileNotFoundError:
        print(f"📂 No existing progress found, starting fresh")
    
    try:
        with open("./scripts/scrap/data/skipped_films_progress.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            already_skipped = {row["title"] for row in reader}
            already_processed.update(already_skipped)
        print(f"📂 Found {len(already_skipped)} previously skipped films")
    except FileNotFoundError:
        pass
    
    # Filter out already processed films
    films_to_process = [film for film in parsed_films if film["title"] not in already_processed]
    print(f"📊 Total films: {len(parsed_films)}, Already done: {len(already_processed)}, To process: {len(films_to_process)}")
    
    if len(films_to_process) == 0:
        print("✅ All films already processed!")
        return

    # Use headless mode on GitHub Actions (CI environment), visible browser locally
    is_ci = os.environ.get('CI', 'false').lower() == 'true' or os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'
    print(f"🖥️  Running in {'CI/headless' if is_ci else 'local/visible'} mode")
    
    driver = create_driver(is_ci)
    films_since_restart = 0
    RESTART_EVERY = 50  # Restart browser every 50 films to prevent memory issues

    skipped_films = []
    done_films = []

    skip_phrases = [
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

    print(f"4️⃣ Start parsing film info: {len(films_to_process)} films remaining")

    # Track save state (using dict so it can be modified by save_progress function)
    save_state = {
        'first_save': len(already_processed) == 0,
        'last_saved_done_count': 0,
        'last_saved_skipped_count': 0
    }

    # for each film, pull its letterboxd info and add to the film object
    for idx, film in enumerate(films_to_process, 1):
        # print(film)
        film_title = re.sub(r"[^\w\s]", "", film["title"]) 

        # if director or title or year is empty, skip
        if (film['directors'] == '' or film['title'] == '' or film['year'] == ''):
            skipped_films.append(film)
            print(f"→ Purposefully skipped {film_title} - missing film data")
        # check if the film needs to be skipped bc bad title or multiple directors or other reasons
        elif (any(p in film_title.lower() for p in skip_phrases) or 'multiple dirs' in film['directors']):
            skipped_films.append(film)
            print(f"→ Purposefully skipped {film_title}")
        else: 
            try:
                print(f"→ Start parsing {film_title}")
                # pull data from letterboxd
                driver.get("https://letterboxd.com/search/" + quote_plus(f"{film_title} {film['year']}")) 

                # Save screenshot for debugging
                save_screenshot(driver, film_title)

                wait = WebDriverWait(driver, 20)  # 20 seconds to wait for elements to load
                
                wait_for_delay()

                solve_challenge(driver)

                link_tag = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h2.headline-2 span.film-title-wrapper a")
                    )
                )

                # Extract the film page URL
                film_url = link_tag.get_attribute("href")
                film["letterboxd_url"] = film_url
                print(f"→ Found film url: {film_url}")
                
                print(f"→ Loading film page...")
                driver.get(film_url)
                print(f"→ Film page loaded")

                wait_for_delay()
                solve_challenge(driver)

                print(f"→ Waiting for rating element...")
                rating = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.average-rating > a"))
                )
                print(f"→ Rating element found")
                film["rating"] = rating.text

                done_films.append(film)

                print(f"→ Successfully parsed {film_title}")
            except TimeoutException as e:
                save_screenshot(driver, film_title, prefix="ERROR_")
                save_page_html(driver, film_title, prefix="ERROR_")
                skipped_films.append(film)
                print(f"→ Skipped {film_title} (timeout - page took too long to load)")
            except WebDriverException as e:
                save_screenshot(driver, film_title, prefix="ERROR_")
                save_page_html(driver, film_title, prefix="ERROR_")
                skipped_films.append(film)
                print(f"→ Skipped {film_title} (webdriver error)")
            except Exception as e:
                save_screenshot(driver, film_title, prefix="ERROR_")
                save_page_html(driver, film_title, prefix="ERROR_")
                skipped_films.append(film)
                print(f"→ Skipped {film_title} (error: {type(e).__name__})")
        
        # Add random delay between requests to avoid rate limiting
        wait_for_delay(10,30)
        
        # Save progress every 10 films
        if idx % 10 == 0:
            save_progress(done_films, skipped_films, save_state)
        
        # Restart browser every RESTART_EVERY films to prevent memory issues
        films_since_restart += 1
        if films_since_restart >= RESTART_EVERY and idx < len(films_to_process):
            print(f"🔄 Restarting browser after {films_since_restart} films to free memory...")
            save_progress(done_films, skipped_films, save_state)  # Save before restart
            try:
                driver.quit()
            except Exception as e:
                print(f"⚠️  Error quitting driver: {e}")
            driver = create_driver(is_ci)
            films_since_restart = 0
            print(f"✅ Browser restarted successfully")

    driver.quit()
    print(f"4️⃣ Finish parsing film info")

    # Final save
    save_progress(done_films, skipped_films, save_state)
    print(f"5️⃣ Final save complete - {len(done_films)} films parsed")

parse_letterboxd()
add_events_to_films()