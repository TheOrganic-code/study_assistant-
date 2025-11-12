from agents.reader import extract_text_from_pdf, split_into_chunks
from agents.flashcard import generate_flashcards
from agents.quiz import generate_quiz
from agents.planner import make_plan

if __name__ == "__main__":
    pdf_path = "temp.pdf"  # test PDF
    print("Extracting text from:", pdf_path)
    text = extract_text_from_pdf(pdf_path)
    chunks = split_into_chunks(text)

    print(f"Extracted {len(chunks)} chunks.\n")

    if chunks:
        print("Generating flashcards...")
        flashcards = generate_flashcards(chunks[0])
        print(flashcards)

        print("\nGenerating quiz...")
        quiz = generate_quiz(chunks[0])
        print(quiz)

        print("\nGenerating study plan...")
        plan = make_plan(["Math", "Physics", "AI"])
        print(plan)
