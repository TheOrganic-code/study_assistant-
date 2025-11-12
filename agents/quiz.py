import openai, json, os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_quiz(text):
    """Generate 5 multiple-choice questions."""
    prompt = f"""
    Make 5 multiple-choice questions from this text.
    Each question should have 4 options and one correct answer.
    Return JSON like this:
    [{{"question": "...", "options": ["A", "B", "C", "D"], "answer": "A"}}]
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
