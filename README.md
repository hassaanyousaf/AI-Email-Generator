# 📧 AI Cold Email Generator

An AI-powered cold email generator built with **Streamlit**, **LangChain**, **ChromaDB**, **HuggingFace sentence-transformers**, and **Groq Llama 3.1**.[web:40][web:43][web:44][web:13]  
Upload your CV, paste a job description, and get a personalized cold email grounded in your actual resume content.

---

## Features:

- Upload CV as **PDF or TXT**.
- Extracts and chunks resume text automatically.
- Builds a **ChromaDB vector store** from your CV for semantic search.[web:40][web:43]
- Uses **HuggingFace `all-MiniLM-L6-v2` embeddings** to represent text.[web:41][web:44]
- Retrieves the most relevant CV snippets for a given job description.
- Generates a concise, tailored cold email using **Groq Llama 3.1 via LangChain’s `ChatGroq` and `RetrievalQA`**.
- Clean Streamlit UI:  
  1) Upload CV → 2) Paste JD → 3) Generate Email.

---

## Tech Stack:

- **Python**
- **Streamlit** – UI and app framework.[web:39][web:42]  
- **LangChain** – LLM orchestration and RetrievalQA chain.[web:68][web:73]  
- **ChromaDB** – Vector store for CV chunks.  
- **HuggingFace sentence-transformers** – `all-MiniLM-L6-v2` embeddings.  
- **Groq API** – Llama 3.1–8B chat model via `langchain-groq`.[web:13][web:60]

---

## Setup:

1. **Create and activate a virtual environment**
```
   python -m venv venv
venv\Scripts\activate
```
2. **Install dependencies**
```
pip install -r requirements.txt
```
3. **Configure environment variables**

- Create a `.env` file in the project root:

  ```
  GROQ_API_KEY= The key.
  ```

- Never commit `.env`. Use `.env.example` as a template.

---

## Run the App
```
streamlit run app.py
```

### Then open the URL shown in the terminal (usually `http://localhost:8501`).

---

## Working:

1. **Upload CV** – App reads PDF/TXT and extracts raw text using `pypdf` or simple decoding.  
2. **Build Vector Store** – CV text is split into chunks and embedded with `all-MiniLM-L6-v2`; chunks + vectors are stored in ChromaDB.  
3. **Job Description Input** – User pastes the JD in a text area.  
4. **Retrieve Relevant CV Chunks** – Chroma performs similarity search against the JD to find the most relevant experience.  
5. **Generate Email** – LangChain’s `RetrievalQA` passes JD + retrieved CV snippets + an email prompt to Groq’s Llama 3.1 model, which returns a ready-to-use cold email.

---







