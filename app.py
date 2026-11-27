import streamlit as st
from generator import generate_questions
from syllabus import SYLLABUS

st.set_page_config(page_title="Maths Master AI", page_icon="📘", layout="wide")

st.markdown("""
<style>
.main {background-color:#f7f9fc;}
.block-container {padding-top:2rem;}
.hero {padding:1.4rem 1.6rem;border-radius:16px;background:linear-gradient(120deg,#123c69,#2a6f97);color:white;margin-bottom:1.2rem;}
.hero h1 {color:white;margin:0;}
.hero p {color:#e7f2fa;margin:.4rem 0 0 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📘 Maths Master AI</h1><p>TG & AP Intermediate Mathematics • Question & Solution Generator</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Generation Settings")
    year = st.selectbox("Intermediate Year", list(SYLLABUS.keys()))
    subject = st.selectbox("Subject", list(SYLLABUS[year].keys()))
    chapter = st.selectbox("Chapter", SYLLABUS[year][subject])
    count = st.selectbox("Number of Questions", [10, 20, 30, 40, 50], index=4)
    qtypes = st.multiselect("Question Types", ["MCQ", "VSAQ", "SAQ", "LAQ"], default=["MCQ", "VSAQ", "SAQ", "LAQ"])
    difficulty = st.selectbox("Difficulty", ["Mixed", "Easy", "Medium", "Hard"])
    st.caption("Solutions are generated in English.")

col1, col2 = st.columns([2,1])
with col1:
    st.subheader("Create a Question Set")
    st.write(f"**Selected:** {year} · {subject} · {chapter}")
    st.info("This starter version includes a demo question bank for selected topics. Connect an AI provider in Step 2 for broader chapter-wise generation.")
with col2:
    st.metric("Questions per set", count)
    st.metric("Output language", "English")

if not qtypes:
    st.warning("Select at least one question type.")
else:
    if st.button("✨ Generate Questions", type="primary", use_container_width=True, disabled=not qtypes):
        with st.spinner("Preparing questions and solutions..."):
            st.session_state["questions"] = generate_questions(
                year=year, subject=subject, chapter=chapter,
                count=count, qtypes=qtypes, difficulty=difficulty
            )
            st.session_state["set_title"] = f"{year} - {chapter}"

if "questions" in st.session_state:
    questions = st.session_state["questions"]
    st.divider()
    st.subheader(f"Generated Set: {st.session_state.get('set_title','')}")
    st.caption(f"{len(questions)} questions")
    for i, q in enumerate(questions, 1):
        with st.expander(f"Q{i}. [{q['type']}] {q['question']}", expanded=(i == 1)):
            if q.get("options"):
                for opt in q["options"]:
                    st.write(opt)
            st.markdown("**Answer**")
            st.write(q["answer"])
            st.markdown("**Detailed Solution**")
            st.markdown(q["solution"])
            st.caption(f"Difficulty: {q['difficulty']}")

    from exporter import make_pdf
    pdf_bytes = make_pdf(st.session_state["set_title"], questions)
    st.download_button(
        "⬇️ Download Questions & Solutions PDF",
        data=pdf_bytes,
        file_name="maths_master_question_set.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.divider()
st.caption("Maths Master AI • Starter MVP • Always review generated questions and solutions before academic use.")
