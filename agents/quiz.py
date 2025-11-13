def generate_quiz(text, context_title="Study Notes"):
    """
    Generate 5 relevant multiple-choice questions using Gemini.
    The questions will be strictly related to the uploaded notes or topic.
    """
    prompt = f"""
    You are a professional education content generator.

    Based on the text provided below, create exactly 5 **high-quality, conceptually relevant multiple-choice questions**.
    Each question should:
    - Be related directly to the content (no random general questions)
    - Have 4 clear and non-overlapping options (A, B, C, D)
    - Contain one correct answer
    - Avoid vague or trivial questions
    - Focus on technical and conceptual understanding

    Return only valid JSON in this format:
    [
      {{
        "question": "What is the main function of ...?",
        "options": ["A", "B", "C", "D"],
        "answer": "C"
      }}
    ]

    Context: {context_title}
    Text:
    {text}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()
        output = re.sub(r"```json|```", "", output).strip()
        quiz = json.loads(output)

        # sanity check: if not valid list
        if not isinstance(quiz, list):
            raise ValueError("Gemini output was not valid JSON list.")

        # optional filter for short or nonsense questions
        quiz = [q for q in quiz if len(q.get("question", "")) > 15]
        return quiz

    except Exception as e:
        return [{
            "question": "Gemini Quiz Generation Error",
            "options": ["Error", "Check API", "Invalid Key", "Retry"],
            "answer": "Error"
        }]
