"""
scam_detector.py
Core scam analysis logic powered by an LLM (OpenAI GPT-4o).
"""

import os
import json
import openai

# Set your OpenAI API key in environment:  export OPENAI_API_KEY="sk-..."
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a scam detection expert helping vulnerable people — including elderly users and non-English
speaking immigrants — identify whether a message is a scam.

Analyze the provided text and respond ONLY with a valid JSON object in this exact format:
{
  "verdict": "SCAM" | "SUSPICIOUS" | "LIKELY SAFE",
  "confidence": <float between 0.0 and 1.0>,
  "explanation": "<plain-language explanation in 1-3 sentences>",
  "red_flags": ["<flag 1>", "<flag 2>", ...]
}

Common scam signals to check:
- Urgency or threats ("act now", "or you will be arrested")
- Requests for gift cards, wire transfers, or crypto payments
- Impersonation of government agencies (IRS, SSA, USCIS, police)
- Suspicious links or phone numbers
- Requests for Social Security Number, passwords, or bank info
- Too-good-to-be-true prizes or offers
- Poor grammar or unusual sender addresses

Return ONLY the JSON. No extra text.
"""


class ScamDetector:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    def analyze(self, text: str) -> dict:
        """
        Analyze a piece of text (already in English) and return a scam verdict dict.
        Falls back to a rule-based check if the API call fails.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this message:\n\n{text}"},
                ],
                temperature=0.1,
                max_tokens=500,
            )
            raw = response.choices[0].message.content.strip()
            return json.loads(raw)

        except Exception as e:
            print(f"[ScamDetector] API error: {e}. Falling back to rule-based check.")
            return self._rule_based_fallback(text)

    def _rule_based_fallback(self, text: str) -> dict:
        """
        Simple keyword-based fallback when the API is unavailable.
        Not as accurate as the LLM, but provides basic protection.
        """
        text_lower = text.lower()

        scam_keywords = [
            "gift card", "wire transfer", "bitcoin", "cryptocurrency",
            "irs", "social security", "arrest warrant", "suspended",
            "verify your account", "click here", "urgent", "immediately",
            "you have won", "claim your prize", "send money",
        ]

        flags_found = [kw for kw in scam_keywords if kw in text_lower]

        if len(flags_found) >= 3:
            verdict, confidence = "SCAM", 0.85
            explanation = "Multiple high-risk scam keywords were found in this message."
        elif len(flags_found) >= 1:
            verdict, confidence = "SUSPICIOUS", 0.60
            explanation = "Some suspicious language was detected. Proceed with caution."
        else:
            verdict, confidence = "LIKELY SAFE", 0.70
            explanation = "No obvious scam keywords detected, but always stay alert."

        return {
            "verdict": verdict,
            "confidence": confidence,
            "explanation": explanation,
            "red_flags": flags_found,
        }
