"""
Cloudflare Turnstile challenge solver for Letterboxd scraping.

This module provides utilities to detect and bypass Cloudflare's Turnstile
challenge when scraping Letterboxd pages using SeleniumBase.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# CSS selectors for detecting successful page load
CONTENT_LOADED_SELECTOR = "h2.headline-2, body.not-found"

# Turnstile iframe selectors
TURNSTILE_IFRAME_SELECTOR = "iframe[src*='turnstile'], iframe[src*='challenge']"

# Keywords that indicate a Turnstile challenge is present
CHALLENGE_KEYWORDS = ["verify you are human", "turnstile"]


def _is_page_loaded(driver) -> bool:
    """Check if the actual content page is already loaded (no challenge)."""
    try:
        driver.find_element(By.CSS_SELECTOR, CONTENT_LOADED_SELECTOR)
        return True
    except:
        return False


def _has_turnstile_challenge(driver) -> bool:
    """Check if the page contains a Turnstile challenge."""
    page_source = driver.page_source.lower()
    return any(keyword in page_source for keyword in CHALLENGE_KEYWORDS)


def _wait_for_content(driver, timeout: int) -> bool:
    """Wait for the content page to load. Returns True if successful."""
    try:
        WebDriverWait(driver, timeout=timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CONTENT_LOADED_SELECTOR))
        )
        return True
    except TimeoutException:
        return False


def _try_gui_click(driver) -> bool:
    """
    Try SeleniumBase's built-in GUI captcha clicker.
    Only works with a display (not headless).
    """
    try:
        driver.uc_gui_click_captcha()
        print("  ✓ uc_gui_click_captcha succeeded")
        return True
    except Exception as e:
        print(f"  ✗ uc_gui_click_captcha failed: {e}")
        return False


def _try_uc_click(driver) -> bool:
    """Try SeleniumBase's undetected click on the Turnstile iframe."""
    try:
        driver.uc_click(TURNSTILE_IFRAME_SELECTOR, timeout=5)
        print("  ✓ uc_click on iframe succeeded")
        return True
    except Exception as e:
        print(f"  ✗ uc_click failed: {e}")
        return False


def _try_manual_iframe_click(driver) -> bool:
    """
    Manually find and click the checkbox inside the Turnstile iframe.
    This is the most invasive method and may not always work.
    """
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            src = (iframe.get_attribute("src") or "").lower()
            if "turnstile" not in src and "challenge" not in src:
                continue
            
            driver.switch_to.frame(iframe)
            time.sleep(1)
            
            checkbox = driver.find_element(
                By.CSS_SELECTOR, 
                "input[type='checkbox'], .checkbox, body"
            )
            driver.execute_script("arguments[0].click();", checkbox)
            driver.switch_to.default_content()
            
            print("  ✓ Manual iframe click succeeded")
            return True
        
        return False
        
    except Exception as e:
        print(f"  ✗ Manual iframe click failed: {e}")
        driver.switch_to.default_content()
        return False


def solve_challenge(driver, timeout: int = 30, is_headless: bool = False) -> bool:
    """
    Detect and attempt to solve a Cloudflare Turnstile challenge.
    
    Tries multiple methods in order of reliability:
    1. GUI click (requires display, skipped in headless mode)
    2. SeleniumBase undetected click on iframe
    3. Manual iframe interaction with JavaScript
    
    Args:
        driver: SeleniumBase Driver instance
        timeout: Seconds to wait for page content to load
        is_headless: If True, skips GUI-based methods that require a display
    
    Returns:
        True if page loaded successfully, False otherwise
    """
    print("⏳ Checking for Cloudflare challenge...")
    
    # Already on the content page?
    if _is_page_loaded(driver):
        print("✅ No challenge detected, page already loaded")
        return True
    
    # No challenge detected in page source?
    if not _has_turnstile_challenge(driver):
        print("ℹ️  No Turnstile challenge detected, waiting for content...")
        if _wait_for_content(driver, timeout):
            print("✅ Page loaded")
            return True
        print("⚠️  Page did not load within timeout")
        return False
    
    # Challenge detected - try solving methods
    print("🔄 Turnstile challenge detected, attempting to solve...")
    
    # Method 1: GUI click (only if not headless)
    if not is_headless:
        _try_gui_click(driver)
    else:
        print("  ⊘ Skipping uc_gui_click_captcha (headless mode)")
    
    # Method 2: SeleniumBase undetected click
    if not _try_uc_click(driver):
        # Method 3: Manual iframe click (fallback)
        _try_manual_iframe_click(driver)
    
    # Wait for challenge to resolve
    print("⏳ Waiting for page to load after challenge attempt...")
    if _wait_for_content(driver, timeout):
        print("✅ Challenge resolved, page loaded")
        return True
    
    print("⚠️  Challenge did not resolve within timeout")
    return False
