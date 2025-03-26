import sys
import os

# 🛠 Ensure root directory is in sys.path BEFORE any helper imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import time
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from helpers.message_scraper import extract_messages_from_html, get_earliest_timestamp

OUTPUT_DIR = "screenshots/"
LOG_DIR = "logs/"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def launch_browser():
    options = Options()
    profile_path = f"{os.getcwd()}\\selenium-profile"
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_previous_day_4am_cutoff():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    cutoff = yesterday.replace(hour=4, minute=0, second=0, microsecond=0)
    return cutoff

def scroll_up_until_cutoff(driver, cutoff_start, delay=1.5, max_scrolls=30):
    print(f"[⬆️] Scrolling up until we see message before {cutoff_start.strftime('%Y-%m-%d %H:%M')}")
    scrollable = driver.find_element("css selector", "ul.MibAa")

    for i in range(max_scrolls):
        earliest = get_earliest_timestamp(driver)
        if earliest and earliest.replace(tzinfo=None) < cutoff_start:
            print(f"[✅] Found message before 4AM previous day: {earliest}")
            break
        driver.execute_script("arguments[0].scrollTop -= 800;", scrollable)
        print(f"[↕] Scrolled up ({i + 1})")
        time.sleep(delay)

    print("[🛑] Finished scrolling up.")

def capture_snapchat():
    driver = launch_browser()
    driver.get("https://web.snapchat.com")
    input("➡️ Log into Snapchat Web, open the group chat, then press Enter...")

    # Get the 4AM of previous calendar day in local time
    local_cutoff_start = get_previous_day_4am_cutoff()
    cutoff_start = local_cutoff_start.astimezone(timezone.utc).replace(tzinfo=None)
    cutoff_end = cutoff_start + timedelta(days=1)

    scroll_up_until_cutoff(driver, cutoff_start)

    chat_text = extract_messages_from_html(driver, cutoff_start=cutoff_start, cutoff_end=cutoff_end)

    # Save log file as the date of the 4AM start (the day you're capturing)
    log_file = local_cutoff_start.strftime(f"{LOG_DIR}%Y-%m-%d.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(chat_text)

    print(f"[📝] Saved chat log: {log_file}")
    driver.quit()

if __name__ == "__main__":
    capture_snapchat()
