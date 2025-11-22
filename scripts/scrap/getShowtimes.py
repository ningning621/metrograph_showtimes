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

def get_metrograph_events(isLocal: bool):
    print("0️⃣ Opening metrograph events page")

    if isLocal:
        # pull raw html from local file
        with open("./scripts/scrap/data/metrograph_events.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        # pull raw html 
        response = requests.get("https://metrograph.com/events/")
        with open("./scripts/scrap/data/metrograph_events.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
    print("1️⃣ Successfully pulled metrograph events html")

    soup_response = response if isLocal else response.text
    soup = BeautifulSoup(soup_response, "html.parser")
    events = soup.find_all("div", class_="homepage-in-theater-movie")

    parsed_events = []

    print("2️⃣ Start parsing events html")

    # parse raw information into list of events
    for event in events:
        # Extract title
        title_tag = event.find("h4")
        if title_tag:
            title_link = title_tag.find("a", class_="title")
            title = title_link.get_text(strip=True) if title_link else ""
        else:
            title = ""

        # Extract director from metadata (format: "Director Name / Year / Duration / Format")
        metadata_tag = event.find("div", class_="film-metadata")
        directors = ""
        if metadata_tag:
            metadata_text = metadata_tag.get_text(strip=True)
            # Split by "/" and take the first part as director
            parts = metadata_text.split("/")
            if parts:
                directors = parts[0].strip()

        # Extract description
        description_tag = event.find("div", class_="film-description")
        description = description_tag.get_text(strip=True) if description_tag else ""

        # Extract time and date
        showtimes_tag = event.find("div", class_="showtimes")
        time_date = ""
        if showtimes_tag:
            showtime_link = showtimes_tag.find("a")
            if showtime_link:
                time_date = showtime_link.get_text(strip=True)

        parsed_events.append({
            "title": title,
            "directors": directors,
            "description": description,
            "time_date": time_date
        })

        print(f"→ Parsed event: {title}")

    print(f"2️⃣ Finish parsing events html - Found {len(parsed_events)} events")

    # Write events to file
    with open("./scripts/scrap/data/raw_events.json", "w", encoding="utf-8") as f:
        json.dump(parsed_events, f, ensure_ascii=False, indent=2)
    
    print("3️⃣ Finish writing events to file")

    return parsed_events

def add_events_to_films():
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
    
    print("3️⃣ Finish writing events to file")

def get_metrograph_films(isLocal: bool):
    print("0️⃣ Starting film scraping work")

    if isLocal:
        # pull raw html from local file
        with open("./scripts/scrap/data/metrograph.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        # pull raw html 
        response = requests.get("https://metrograph.com/film/")
        with open("./scripts/scrap/data/metrograph.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
    print("1️⃣ Successfully pulled metrograph films html")

    soup_response = response if isLocal else response.text
    soup = BeautifulSoup(soup_response, "html.parser")
    films = soup.find_all("div", class_="homepage-in-theater-movie")

    parsed_films = []

    print("2️⃣ Start parsing html")

    # parse raw information into list of films
    for film in films:
        # print(film)
        title = film.find("h3", class_="movie_title").get_text(strip=True)

        raw_director = film.find("h5", string=lambda t: t and "Director" in t)

        pattern = re.compile(r'^\s*(\d{3,4})\s*/\s*(\d+)\s*min(?:\s*/.*)?$', re.IGNORECASE)
        raw_year_duration = film.find(
            "h5",
            string=lambda t: isinstance(t, str) and pattern.match(t.strip())
        )
        year = int(raw_year_duration.get_text(strip=True).split("/")[0].strip()) if raw_year_duration else 0

        if raw_director:
            director_text = raw_director.get_text(strip=True).replace("Director:", "").strip()
            directors = [name.strip() for name in director_text.split(",")]

        # TODO switch synopsis with MORE... text and track Q&As
        synopsis = film.find("p", class_="synopsis").get_text(strip=True)
        imageUrl = film.find("img").attrs["src"]

        parsed_films.append({"title": title, "imageUrl": imageUrl, "directors": directors, "synopsis": synopsis, "year": year })
    
    print("2️⃣ Finish parsing html")

    # add metrograph html to file for local storage 
    with open("./scripts/scrap/data/raw_films.json", "w", encoding="utf-8") as f:
        json.dump(parsed_films, f, ensure_ascii=False, indent=2)
    
    print("3️⃣ Finish writing html to file")

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

    skipped_films = []
    done_films = []

    skip_phrases = [
        "ace presents",
        "afternoon cartoon",
        "best of nyc",
        "private event today",
        "preceded by",
        "presents:",
        "short film program",
    ]

    print(f"4️⃣ Start parsing film info: {len(parsed_films)} films")

    for film in parsed_films:
        # print(film)
        film_title = re.sub(r"[^\w\s]", "", film["title"]) 

        if (any(p in film_title.lower() for p in skip_phrases) or 'multiple dirs' in film['directors']):
            skipped_films.append(film)
            print(f"→ Purposefully skipped {film_title}")
        else: 
            try:
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

    driver.quit()
    print(f"4️⃣ Finish parsing film info")

    with open("./scripts/scrap/data/parsed_films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "synopsis", "year", "rating", "letterboxd_url"])
        writer.writeheader()
        writer.writerows(done_films)

    with open("./scripts/scrap/data/skipped_films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "year", "synopsis",])
        writer.writeheader()
        writer.writerows(skipped_films)
    
    print(f"5️⃣ Wrote data to files")

get_metrograph_films(False)
parse_letterboxd()
get_metrograph_events(False)
add_events_to_films()