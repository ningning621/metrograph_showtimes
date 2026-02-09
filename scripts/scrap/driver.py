"""
Browser driver management for SeleniumBase.

Handles creating and configuring Chrome browser instances
with undetected mode for bypassing bot detection.
"""

from seleniumbase import Driver
from helpers import is_ci_environment


# Browser configuration
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

PAGE_LOAD_TIMEOUT = 120  # seconds
RESTART_EVERY_N_FILMS = 50  # Restart browser periodically to prevent memory issues


def create_driver(is_ci: bool = None):
    """
    Create a new SeleniumBase driver instance configured for scraping.
    
    Uses undetected Chrome mode to bypass bot detection. Automatically
    switches to headless mode when running in CI environments.
    
    Args:
        is_ci: Force CI mode (headless). If None, auto-detects environment.
    
    Returns:
        Configured SeleniumBase Driver instance
    """
    if is_ci is None:
        is_ci = is_ci_environment()
    
    print(f"🚀 Starting new browser instance ({'headless' if is_ci else 'visible'})...")
    
    driver = Driver(
        browser="chrome",
        uc=True,              # Undetected Chrome mode
        headless2=is_ci,      # Headless in CI, visible locally
        incognito=True,
        agent=USER_AGENT,
        do_not_track=True,
        undetectable=True
    )
    
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    return driver
