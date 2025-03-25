import sys
import os

# 🛠 Ensure root directory is in sys.path BEFORE any helper imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from helpers.message_scraper import extract_messages_from_html
import time
from datetime import datetime

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

    # os.system("taskkill /F /IM chrome.exe")
    # os.system("taskkill /F /IM chromedriver.exe")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scroll_chat(driver, delay=1.5):
    try:
        scrollable = driver.find_element("css selector", "ul.MibAa")
        driver.execute_script("arguments[0].scrollTop -= 600;", scrollable)
        print("[↕] Scrolled chat container up")
        time.sleep(delay)
    except Exception as e:
        print(f"[!] Scroll failed: {e}")

def capture_snapchat():
    driver = launch_browser()
    driver.get("https://web.snapchat.com")
    input("➡️ Log into Snapchat Web, open the group chat, then press Enter...")

    # Optional screenshot scroll (visual backup)
    for i in range(4):  # scroll up 4 times
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        driver.save_screenshot(f"{OUTPUT_DIR}snap_web_{timestamp}.png")
        scroll_chat(driver)

    # Extract messages to log
    chat_text = extract_messages_from_html(driver)
    log_file = datetime.now().strftime(f"{LOG_DIR}%Y-%m-%d.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(chat_text)

    print(f"[📝] Saved chat log: {log_file}")
    driver.quit()

if __name__ == "__main__":
    capture_snapchat()
