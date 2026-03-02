from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_commit_message(diff_text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Generate a short, professional Git commit message.
Use imperative tone.
Keep it under 15 words.
Do not explain anything.

Changes:
{diff_text}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )

    return response.text.strip().replace("\n", " ")