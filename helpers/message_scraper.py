from bs4 import BeautifulSoup
from datetime import datetime
import re

def extract_messages_from_html(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    chat_container = soup.select_one("ul.MibAa")
    if not chat_container:
        print("[!] Chat container not found")
        return ""

    logs = []
    current_day = datetime.now().strftime("%Y-%m-%d")

    last_sender = None
    last_timestamp = "TBD"  # We'll fix this later

    for li in chat_container.select("li.T1yt2"):
        # Check if this message has a new sender
        sender_elem = li.select_one("header.R1ne3 span.nonIntl")
        if sender_elem:
            sender = sender_elem.text.strip()
            last_sender = sender
        else:
            sender = last_sender or "Unknown"

        # Get all message bubbles under this block (can be multiple)
        message_bubbles = li.select("div.KB4Aq div.p8r1z span.ogn1z")

        for bubble in message_bubbles:
            content = bubble.text.strip()

            # Skip blank or malformed messages
            if not content:
                continue

            logs.append(f"[{current_day} {datetime.now().strftime('%H:%M')}] {sender}: {content}")

    print(f"[✓] Parsed {len(logs)} messages from DOM.")
    return "\n".join(logs)
