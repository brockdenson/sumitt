import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_messages_from_html(driver):
    logs = []
    last_sender = None
    actions = ActionChains(driver)

    message_items = driver.find_elements(By.CSS_SELECTOR, "li.T1yt2")

    for item in message_items:
        try:
            # Get sender from within the message item
            try:
                sender_elem = item.find_element(By.CSS_SELECTOR, "header.R1ne3 span.nonIntl")
                sender = sender_elem.text.strip()
                last_sender = sender
            except:
                sender = last_sender or "Unknown"

            # Hover over the message bubble to reveal timestamp
            try:
                bubble = item.find_element(By.CSS_SELECTOR, "div.KB4Aq")
                actions.move_to_element(bubble).perform()
                time.sleep(0.2)  # Allow timestamp to appear
            except Exception as e:
                print(f"[!] Failed to hover: {e}")
                continue

            # Try to get timestamp from <time> element now in DOM
            timestamp = "Unknown"
            try:
                time_elem = item.find_element(By.CSS_SELECTOR, "header.R1ne3 time")
                if time_elem.get_attribute("datetime"):
                    dt = datetime.fromisoformat(time_elem.get_attribute("datetime"))
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                pass  # fallback to Unknown

            # Extract message text (could be multiple per sender block)
            bubbles = item.find_elements(By.CSS_SELECTOR, "div.KB4Aq div.p8r1z span.ogn1z")
            for b in bubbles:
                content = b.text.strip()
                if content:
                    logs.append(f"[{timestamp}] {sender}: {content}")

        except Exception as e:
            print(f"[!] Failed to parse message: {e}")
            continue

    print(f"[✓] Parsed {len(logs)} messages from DOM with timestamps.")
    return "\n".join(logs)
