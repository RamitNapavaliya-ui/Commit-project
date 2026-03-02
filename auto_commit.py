import os
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GEMINI_API_KEY not found.")
    exit()

genai.configure(api_key=api_key)

def get_staged_changes():
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def generate_message(diff):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
Generate a professional Git commit message
for the following changes.
Use imperative tone.
Keep it short.

{diff}
"""

    response = model.generate_content(prompt)
    return response.text.strip().replace("\n", " ")

def commit_and_push(message):
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push"])

def main():
    diff = get_staged_changes()

    if not diff:
        print("No staged changes found.")
        return

    print("Generating commit message...")
    message = generate_message(diff)

    print("Commit Message:", message)
    commit_and_push(message)

if __name__ == "__main__":
    main()

    #testing the code for git commit