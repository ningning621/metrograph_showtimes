import requests
from bs4 import BeautifulSoup
import json
import csv
import re

def get_metrograph_films(isLocal: bool):
    

    if isLocal:
        print("0️⃣ Pulling films from local file")
        # pull raw html from local file
        with open("./scripts/scrap/data/metrograph.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        print("0️⃣ Pulling films from Metrograph website, films page")

        # pull raw html with cache-busting headers
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get("https://metrograph.com/film/", headers=headers)
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

def get_metrograph_events(isLocal: bool):
    
    if isLocal:
        print("0️⃣ Opening local metrograph events html file")
        # pull raw html from local file
        with open("./scripts/scrap/data/metrograph_events.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        print("0️⃣ Pulling from Metrograph website, events page")

        # pull raw html with cache-busting headers
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get("https://metrograph.com/events/", headers=headers)
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

get_metrograph_films(False)
get_metrograph_events(False)