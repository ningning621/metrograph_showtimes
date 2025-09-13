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

def get_metrograph_films(isLocal: bool):
    if isLocal:
        # pull raw html from local file
        with open("./scripts/scrap/data/metrograph.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        # pull raw html 
        response = requests.get("https://metrograph.com/nyc/")
        with open("./scripts/scrap/data/metrograph.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
    soup_response = response if isLocal else response.text
    soup = BeautifulSoup(soup_response, "html.parser")
    films = soup.find_all("div", class_="homepage-in-theater-movie")

    parsed_films = []

    # parse raw information into list of films
    for film in films[:5]:
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

    # add metrograph html to file for local storage 
    with open("./scripts/scrap/data/raw_films.json", "w", encoding="utf-8") as f:
        json.dump(parsed_films, f, ensure_ascii=False, indent=2)

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

    for film in parsed_films:
        # print(film)
        film_title = re.sub(r"[^\w\s]", "", film["title"]) 

        if (any(p in film_title.lower() for p in skip_phrases) or 'multiple dirs' in film['directors']):
            skipped_films.append(film)
        else: 
            try:
                driver.get("https://letterboxd.com/search/" + quote_plus(f"{film_title} {film['year']}")) 

                wait = WebDriverWait(driver, 10)
                
                link_tag = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h2.headline-2 span.film-title-wrapper a")
                    )
                )

                # Extract the film page URL
                film_url = link_tag.get_attribute("href")

                driver.get(film_url)

                rating = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.average-rating > a"))
                )
                film["rating"] = rating.text

                driver.implicitly_wait(5)
                done_films.append(film)
            except Exception as e:
                # print(e)
                skipped_films.append(film)

    driver.quit()

    with open("./scripts/scrap/data/parsed_films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "synopsis", "year", "rating"])
        writer.writeheader()
        writer.writerows(done_films)

    with open("./scripts/scrap/data/skipped_films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "imageUrl", "directors", "year", "synopsis",])
        writer.writeheader()
        writer.writerows(skipped_films)
    
get_metrograph_films(False)
parse_letterboxd()
