"""
Progress tracking for incremental film scraping.

Handles saving progress to CSV files so scraping can resume
after interruptions without losing work.
"""

import csv
from typing import List, Dict, Any


# CSV field definitions
PARSED_FILMS_FIELDS = [
    "title", "imageUrl", "directors", "synopsis", 
    "year", "rating", "letterboxd_url"
]

SKIPPED_FILMS_FIELDS = [
    "title", "imageUrl", "directors", "year", 
    "synopsis", "letterboxd_url"
]

# File paths
PARSED_PROGRESS_FILE = "./scripts/scrap/data/parsed_films_progress.csv"
PARSED_FINAL_FILE = "./scripts/scrap/data/parsed_films.csv"
SKIPPED_PROGRESS_FILE = "./scripts/scrap/data/skipped_films_progress.csv"
SKIPPED_FINAL_FILE = "./scripts/scrap/data/skipped_films.csv"


def create_save_state(already_processed_count: int = 0) -> Dict[str, Any]:
    """
    Create initial save state for tracking progress.
    
    Args:
        already_processed_count: Number of films already processed (for resume)
    
    Returns:
        State dict to pass to save_progress()
    """
    return {
        'first_save': already_processed_count == 0,
        'last_saved_done_count': 0,
        'last_saved_skipped_count': 0
    }


def save_progress(
    done_films: List[Dict], 
    skipped_films: List[Dict], 
    state: Dict[str, Any]
) -> None:
    """
    Save scraping progress to CSV files.
    
    Writes incrementally - only new films since last save are appended.
    Saves to both progress files (for resume) and final files.
    
    Args:
        done_films: List of successfully parsed film dicts
        skipped_films: List of skipped film dicts
        state: Progress state dict (modified in place)
    """
    # Determine write mode
    if state['first_save']:
        mode = "w"
        write_header = True
        state['first_save'] = False
    else:
        mode = "a"
        write_header = False
    
    # Save parsed films
    new_done = done_films[state['last_saved_done_count']:]
    if new_done or mode == "w":
        _write_films_csv(
            filenames=[PARSED_PROGRESS_FILE, PARSED_FINAL_FILE],
            films=new_done,
            fieldnames=PARSED_FILMS_FIELDS,
            mode=mode,
            write_header=write_header
        )
    
    # Save skipped films
    new_skipped = skipped_films[state['last_saved_skipped_count']:]
    if new_skipped or mode == "w":
        _write_films_csv(
            filenames=[SKIPPED_PROGRESS_FILE, SKIPPED_FINAL_FILE],
            films=new_skipped,
            fieldnames=SKIPPED_FILMS_FIELDS,
            mode=mode,
            write_header=write_header
        )
    
    # Update state
    state['last_saved_done_count'] = len(done_films)
    state['last_saved_skipped_count'] = len(skipped_films)
    
    print(f"💾 Progress saved: {len(done_films)} done, {len(skipped_films)} skipped")


def _write_films_csv(
    filenames: List[str],
    films: List[Dict],
    fieldnames: List[str],
    mode: str,
    write_header: bool
) -> None:
    """
    Write films to multiple CSV files.
    
    Args:
        filenames: List of file paths to write to
        films: List of film dicts to write
        fieldnames: CSV column names
        mode: File mode ('w' or 'a')
        write_header: Whether to write the header row
    """
    for filename in filenames:
        with open(filename, mode, newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=fieldnames, 
                extrasaction='ignore'
            )
            if write_header:
                writer.writeheader()
            writer.writerows(films)
