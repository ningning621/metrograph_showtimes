import requests
from bs4 import BeautifulSoup
import json
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus

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

def parse_letterboxd():
    with open("./scripts/scrap/data/raw_films.json", "r", encoding="utf-8") as f:
        parsed_films = json.load(f)

    # set up selenium
    options = Options()

    # note: comment this out on local
    options.add_argument("--headless=new")   

    options.add_argument("--no-sandbox")             
    options.add_argument("--disable-dev-shm-usage")   
    options.add_argument("--blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(60) # 60 seconds timeout

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

    print(f"4️⃣ Start parsing film info: {len(parsed_films)} films")

    # Track if this is the first save
    first_save = True
    last_saved_done_count = 0
    last_saved_skipped_count = 0

    # Helper function to save progress
    def save_progress():
        nonlocal first_save, last_saved_done_count, last_saved_skipped_count
        
        if first_save:
            # First save: overwrite and write header
            mode = "w"
            write_header = True
            first_save = False
        else:
            # Subsequent saves: append only new films
            mode = "a"
            write_header = False
        
        # Write only new done films
        new_done_films = done_films[last_saved_done_count:]
        if new_done_films or mode == "w":
            with open("./scripts/scrap/data/parsed_films.csv", mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "synopsis", "year", "rating", "letterboxd_url"])
                if write_header:
                    writer.writeheader()
                writer.writerows(new_done_films)
        
        # Write only new skipped films
        new_skipped_films = skipped_films[last_saved_skipped_count:]
        if new_skipped_films or mode == "w":
            with open("./scripts/scrap/data/skipped_films.csv", mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "year", "synopsis", "letterboxd_url"], extrasaction='ignore')
                if write_header:
                    writer.writeheader()
                writer.writerows(new_skipped_films)
        
        last_saved_done_count = len(done_films)
        last_saved_skipped_count = len(skipped_films)
        
        print(f"💾 Progress saved: {len(done_films)} done, {len(skipped_films)} skipped")

    # for each film, pull its letterboxd info and add to the film object
    for idx, film in enumerate(parsed_films, 1):
        # print(film)
        film_title = re.sub(r"[^\w\s]", "", film["title"]) 

        # check if the film needs to be skipped bc bad title or multiple directors or other reasons
        if (any(p in film_title.lower() for p in skip_phrases) or 'multiple dirs' in film['directors']):
            skipped_films.append(film)
            print(f"→ Purposefully skipped {film_title}")
        else: 
            try:
                print(f"→ Start parsing {film_title}")
                # pull data from letterboxd
                driver.get("https://letterboxd.com/search/" + quote_plus(f"{film_title} {film['year']}")) 

                wait = WebDriverWait(driver, 5)
                
                link_tag = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h2.headline-2 span.film-title-wrapper a")
                    )
                )

                # Extract the film page URL
                film_url = link_tag.get_attribute("href")
                film["letterboxd_url"] = film_url

                driver.get(film_url)

                rating = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.average-rating > a"))
                )
                film["rating"] = rating.text

                driver.implicitly_wait(5)
                done_films.append(film)

                print(f"→ Successfully parsed {film_title}")
            except Exception as e:
                # print(e)
                skipped_films.append(film)
                print(f"→ Skipped {film_title}")
        
        # Save progress every 10 films
        if idx % 10 == 0:
            save_progress()

    driver.quit()
    print(f"4️⃣ Finish parsing film info")

    # Final save
    save_progress()
    print(f"5️⃣ Final save complete - {len(done_films)} films parsed")

parse_letterboxd()
add_events_to_films()