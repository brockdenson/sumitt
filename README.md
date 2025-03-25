
# 📬 Sumitt – Weekly Snapchat Group Chat Summarizer

**Sumitt** is a smart automation tool that reads Snapchat group chat activity from screenshots, summarizes the week's activity using GPT-4, and delivers a digest to a designated phone number (via SMS). It's built to help keep friends like Colton in the loop—without needing to be on Snapchat.

---

## ✨ Features

- 🧠 Extracts chat text from screenshots using OCR (Tesseract)
- 🤖 Summarizes chat logs using OpenAI's GPT-4 with contextual formatting
- 📩 Sends summaries via SMS using Twilio
- 📁 Automatically archives summaries for future reference
- 🗂️ Clean folder structure with future expansion in mind

---

## 🏗️ Project Structure

```
sumitt/
├── config.py               # API keys and phone numbers (excluded from Git)
├── summarize.py            # Main pipeline runner
├── requirements.txt        # Python dependencies
├── output/                 # Auto-saved summary logs
├── screenshots/            # Drop screenshots here for processing
└── helpers/
    ├── ocr.py              # Image-to-text extraction (Tesseract)
    └── sms.py              # Twilio SMS integration
```

---

## 🚀 Getting Started

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/brockdenson/sumitt.git
cd sumitt
```

### ✅ 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have **Tesseract OCR** installed on your machine:

#### Windows:
- Download from: https://github.com/tesseract-ocr/tesseract
- Add install path (e.g., `C:\Program Files\Tesseract-OCR`) to your **System PATH**

#### macOS:
```bash
brew install tesseract
```

#### Ubuntu:
```bash
sudo apt install tesseract-ocr
```

---

## 🔐 Configuration

Create a file called `config.py` in the root directory and add:

```python
# config.py

OPENAI_API_KEY = "your-openai-api-key"

TWILIO_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_FROM_NUMBER = "+1YOUR_TWILIO_PHONE"
TO_PHONE_NUMBER = "+1TO_PHONE"
```

> 💡 Tip: You can switch to using a `.env` file or environment variables later for better security.

---

## 🧪 Usage

1. Drop any number of `.png`, `.jpg`, or `.jpeg` screenshots into the `/screenshots` folder.
2. Run the main script:

```bash
python summarize.py
```

This will:
- Extract text from the screenshots via OCR
- Generate a weekly digest using GPT-4
- Send the summary to Colton via SMS using Twilio
- Archive the summary in `/output/` with a timestamp

---

## 🔮 Planned Features

We're building this into a fully automated, memory-aware system:

- 📸 Automated daily screenshot capture using a dedicated Snapchat account
- 🤖 Discord bot for two-way communication with Colton
- 🧠 Fine-tuned GPT with memory of group context, jokes, and names
- 📆 Weekly scheduling (e.g., every Sunday evening)
- 🔄 “Ask the group” responses + reply forwarding
- 📚 Local summary history for “Year in Review” features
- 🧩 Custom digest formats (TL;DR, plans only, gossip mode, etc.)

---

## 📄 License

MIT License – open-source and free to use. Attribution appreciated but not required.

---

## 🤝 Contributions

Currently private and under active development. Future PRs and issues will be welcomed once MVP is launched.

---

## 👨‍💻 Author

**Brock Denson**  
GitHub: [@brockdenson](https://github.com/brockdenson)  
Built for fun and utility to help friends stay connected.
