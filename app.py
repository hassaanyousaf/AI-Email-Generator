import streamlit as st
import os
from io import StringIO
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from pypdf import PdfReader


load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

st.markdown(
    "<h1 style='text-align: center;'>📧 AI Cold Email Generator</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "**Your personalized cold email generator based on your resume.**"
)
if not groq_key:
    st.error("GROQ_API_KEY is missing in .env file. Add it and restart the app.")
    st.stop()

def text_extract(uploaded_file):
    """Extract plain text from an uploaded PDF or TXT file."""
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
        return text
    else:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8", errors="ignore"))
        return stringio.read()

@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def Build_vectorstore(cv_text):
    embeddings = get_embeddings()
    chunks = [c.strip() for c in cv_text.split("\n\n") if c.strip()]
    if not chunks:
        chunks = [cv_text]
    return Chroma.from_texts(chunks, embeddings)

def build_qa_chain(vectorstore):
    llm = ChatGroq( model_name="llama-3.1-8b-instant", temperature=0.3, groq_api_key=groq_key, )
    return RetrievalQA.from_chain_type( llm, retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    )


if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "cv_loaded" not in st.session_state:
    st.session_state.cv_loaded = False

st.subheader("📤 Upload your CV (PDF or TXT)")
uploaded_cv = st.file_uploader("Upload your CV / Resume", type=["pdf", "txt"])

if uploaded_cv is not None:
    with st.spinner("Reading and indexing your CV..."):
        cv_text = text_extract(uploaded_cv)
        if not cv_text.strip():
            st.error("Could not read any text from this file. Try another CV.")
        else:
            vectorstore = Build_vectorstore(cv_text)
            qa_chain = build_qa_chain(vectorstore)
            st.session_state.vectorstore = vectorstore
            st.session_state.qa_chain = qa_chain
            st.session_state.cv_loaded = True
            st.success(" CV indexed successfully. You can now paste a job description.")



st.subheader("📤 Write Job Description")

job_desc = st.text_area(
    "Paste the job description here:",
    height=220,
    placeholder="e.g., Looking for Python developer with data science experience...",
)

generate = st.button("Generate Personalized Cold Email", type="primary")

if generate:
    if not st.session_state.cv_loaded:
        st.error("Please upload your CV first and wait until it is indexed.")
    elif not job_desc.strip():
        st.error("Please paste a job description.")
    else:
        vectorstore = st.session_state.vectorstore
        qa_chain = st.session_state.qa_chain
        if vectorstore is None or qa_chain is None:
            st.error("CV index not available. Re-upload your CV.")
        else:
            with st.spinner("Generating personalized email from your CV + job description..."):
                relevant_docs = vectorstore.similarity_search(job_desc, k=2)
                context = "\n\n".join(doc.page_content for doc in relevant_docs)

                prompt = f"""
                You are writing a cold email for a job application.
                JOB DESCRIPTION:
                {job_desc}
                CANDIDATE CV HIGHLIGHTS (only use what is relevant):
                {context}
                Task:
                - Write a concise, personalized cold email for this role.
                - Mention 2–3 specific matches between the CV and the job description.
                - Structure:
                  1) Short subject line
                  2) Greeting
                  3) 2–3 short paragraphs showing fit
                  4) Clear call to action
                  5) Professional sign-off (use a generic name like "Your Name").
                Keep it under 180 words. Make it natural and professional.
                """

                result = qa_chain.invoke({"query": prompt})
                st.success(" Email Generated!")
                st.markdown("### 📧 **Generated Email**")
                st.markdown(result["result"])


