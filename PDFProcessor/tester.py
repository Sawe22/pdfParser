from pdfProcessor import PDFProcessor


pdf_processor = PDFProcessor()
file_path = '2022WT2AbstractMudassirAbbasDaytonSe_BrianMarcus.pdf'
sections, metadata = pdf_processor.upload_file(file_path)
print(sections)  # Segmented sections
print(metadata)  # Extracted metadata