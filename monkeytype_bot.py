#!/usr/bin/env python3
"""
Monkeytype typing helper (Selenium + keyboard automation).

For learning/personal practice only. Make sure this usage complies with
monkeytype.com's terms before running.
"""

import argparse
import sys
import time
from typing import List

from pynput.keyboard import Controller
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MONKEYTYPE_URL = "https://monkeytype.com/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open Monkeytype, extract the visible words, and auto-type them."
    )
    parser.add_argument(
        "--wpm",
        type=int,
        default=80,
        help="Target words per minute for auto typing (default: 80).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode.",
    )
    parser.add_argument(
        "--delay-before-start",
        type=float,
        default=3.0,
        help="Seconds to wait before typing starts (default: 3.0).",
    )
    return parser.parse_args()


def build_driver(headless: bool) -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    if headless:
        options.add_argument("--headless=new")

    return webdriver.Chrome(options=options)


def accept_cookie_popup(driver: webdriver.Chrome) -> None:
    selectors = [
        "button[aria-label='accept all']",
        "button[mode='acceptAll']",
    ]

    for selector in selectors:
        try:
            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            button.click()
            return
        except Exception:
            continue


def get_words_to_type(driver: webdriver.Chrome) -> List[str]:
    wait = WebDriverWait(driver, 20)

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#words .word"))
        )
    except TimeoutException:
        raise RuntimeError(
            "Could not find typing words on Monkeytype. UI may have changed."
        )

    word_elements = driver.find_elements(By.CSS_SELECTOR, "#words .word")
    words: List[str] = []

    for word in word_elements:
        raw = word.text.strip()
        if raw:
            words.append(raw)

    if not words:
        raise RuntimeError("No words were extracted from the page.")

    return words


def focus_typing_input(driver: webdriver.Chrome) -> None:
    # Monkeytype starts typing when the typing area is focused/clicked.
    try:
        typing_area = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#words"))
        )
        typing_area.click()
    except TimeoutException as exc:
        raise RuntimeError("Could not focus Monkeytype typing area.") from exc


def auto_type(words: List[str], wpm: int) -> None:
    keyboard = Controller()

    # Approx timing: 1 word + 1 trailing space per unit.
    per_word_seconds = 60.0 / max(wpm, 1)

    for word in words:
        keyboard.type(word)
        keyboard.type(" ")
        time.sleep(per_word_seconds)


def main() -> None:
    args = parse_args()
    driver = build_driver(args.headless)

    try:
        driver.get(MONKEYTYPE_URL)
        accept_cookie_popup(driver)

        words = get_words_to_type(driver)
        focus_typing_input(driver)

        print(f"Extracted {len(words)} words.")
        print(f"Starting to type in {args.delay_before_start:.1f}s...")
        time.sleep(max(args.delay_before_start, 0))

        auto_type(words, args.wpm)
        print("Finished typing run.")

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Keep browser open briefly so you can see the result.
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    main()
