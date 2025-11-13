import streamlit as st
import os, json, datetime, requests, re
import google.generativeai as genai
import pandas as pd

# ==============================
# ✅ GEMINI CONFIG
# ==============================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Helper functions ---
def extract_text_from_pdf(pdf_path):
    # Placeholder extraction (since PyMuPDF or pdfminer not used)
    return "This is a placeholder extracted text. Replace with real PDF parsing logic."

def split_into_chunks(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def generate_flashcards(text):
    return [
        {"question": "What is AI?", "answer": "AI stands for Artificial Intelligence."},
        {"question": "What is Machine Learning?", "answer": "A subset of AI using data and algorithms."}
    ]

def make_plan(topics, start_date=None, gap_days=2, include_revision=True, skip_weekends=True):
    today = start_date or datetime.date.today()
    plan = []
    current_date = today

    for i, topic in enumerate(topics):
        if i > 0:
            current_date += datetime.timedelta(days=gap_days)
        while skip_weekends and current_date.weekday() >= 5:
            current_date += datetime.timedelta(days=1)

        entry = {"topic": topic, "study_on": current_date.strftime("%A, %d %B %Y")}
        if include_revision:
            review_1 = current_date + datetime.timedelta(days=2)
            review_2 = current_date + datetime.timedelta(days=5)
            entry["reviews"] = [
                review_1.strftime("%A, %d %B %Y"),
                review_2.strftime("%A, %d %B %Y"),
            ]
        plan.append(entry)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/planner.json", "w") as f:
        json.dump(plan, f, indent=2)
    return plan


# --- Gemini Quiz Generator ---
def generate_quiz(text):
    prompt = f"""
    You are a quiz generator.
    Create 5 multiple-choice questions from the given text.
    Each question should have exactly 4 options and one correct answer.
    Return only JSON in this format:
    [{{"question": "...", "options": ["A", "B", "C", "D"], "answer": "A"}}]

    Text:
    {text}
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    try:
        response = model.generate_content(prompt)
        output = response.text.strip()
        output = re.sub(r"```json|```", "", output).strip()
        quiz = json.loads(output)
        if isinstance(quiz, list):
            return quiz
        else:
            return [{"question": "Parsing issue", "options": [], "answer": output}]
    except Exception as e:
        return [{"question": "Gemini API Error", "options": [], "answer": str(e)}]


# ==============================
# ✅ PAGE CONFIG
# ==============================
st.set_page_config(page_title="Study Assistant", page_icon="🧠", layout="wide")

# ==============================
# 🎨 STYLING
# ==============================
st.markdown("""
<style>
body {
  background: #070708 url('https://i.ibb.co/vqyqnxC/black-wave-pattern.png') repeat;
  background-size: 300px;
  animation: bgScroll 40s linear infinite;
  color: #f2f3f4;
  font-family: 'Inter', sans-serif;
}
@keyframes bgScroll {
  0% { background-position: 0 0; }
  100% { background-position: 1000px 1000px; }
}

.main-title {
  text-align: center;
  font-size: 3.5rem;
  font-weight: 800;
  color: #fff;
  text-shadow: 0 0 25px rgba(100,150,255,0.3);
  margin-top: 2rem;
}
.subtitle {
  text-align: center;
  color: #a8abb3;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}
.navbar {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2.2rem;
  margin-bottom: 3.2rem;
}
.nav-btn {
  font-size: 1.5rem;
  border: none;
  border-radius: 26px;
  background: rgba(255,255,255,0.06);
  color: #f5f5f5;
  padding: 1.5rem 3.8rem;
  font-weight: 600;
  letter-spacing: 0.4px;
  backdrop-filter: blur(18px);
  transition: all 0.25s ease;
}
.nav-btn:hover {
  background: rgba(255,255,255,0.12);
  box-shadow: 0 0 50px rgba(120,160,255,0.4);
  transform: translateY(-3px) scale(1.02);
}
.glass {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 22px;
  padding: 2.5rem;
  margin-bottom: 2.2rem;
  backdrop-filter: blur(24px);
}
.stButton > button {
  border: none;
  border-radius: 18px;
  background: linear-gradient(145deg, #181818, #222);
  color: #f1f1f1;
  font-size: 1.25rem;
  font-weight: 500;
  padding: 1.2rem 2.5rem;
  width: 100%;
  box-shadow: 0 0 35px rgba(120,160,255,0.2);
  transition: all 0.3s ease;
}
.stButton > button:hover {
  background: linear-gradient(145deg, #2a2a2a, #1c1c1c);
  box-shadow: 0 0 55px rgba(120,160,255,0.5);
  transform: translateY(-3px) scale(1.02);
}
.footer {
  text-align: center;
  color: #8b8b8b;
  margin-top: 3.5rem;
  font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🧠 HEADER
# ==============================
st.markdown('<div class="main-title">Study Assistant</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Minimal • Intelligent • Designed for Focused Learners</p>', unsafe_allow_html=True)

# ==============================
# 🧭 NAVIGATION
# ==============================
nav = st.session_state.get("nav", "Dashboard")
cols = st.columns(5)
pages = ["Dashboard", "Reader", "Flashcards", "Quiz", "Planner"]
for i, p in enumerate(pages):
    if cols[i].button(p, key=p, use_container_width=True):
        st.session_state["nav"] = p
        nav = p

# ==============================
# 📂 FILE UPLOAD
# ==============================
uploaded = st.file_uploader("Upload your study material (PDF)", type="pdf")
if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("✅ File uploaded successfully!")

# ==============================
# 📋 DASHBOARD
# ==============================
if nav == "Dashboard":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Welcome to Your Study Hub 🚀")
    st.write("Choose a tool below to get started.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 📖 READER
# ==============================
elif nav == "Reader":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Reader Agent")
    if st.button("Run Reader Agent"):
        text = extract_text_from_pdf("temp.pdf")
        chunks = split_into_chunks(text)
        st.session_state["chunks"] = chunks
        st.success(f"✅ Extracted {len(chunks)} sections.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 💡 FLASHCARDS
# ==============================
elif nav == "Flashcards":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Flashcard Generator")
    if st.button("Generate Flashcards"):
        text = " ".join(st.session_state.get("chunks", []))
        flashcards = generate_flashcards(text)
        st.session_state["flashcards"] = flashcards
        with open("outputs/flashcards.json", "w") as f:
            json.dump(flashcards, f, indent=2)
        st.success("✅ Flashcards Ready!")
    if st.session_state.get("flashcards"):
        for fc in st.session_state["flashcards"]:
            st.markdown(f"**Q:** {fc['question']}")
            st.markdown(f"**A:** {fc['answer']}")
            st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 🧩 QUIZ
# ==============================
elif nav == "Quiz":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Quiz Generator")

    if "chunks" not in st.session_state or not st.session_state["chunks"]:
        st.warning("⚠️ Run Reader Agent first.")
    else:
        if st.button("Generate Quiz"):
            with st.spinner("🎯 Creating quiz..."):
                quiz = generate_quiz(" ".join(st.session_state["chunks"][:2]))
                st.session_state["quiz"] = quiz
                st.session_state["user_answers"] = [None] * len(quiz)
                st.session_state["submitted"] = False
            st.success("✅ Quiz ready!")

        if st.session_state.get("quiz"):
            for i, q in enumerate(st.session_state["quiz"]):
                st.markdown(f"**Q{i+1}. {q['question']}**")
                selected = st.radio(
                    f"Select answer for Q{i+1}",
                    q["options"],
                    key=f"q{i}",
                    horizontal=True
                )
                st.session_state["user_answers"][i] = selected
                st.markdown("---")

            if st.button("Submit Quiz"):
                st.session_state["submitted"] = True

        if st.session_state.get("submitted"):
            quiz = st.session_state.get("quiz", [])
            answers = st.session_state.get("user_answers", [])
            score = sum(1 for i, q in enumerate(quiz) if answers[i] == q["answer"])
            st.success(f"🏁 You scored **{score}/{len(quiz)}** 🎉")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 🗓️ PLANNER
# ==============================
elif nav == "Planner":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Study Planner")
    if st.button("Generate Study Plan"):
        topics = [f"Topic {i+1}" for i in range(5)]
        plan = make_plan(topics)
        st.session_state["plan"] = plan
        st.success("✅ Plan Created!")
    if st.session_state.get("plan"):
        st.table(pd.DataFrame(st.session_state["plan"]))
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# ⚡ FOOTER
# ==============================
st.markdown('<p class="footer">Built by <b>Ayush Pandey</b> — Designed for Focused Minds ⚡</p>', unsafe_allow_html=True)
