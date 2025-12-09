# 📧 AI Cold Email Generator

An AI-powered cold email generator built with **Streamlit**, **LangChain**, **ChromaDB**, **HuggingFace sentence-transformers**, and **Groq Llama 3.1**.[web:40][web:43][web:44][web:13]  
Upload your CV, paste a job description, and get a personalized cold email grounded in your actual resume content.

---

## 🔧 Features

- Upload CV as **PDF or TXT**.
- Extracts and chunks resume text automatically.
- Builds a **ChromaDB vector store** from your CV for semantic search.[web:40][web:43]
- Uses **HuggingFace `all-MiniLM-L6-v2` embeddings** to represent text.[web:41][web:44]
- Retrieves the most relevant CV snippets for a given job description.
- Generates a concise, tailored cold email using **Groq Llama 3.1 via LangChain’s `ChatGroq` and `RetrievalQA`**.[web:13][web:68][web:73]
- Clean Streamlit UI:  
  1) Upload CV → 2) Paste JD → 3) Generate Email.

---

## 📦 Tech Stack

- **Python**
- **Streamlit** – UI and app framework.[web:39][web:42]  
- **LangChain** – LLM orchestration and RetrievalQA chain.[web:68][web:73]  
- **ChromaDB** – Vector store for CV chunks.  
- **HuggingFace sentence-transformers** – `all-MiniLM-L6-v2` embeddings.  
- **Groq API** – Llama 3.1–8B chat model via `langchain-groq`.[web:13][web:60]

---

## 🚀 Setup

1. **Clone the repo**

