import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_flashcards(text):
    """Generate 5 flashcards from text."""
    prompt = f"""
    You are a flashcard generator.
    Create 5 question-answer pairs from this text.
    Return JSON like this:
    [{{"question": "...", "answer": "..."}}]
    Text:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response['choices'][0]['message']['content']
    try:
        return json.loads(output)
    except:
        return [{"question": "Parsing failed", "answer": output}]
