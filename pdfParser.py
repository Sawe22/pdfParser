from flask import Flask, jsonify, request
import fitz  # PyMuPDF
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
JSON_FOLDER = 'json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(JSON_FOLDER):
    os.makedirs(JSON_FOLDER)

def process_pdf_and_segment(file_path):
    pdf_document = fitz.open(file_path)
    text = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()

    sections = {
        "Abstract": "",
        "Introduction": "",
        "Methodology": "",
        "Results": "",
        "Conclusion": ""
    }

    current_section = None
    for line in text.split('\n'):
        for section in sections:
            if section.lower() in line.lower():
                current_section = section
                break
        if current_section:
            sections[current_section] += line + '\n'

    return sections

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        sections = process_pdf_and_segment(file_path)
        
        # Save the sections as JSON
        json_file_path = os.path.join(app.config['JSON_FOLDER'], file.filename.split('.')[0] + '.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(sections, json_file, indent=4)
        
        # Print the sections in the terminal
        print(sections)
        
        return jsonify(sections), 200
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file'}), 400

if __name__ == '__main__':
    app.run(debug=True)

#curl -X POST -F "file=@$PathToPDF$" http://localhost:5000/upload