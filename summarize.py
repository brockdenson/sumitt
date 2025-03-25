from openai import OpenAI
import os
from datetime import datetime
from helpers.ocr import extract_chat_from_folder
from helpers.sms import send_sms
from config import OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_chat(chat_text):
    prompt = f"""
You are an assistant summarizing a group of close friends' Snapchat group chat messages.
Write a casual weekly digest including:

1. Big News
2. Inside Jokes or Funny Moments
3. Drama or Tea
4. Upcoming Plans

Be witty but clear. Help someone who missed everything stay in the loop.

Chat:
{chat_text}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You summarize Snapchat group chats into weekly recaps."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1000
    )
    return response.choices[0].message.content

def save_summary(summary):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    with open(f"output/summary_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(summary)

def main():
    chat_text = extract_chat_from_folder("screenshots/")
    if not chat_text.strip():
        print("No text extracted. Check your screenshots.")
        return

    summary = summarize_chat(chat_text)
    print("Summary:\n", summary)

    send_sms(summary)
    save_summary(summary)

if __name__ == "__main__":
    main()
