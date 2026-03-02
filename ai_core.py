import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=api_key)

# Use free-tier optimized model
model = genai.GenerativeModel("gemini-1.5-flash")

MAX_DIFF_LENGTH = 3000


def trim_diff(diff):
    if len(diff) > MAX_DIFF_LENGTH:
        return diff[:MAX_DIFF_LENGTH]
    return diff


def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"API Error: {str(e)}"


# ------------------------------
# Commit Generator
# ------------------------------
def generate_commit(diff):
    diff = trim_diff(diff)

    prompt = f"""
Generate a Conventional Commit message.

Rules:
- Format strictly: type: short description
- Types: feat, fix, docs, style, refactor, test, chore
- Max 72 characters
- No emojis
- No explanation

Git diff:
{diff}
"""
    return ask_ai(prompt)


# ------------------------------
# Branch Generator
# ------------------------------
def generate_branch(diff):
    diff = trim_diff(diff)

    prompt = f"""
Generate a git branch name.

Rules:
- Use kebab-case
- Format: type/short-description
- Types: feature, fix, refactor, docs, chore, test
- No spaces
- Max 5 words

Git diff:
{diff}
"""
    return ask_ai(prompt)


# ------------------------------
# PR Generator
# ------------------------------
def generate_pr(diff):
    diff = trim_diff(diff)

    prompt = f"""
Generate a professional Pull Request description.

Structure:

## Summary
Short summary

## What Changed
- Bullet points

## Why
Reason

## Testing
How to test

Be concise and professional.

Git diff:
{diff}
"""
    return ask_ai(prompt)