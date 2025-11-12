import google.generativeai as genai
import os
import json
import re

# Configure Gemini API key securely
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(text):
    """
    Generate 5 multiple-choice questions (MCQs) from the given text using Gemini 1.5 Flash.

    Each question should have:
      - 'question': The question text
      - 'options': A list of 4 choices
      - 'answer': The correct option (A/B/C/D)

    Returns: List[dict]
    """
    prompt = f"""
    You are an expert MCQ generator.
    Create 5 multiple-choice questions from the text below.

    Each question must have 4 options and 1 correct answer.
    Return **only valid JSON** in this format:
    [
      {{
        "question": "What is ...?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "A"
      }}
    ]

    Text:
    {text}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()

        # 🧹 Remove code blocks (e.g. ```json ... ```)
        output = re.sub(r"```(json)?", "", output).strip("` \n")

        # ✅ Parse JSON safely
        quiz_data = json.loads(output)
        if isinstance(quiz_data, list):
            # Ensure proper keys exist in each question
            cleaned = []
            for q in quiz_data:
                cleaned.append({
                    "question": q.get("question", "N/A"),
                    "options": q.get("options", []),
                    "answer": q.get("answer", "N/A")
                })
            return cleaned

        # Handle non-list responses
        return [{"question": "Parsing issue", "options": [], "answer": str(quiz_data)}]

    except json.JSONDecodeError:
        return [{"question": "⚠️ JSON Parsing Failed", "options": [], "answer": output}]
    except Exception as e:
        return [{"question": "⚠️ Gemini API Error", "options": [], "answer": str(e)}]
