from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

def generate_commit_message(diff_text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    # IMPORTANT: specify API version for free keys
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version="v1")
    )

    prompt = f"""
Generate a short professional Git commit message.
Use imperative tone.
Keep under 15 words.
No explanation.

Changes:
{diff_text}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )

    return response.text.strip().replace("\n", " ")