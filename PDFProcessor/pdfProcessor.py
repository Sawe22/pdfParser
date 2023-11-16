import os
import json
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

class PDFProcessor:
    def __init__(self):
        self.UPLOAD_FOLDER = 'uploads'
        self.JSON_FOLDER = 'json'
        
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)

        if not os.path.exists(self.JSON_FOLDER):
            os.makedirs(self.JSON_FOLDER)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

    def process_pdf_and_segment(self, file_path):
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

    def extract_information(self, pdf_path):
        # Extract metadata
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            information = pdf.metadata
            number_of_pages = len(pdf.pages)

        metadata = {
            'Author': information.author,
            'Creator': information.creator,
            'Producer': information.producer,
            'Subject': information.subject,
            'Title': information.title,
            'Number of pages': number_of_pages
        }

        # Append metadata to the existing JSON file
        file_name = os.path.basename(pdf_path)
        json_file_path = os.path.join(self.JSON_FOLDER, file_name.split('.')[0] + '.json')
        
        with open(json_file_path, 'r') as json_file:
            sections = json.load(json_file)

        sections['Metadata'] = metadata

        with open(json_file_path, 'w') as json_file:
            json.dump(sections, json_file, indent=4)

        return metadata

    def upload_file(self, file_path):
        file_name = os.path.basename(file_path)
        if self.allowed_file(file_name):
            file_destination = os.path.join(self.UPLOAD_FOLDER, file_name)
            os.rename(file_path, file_destination)

            sections = self.process_pdf_and_segment(file_destination)
            json_file_path = os.path.join(self.JSON_FOLDER, file_name.split('.')[0] + '.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(sections, json_file, indent=4)
            print(sections)

            metadata = self.extract_information(file_destination)
            print(metadata)

            return sections, metadata
        else:
            return {'error': 'Invalid file format. Please upload a PDF file'}
