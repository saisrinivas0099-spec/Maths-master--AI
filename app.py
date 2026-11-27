import streamlit as st
from syllabus import SYLLABUS
from generator import generate_questions, GeminiConfigError, GeminiGenerationError
from exporter import make_pdf

st.set_page_config(page_title="Maths Master AI", page_icon="📘", layout="wide")
st.markdown("""<style>.block-container{padding-top:1.5rem}.hero{padding:1.4rem;border-radius:16px;background:linear-gradient(120deg,#123c69,#2a6f97);color:white}.hero h1{color:white}</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>📘 Maths Master AI</h1><p>TG & AP Intermediate Mathematics · AI Question & Solution Generator</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Question Settings")
    year=st.selectbox("Intermediate Year",list(SYLLABUS.keys()))
    subject=st.selectbox("Subject",list(SYLLABUS[year].keys()))
    chapter=st.selectbox("Chapter",SYLLABUS[year][subject])
    count=st.selectbox("Number of Questions",[10,20,30,40,50],index=4)
    qtypes=st.multiselect("Question Types",["MCQ","VSAQ","SAQ","LAQ"],default=["MCQ","VSAQ","SAQ","LAQ"])
    difficulty=st.selectbox("Difficulty",["Mixed","Easy","Medium","Hard"])
    st.caption("Language: English")

st.subheader("Create an AI-generated question set")
st.write(f"**Selected:** {year} · {subject} · {chapter}")
st.info("AI-generated questions are drafts. Review every item before using it in a DPP or examination.")
if st.button("✨ Generate with Gemini AI",type="primary",use_container_width=True):
    if not qtypes: st.warning("Select at least one question type.")
    else:
        try:
            with st.spinner("Gemini is preparing questions and solutions..."):
                st.session_state["questions"]=generate_questions(year,subject,chapter,count,qtypes,difficulty)
                st.session_state["set_title"]=f"{year} - {subject} - {chapter}"
            st.success(f"Generated {len(st.session_state['questions'])} questions.")
        except (GeminiConfigError,GeminiGenerationError) as e: st.error(str(e))
        except Exception as e: st.error(f"Unexpected error: {e}")

if "questions" in st.session_state:
    qs=st.session_state["questions"]
    st.divider()
    st.subheader(st.session_state["set_title"])
    for i,q in enumerate(qs,1):
        with st.expander(f"Q{i}. [{q['type']}] {q['question']}",expanded=(i==1)):
            for opt in q.get("options",[]): st.write(opt)
            st.markdown("**Answer**")
            st.write(q["answer"])
            st.markdown("**Detailed Solution**")
            st.markdown(q["solution"])
            st.caption("Difficulty: "+q["difficulty"])
    st.download_button("⬇️ Download Questions & Solutions PDF",make_pdf(st.session_state["set_title"],qs),
                       file_name="maths_master_ai_questions.pdf",mime="application/pdf",use_container_width=True)
st.divider()
st.caption("Maths Master AI · AI-assisted draft content · Verify syllabus alignment and calculations before publication.")
from exporter import generate_pdf

pdf_buffer = generate_pdf(questions_list, title="Intermediate 1st Year - Mathematics IA")
st.download_button("Download PDF", data=pdf_buffer, file_name="questions.pdf", mime="application/pdf")
