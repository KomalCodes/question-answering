import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from content_extraction import extract_text_from_pdfs  # For PDF text extraction
from hierarchical_indexing import build_hierarchical_tree  # For hierarchical indexing
from retrieval import bm25_retrieve, semantic_retrieve  # Retrieval techniques
from rag import generate_answer_with_llm  # RAG-based answer generation

app = Flask(__name__)

# Configurations for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_pdfs():
    if request.method == 'POST':
        if 'pdf_files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        files = request.files.getlist('pdf_files')

        if len(files) != 3:
            return jsonify({"error": "Please upload exactly three PDF files."}), 400

        file_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)

        # Extract and index the text
        extracted_text = extract_text_from_pdfs(file_paths)
        hierarchical_tree = build_hierarchical_tree(extracted_text)
        
        # Store hierarchical_tree for querying later (can be in-memory or database)
        return render_template('index.html', message="Files uploaded successfully.")

    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "Query is missing"}), 400
    
    # Step 1: Use retrieval techniques to get relevant content
   
    retrieved_content = semantic_retrieve(query, hierarchical_tree)  # Or use bm25_retrieve
    
    # Step 2: Generate an answer using the retrieved content (RAG)
    answer = generate_answer_with_llm(retrieved_content, query)
    
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
