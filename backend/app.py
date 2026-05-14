import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, save_document, save_qa, get_history, get_document_info, get_all_documents
from pdf_utils import extract_text_from_pdf
from summarizer import generate_summary
from qa import answer_question
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Database
init_db()

@app.route('/')
def home():
    return jsonify({"message": "AI Research Paper API is running!", "status": "online"})

@app.route('/documents', methods=['GET'])
def list_documents():
    docs = get_all_documents()
    return jsonify(docs)

@app.route('/document/<int:doc_id>', methods=['GET'])
def get_single_document(doc_id):
    info = get_document_info(doc_id)
    if info:
        return jsonify(info)
    return jsonify({'error': 'Not found'}), 404

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"File saved to: {filepath}")
            
            # 1. Extract Text
            extracted_text = extract_text_from_pdf(filepath)
            print(f"Extracted {len(extracted_text)} characters.")
            
            if not extracted_text.strip():
                return jsonify({'error': 'No text could be extracted from this PDF.'}), 400

            # 2. Generate Summary
            summary = generate_summary(extracted_text)
            print("Summary generated successfully.")
            
            # 3. Save to Database
            doc_id = save_document(filename, filepath, extracted_text, summary)
            print(f"Document saved to DB with ID: {doc_id}")
            
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'document_id': doc_id,
                'summary': summary
            })
        
        return jsonify({'error': 'Invalid file type. Only PDFs are allowed.'}), 400
    except Exception as e:
        print(f"ERROR DURING UPLOAD: {str(e)}")
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    doc_id = data.get('document_id')
    question = data.get('question')
    
    if not doc_id or not question:
        return jsonify({'error': 'Document ID and question are required'}), 400
    
    # 1. Retrieve text and summary
    doc_info = get_document_info(doc_id)
    if not doc_info:
        return jsonify({'error': 'Document not found'}), 404
    
    # 2. Get answer
    answer = answer_question(question, doc_info['extracted_text'], doc_info['summary'])
    
    # 3. Save to history
    save_qa(doc_id, question, answer)
    
    return jsonify({
        'answer': answer
    })

@app.route('/history/<int:doc_id>', methods=['GET'])
def get_chat_history(doc_id):
    history = get_history(doc_id)
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
