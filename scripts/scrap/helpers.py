"""
Utility helper functions for the Metrograph scraper.
"""

import os
import time
import random


def is_ci_environment() -> bool:
    """Check if running in a CI environment (GitHub Actions, etc.)."""
    ci = os.environ.get('CI', 'false').lower() == 'true'
    github_actions = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'
    return ci or github_actions


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Convert text to a safe filename by removing special characters.
    
    Args:
        text: The text to sanitize
        max_length: Maximum length of the resulting filename
    
    Returns:
        A filesystem-safe string
    """
    safe_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_')
    sanitized = ''.join(c if c in safe_chars else '_' for c in text)
    return sanitized[:max_length]


def wait_for_delay(min_seconds: float = 0, max_seconds: float = 15) -> None:
    """
    Wait for a random delay to avoid rate limiting.
    
    Args:
        min_seconds: Minimum delay in seconds
        max_seconds: Maximum delay in seconds
    """
    delay = random.uniform(min_seconds, max_seconds)
    print(f"⏱️  Waiting {delay:.1f} seconds...")
    time.sleep(delay)
