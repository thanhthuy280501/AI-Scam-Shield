# 🛡️ AI Scam Shield

A multilingual, AI-powered scam detection tool built to protect
**non-English speaking immigrants and the elderly** from AI-generated scams.

---

## Project Structure

```
ai_scam_shield/
├── app.py              ← Main entry point (run this)
├── scam_detector.py    ← Core AI scam analysis (GPT-4o)
├── translator.py       ← Language detection + translation (100+ languages)
├── ocr_reader.py       ← Extract text from images/screenshots
├── requirements.txt    ← Python dependencies
└── README.md
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Tesseract (for image/screenshot reading)
- macOS:  `brew install tesseract`
- Ubuntu: `sudo apt install tesseract-ocr`
- Windows: https://github.com/UB-Mannheim/tesseract/wiki

### 3. Set your OpenAI API key
```bash
export OPENAI_API_KEY="sk-your-key-here"
```
Get a key at: https://platform.openai.com/api-keys

### 4. Run the app
```bash
python app.py
```

---

## How It Works

```
User Input (text OR image)
        ↓
   [OCR if image]          ← ocr_reader.py
        ↓
  Detect Language          ← translator.py
        ↓
 Translate → English       ← translator.py
        ↓
  AI Scam Analysis         ← scam_detector.py (GPT-4o)
        ↓
Translate Result → User's Language
        ↓
  Display Verdict + Tips
```

---

## Supported Languages
English, Spanish, Vietnamese, Chinese, Tagalog, Korean,
Arabic, Hindi, Portuguese, Russian, French, and 100+ more.

---

## Future Features (Ideas)
- [ ] Web/mobile frontend (Flask or Streamlit)
- [ ] WhatsApp / SMS integration (Twilio)
- [ ] Report scam to FTC automatically
- [ ] Community scam database (crowdsourced)
- [ ] Voice input support for low-literacy users
