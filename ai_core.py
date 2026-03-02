import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")


def generate_commit_message(diff_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}"

    prompt = f"""
Generate a short professional Git commit message.
Use imperative tone.
Keep under 15 words.
Do not explain anything.

Changes:
{diff_text}
"""

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"].strip().replace("\n", " ")
    #testing the code for git commit