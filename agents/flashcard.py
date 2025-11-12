import google.generativeai as genai
import os, json, re

# ✅ Configure Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_flashcards(text):
    """
    Generate 5 flashcards (question-answer pairs) using Gemini.
    """
    prompt = f"""
    You are a flashcard generator.
    Create 5 concise and educational question-answer pairs in JSON format.
    Return JSON as:
    [{{"question": "...", "answer": "..."}}]

    Text:
    {text}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()
        output = re.sub(r"```json|```", "", output).strip()
        flashcards = json.loads(output)
        if isinstance(flashcards, list):
            return flashcards
        else:
            return [{"question": "Parsing issue", "answer": output}]
    except Exception as e:
        return [{"question": "Gemini API Error", "answer": str(e)}]
