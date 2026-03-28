"""
translator.py
Detects language and translates text using Google Cloud Translation API (free tier).
Supports 100+ languages — critical for non-English speaking immigrant users.

Install:  pip install google-cloud-translate
Setup:    https://cloud.google.com/translate/docs/setup
          Set environment variable: GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
          OR use the free `googletrans` library (no API key needed, but rate-limited).
"""

# ── Option A: Use the free `googletrans` library (easiest to start with) ──────
# pip install googletrans==4.0.0-rc1
try:
    from googletrans import Translator as GoogleTranslator, LANGUAGES

    _USE_GOOGLETRANS = True
except ImportError:
    _USE_GOOGLETRANS = False

# ── Option B: Official Google Cloud Translate (more reliable for production) ──
# from google.cloud import translate_v2 as google_translate


SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "zh-cn": "Chinese (Simplified)",
    "vi": "Vietnamese",
    "tl": "Tagalog",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "pt": "Portuguese",
    "ru": "Russian",
    "fr": "French",
}


class Translator:
    def __init__(self):
        if _USE_GOOGLETRANS:
            self._client = GoogleTranslator()
        else:
            raise ImportError(
                "Install googletrans:  pip install googletrans==4.0.0-rc1\n"
                "Or set up Google Cloud Translation and update translator.py."
            )

    def detect_language(self, text: str) -> str:
        """
        Returns the BCP-47 language code of the input text (e.g., 'en', 'vi', 'es').
        Falls back to 'en' if detection fails.
        """
        try:
            result = self._client.detect(text)
            return result.lang  # e.g., "vi", "es", "zh-cn"
        except Exception as e:
            print(f"[Translator] Language detection failed: {e}")
            return "en"

    def to_english(self, text: str, source_lang: str = "auto") -> str:
        """
        Translate any text to English.
        If already English, returns text unchanged.
        """
        if source_lang == "en":
            return text
        try:
            result = self._client.translate(text, src=source_lang, dest="en")
            return result.text
        except Exception as e:
            print(f"[Translator] Translation to English failed: {e}")
            return text  # return original if translation fails

    def from_english(self, text: str, target_lang: str) -> str:
        """
        Translate English text into the target language.
        Used to send results back in the user's native language.
        """
        if target_lang == "en":
            return text
        try:
            result = self._client.translate(text, src="en", dest=target_lang)
            return result.text
        except Exception as e:
            print(f"[Translator] Translation from English failed: {e}")
            return text
