import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pytz

def extract_messages_from_html(driver, cutoff_start=None, cutoff_end=None):
    logs = []
    last_sender = None
    actions = ActionChains(driver)
    eastern = pytz.timezone("US/Eastern")

    if not cutoff_start or not cutoff_end:
        now = datetime.now()
        cutoff_start = now.replace(hour=4, minute=0, second=0, microsecond=0)
        if now.hour < 4:
            cutoff_start -= timedelta(days=1)
        cutoff_end = cutoff_start + timedelta(days=1)

    message_items = driver.find_elements(By.CSS_SELECTOR, "li.T1yt2")

    for item in message_items:
        try:
            # Get sender
            try:
                sender_elem = item.find_element(By.CSS_SELECTOR, "header.R1ne3 span.nonIntl")
                sender = sender_elem.text.strip()
                last_sender = sender
            except:
                sender = last_sender or "Unknown"

            # Hover to reveal timestamp
            try:
                bubble = item.find_element(By.CSS_SELECTOR, "div.KB4Aq")
                actions.move_to_element(bubble).perform()
                time.sleep(0.1)
            except:
                continue  # Skip if no bubble to hover on

            # Extract timestamp
            timestamp_str = "Unknown"
            dt = None
            try:
                time_elem = item.find_element(By.CSS_SELECTOR, "header.R1ne3 time")
                if time_elem.get_attribute("datetime"):
                    dt = datetime.fromisoformat(time_elem.get_attribute("datetime"))
            except:
                continue

            # Compare against UTC cutoff window
            if not dt:
                continue
            dt_naive = dt.replace(tzinfo=None)
            if dt_naive < cutoff_start or dt_naive >= cutoff_end:
                continue

            # Convert to local time for display
            dt_local = dt.astimezone(eastern)
            timestamp_str = dt_local.strftime("%Y-%m-%d %H:%M")

            # Extract message text
            bubbles = item.find_elements(By.CSS_SELECTOR, "div.KB4Aq div.p8r1z span.ogn1z")
            for b in bubbles:
                content = b.text.strip()
                if content:
                    logs.append(f"[{timestamp_str}] {sender}: {content}")

        except Exception as e:
            print(f"[!] Failed to parse message: {e}")
            continue

    print(f"[✓] Parsed {len(logs)} messages from DOM within 4AM–4AM window.")
    return "\n".join(logs)

def get_earliest_timestamp(driver):
    timestamps = []
    actions = ActionChains(driver)
    message_items = driver.find_elements(By.CSS_SELECTOR, "li.T1yt2")

    for item in message_items:
        try:
            bubble = item.find_element(By.CSS_SELECTOR, "div.KB4Aq")
            actions.move_to_element(bubble).perform()
            time.sleep(0.1)

            time_elem = item.find_element(By.CSS_SELECTOR, "header.R1ne3 time")
            if time_elem.get_attribute("datetime"):
                dt = datetime.fromisoformat(time_elem.get_attribute("datetime"))
                timestamps.append(dt)
        except:
            continue

    return min(timestamps) if timestamps else None
