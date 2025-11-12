import streamlit as st
import json
from agents.reader import extract_text_from_pdf, split_into_chunks
from agents.flashcard import generate_flashcards
from agents.quiz import generate_quiz
from agents.planner import make_plan

st.title("🧠 Study Assistant")

uploaded = st.file_uploader("Upload your notes (PDF)", type="pdf")

if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.getbuffer())
    text = extract_text_from_pdf("temp.pdf")
    chunks = split_into_chunks(text)
    st.success(f"Extracted {len(chunks)} sections!")

    st.header("Flashcards")
    flashcards = generate_flashcards(chunks[0])
    for fc in flashcards:
        st.markdown(f"**Q:** {fc['question']}")
        st.markdown(f"**A:** {fc['answer']}")
        st.markdown("---")

    st.header("Quizzes")
    quiz = generate_quiz(chunks[0])
    for q in quiz:
        st.markdown(f"**Q:** {q['question']}")
        for o in q['options']:
            st.write("-", o)
        st.markdown(f"**Answer:** {q['answer']}")
        st.markdown("---")

    st.header("Planner")
    plan = make_plan(["Topic 1", "Topic 2", "Topic 3"])
    for p in plan:
        st.write(p["topic"], "→ Revise on", p["revise_on"])
