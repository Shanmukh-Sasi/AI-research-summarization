# AI Research Paper Summarization and Q&A System

A full-stack application to extract text from research papers, generate extractive summaries, and answer questions based on the document content.

## 🚀 Features

- **PDF Upload**: Extracts text using PyMuPDF.
- **Extractive Summarization**: TF-IDF based sentence ranking.
- **Document Q&A**: Find relevant answers using TF-IDF and Cosine Similarity.
- **History Tracking**: Chat history stored in SQLite.
- **Modern UI**: Dark theme with glassmorphism and responsive design.

## 🛠️ Setup Instructions

### Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`.

### Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`.

## 📦 Tech Stack
- **Frontend**: React, Axios, Lucide-React, Vite.
- **Backend**: Flask, PyMuPDF, NLTK, Scikit-learn, SQLite.
