"""
Debug utilities for saving screenshots and HTML during scraping.

These functions help diagnose issues by capturing the browser state
when errors occur or at key checkpoints.
"""

import os
from helpers import sanitize_filename


# Default directories for debug output
SCREENSHOT_DIR = "./scripts/scrap/data/screenshots"
HTML_DIR = "./scripts/scrap/data/page_html"


def save_screenshot(driver, film_title: str, prefix: str = "") -> bool:
    """
    Save a screenshot of the current browser state.
    
    Args:
        driver: Selenium/SeleniumBase WebDriver instance
        film_title: Title used for the filename
        prefix: Optional prefix (e.g., "ERROR_" for failed attempts)
    
    Returns:
        True if screenshot was saved successfully, False otherwise
    """
    try:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        filename = f"{prefix}{sanitize_filename(film_title)}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        driver.save_screenshot(filepath)
        print(f"📸 Screenshot saved: {filepath}")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not save screenshot: {e}")
        return False


def save_page_html(driver, film_title: str, prefix: str = "") -> bool:
    """
    Save the HTML source of the current page.
    
    Useful for debugging when the page structure is unexpected
    or when Cloudflare challenges appear.
    
    Args:
        driver: Selenium/SeleniumBase WebDriver instance
        film_title: Title used for the filename
        prefix: Optional prefix (e.g., "ERROR_" for failed attempts)
    
    Returns:
        True if HTML was saved successfully, False otherwise
    """
    try:
        os.makedirs(HTML_DIR, exist_ok=True)
        filename = f"{prefix}{sanitize_filename(film_title)}.html"
        filepath = os.path.join(HTML_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        print(f"📄 Page HTML saved: {filepath}")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not save page HTML: {e}")
        return False


def save_debug_info(driver, film_title: str, prefix: str = "ERROR_") -> None:
    """
    Convenience function to save both screenshot and HTML.
    
    Typically called when an error occurs during scraping.
    
    Args:
        driver: Selenium/SeleniumBase WebDriver instance
        film_title: Title used for filenames
        prefix: Prefix for filenames (default: "ERROR_")
    """
    save_screenshot(driver, film_title, prefix)
    save_page_html(driver, film_title, prefix)
