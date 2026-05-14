import sqlite3
import os

DB_PATH = 'research_app.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table for documents
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            extracted_text TEXT,
            summary TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for Q&A history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_document(filename, filepath, extracted_text, summary):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documents (filename, filepath, extracted_text, summary)
        VALUES (?, ?, ?, ?)
    ''', (filename, filepath, extracted_text, summary))
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def save_qa(doc_id, question, answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO qa_history (document_id, question, answer)
        VALUES (?, ?, ?)
    ''', (doc_id, question, answer))
    conn.commit()
    conn.close()

def get_history(doc_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT question, answer, asked_at FROM qa_history WHERE document_id = ? ORDER BY asked_at DESC', (doc_id,))
    history = cursor.fetchall()
    conn.close()
    return [dict(row) for row in history]

def get_document_info(doc_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT extracted_text, summary FROM documents WHERE id = ?', (doc_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, uploaded_at FROM documents ORDER BY uploaded_at DESC')
    docs = cursor.fetchall()
    conn.close()
    return [dict(row) for row in docs]
