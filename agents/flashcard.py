import google.generativeai as genai
import os
import json
import re

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_flashcards(text):
    """
    Generate concise Q&A flashcards using Gemini 1.5 Flash.
    Returns a list of dicts: [{"question": "...", "answer": "..."}]
    """
    prompt = f"""
    You are a flashcard generator for students.
    Create 5 concise Q&A pairs from this text.

    Return **only valid JSON**, in this exact format:
    [
      {{"question": "What is ...?", "answer": "It is ..."}},
      ...
    ]

    Text:
    {text}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()

        # ✅ Clean markdown/code blocks if Gemini wraps JSON in ```json ... ```
        output = re.sub(r"```(json)?", "", output).strip("` \n")

        # ✅ Try parsing cleanly
        flashcards = json.loads(output)
        if isinstance(flashcards, list):
            return flashcards

        # ✅ If Gemini returns a dict or malformed text, wrap it safely
        return [{"question": "Parsing issue", "answer": str(flashcards)}]

    except json.JSONDecodeError:
        return [{"question": "⚠️ JSON Parsing Failed", "answer": output}]
    except Exception as e:
        return [{"question": "⚠️ Gemini API Error", "answer": str(e)}]
