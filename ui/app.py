import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
import pandas as pd
from agents.reader import extract_text_from_pdf, split_into_chunks
from agents.flashcard import generate_flashcards
from agents.quiz import generate_quiz
from agents.planner import make_plan

# --- Streamlit Config ---
st.set_page_config(page_title="🧠 Study Assistant", layout="centered")
st.title("🧠 Study Assistant — Autonomous Revision Tool")

# --- Ensure outputs folder exists ---
os.makedirs("outputs", exist_ok=True)

# --- File Upload Section ---
uploaded = st.file_uploader("📂 Upload your notes (PDF)", type="pdf")

if uploaded:
    with st.spinner("📄 Uploading and reading your file..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded.getbuffer())
    st.success("✅ File uploaded successfully!")

    # --- READER AGENT ---
    st.header("📖 Reader Agent")
    with st.spinner("🔍 Extracting and structuring your content..."):
        text = extract_text_from_pdf("temp.pdf")
        if not text.strip():
            st.error("⚠️ No readable text found in this PDF. Try another file or a text-based one.")
            st.stop()
        chunks = split_into_chunks(text)

    st.success(f"✅ Extracted {len(chunks)} sections from your notes.")
    st.markdown("---")

    # --- FLASHCARD AGENT ---
    st.header("💡 Flashcards")
    if not chunks:
        st.warning("⚠️ No readable text found for flashcards.")
    else:
        with st.spinner("✨ Generating flashcards..."):
            flashcards = []
            for chunk in chunks[:3]:  # process only first 3 chunks for speed
                flashcards.extend(generate_flashcards(chunk))

            with open("outputs/flashcards.json", "w") as f:
                json.dump(flashcards, f, indent=2)

        st.success("✅ Flashcards generated successfully!")
        for fc in flashcards:
            st.markdown(f"**Q:** {fc['question']}")
            st.markdown(f"**A:** {fc['answer']}")
            st.markdown("---")

    # --- QUIZ AGENT ---
    st.header("🧩 Quiz Generator")
    if not chunks:
        st.info("No text available for quiz generation.")
    else:
        with st.spinner("🧠 Generating adaptive quiz..."):
            quiz = generate_quiz(" ".join(chunks[:2]))

            with open("outputs/quizzes.json", "w") as f:
                json.dump(quiz, f, indent=2)

        st.success("✅ Quiz generated successfully!")
        for q in quiz:
            st.markdown(f"**Q:** {q['question']}")
            for opt in q['options']:
                st.write("-", opt)
            st.markdown(f"**Answer:** {q['answer']}")
            st.markdown("---")

    # --- PLANNER AGENT ---
    st.header("📅 Revision Planner")
    with st.spinner("🗓️ Creating your revision plan..."):
        topics = [f"Topic {i+1}" for i in range(min(5, len(chunks)))]
        plan = make_plan(topics)
        with open("outputs/planner.json", "w") as f:
            json.dump(plan, f, indent=2)

    st.success("✅ Smart revision plan generated!")
    st.table(pd.DataFrame(plan))

    st.markdown("---")
    st.caption("🚀 Built with Streamlit + Gemini by Ayush Pandey")

else:
    st.info("👆 Upload a PDF to begin generating flashcards, quizzes, and a study plan.")
