"""
AI Scam Shield - Main Application Entry Point
A multilingual AI-powered scam detection tool for immigrants and elderly users.
"""

from scam_detector import ScamDetector
from translator import Translator
from ocr_reader import OCRReader


def main():
    print("=" * 50)
    print("   AI Scam Shield - Proactive Scam Defense")
    print("=" * 50)

    detector = ScamDetector()
    translator = Translator()
    ocr = OCRReader()

    while True:
        print("\nHow would you like to check for a scam?")
        print("  1. Paste a text message or email")
        print("  2. Upload an image or screenshot")
        print("  3. Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            text = input("\nPaste the message here:\n> ").strip()
            if not text:
                print("No text entered.")
                continue

            # Detect language and translate to English if needed
            detected_lang = translator.detect_language(text)
            print(f"\n[Language detected: {detected_lang}]")

            english_text = translator.to_english(text, source_lang=detected_lang)

            # Analyze for scam
            result = detector.analyze(english_text)
            display_result(result, original_lang=detected_lang, translator=translator)

        elif choice == "2":
            image_path = input("\nEnter the image file path:\n> ").strip()
            extracted_text = ocr.extract_text(image_path)

            if not extracted_text:
                print("Could not extract text from image.")
                continue

            print(f"\n[Extracted text from image]:\n{extracted_text}\n")

            detected_lang = translator.detect_language(extracted_text)
            english_text = translator.to_english(extracted_text, source_lang=detected_lang)

            result = detector.analyze(english_text)
            display_result(result, original_lang=detected_lang, translator=translator)

        elif choice == "3":
            print("\nStay safe! Goodbye.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def display_result(result: dict, original_lang: str, translator: Translator):
    """Display the scam analysis result, translated back to the user's language."""
    verdict = result["verdict"]        # "SCAM", "SUSPICIOUS", or "LIKELY SAFE"
    confidence = result["confidence"]  # 0.0 to 1.0
    explanation = result["explanation"]
    red_flags = result["red_flags"]    # list of strings

    # Translate explanation back to user's language
    if original_lang != "en":
        explanation = translator.from_english(explanation, target_lang=original_lang)
        red_flags = [translator.from_english(f, target_lang=original_lang) for f in red_flags]

    print("\n" + "=" * 50)
    print(f"  VERDICT: {verdict}  (Confidence: {confidence:.0%})")
    print("=" * 50)
    print(f"\n{explanation}\n")

    if red_flags:
        print("Red Flags Found:")
        for flag in red_flags:
            print(f"  ⚠️  {flag}")

    if verdict == "SCAM":
        tip = "Do NOT respond, click any links, or send money. Report this to the FTC at reportfraud.ftc.gov"
    elif verdict == "SUSPICIOUS":
        tip = "Be cautious. Verify by calling the official number from the organization's real website."
    else:
        tip = "This looks okay, but always stay alert."

    if original_lang != "en":
        tip = translator.from_english(tip, target_lang=original_lang)

    print(f"\n💡 Tip: {tip}")
    print("=" * 50)


if __name__ == "__main__":
    main()
