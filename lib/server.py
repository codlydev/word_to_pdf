# from flask import Flask, request, send_file
# from werkzeug.utils import secure_filename
# import os
# from docx import Document
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def docx_to_pdf(docx_path, pdf_path):
#     doc = Document(docx_path)
#     c = canvas.Canvas(pdf_path, pagesize=letter)
#     width, height = letter
#     y = height - 40
#     for para in doc.paragraphs:
#         c.drawString(40, y, para.text)
#         y -= 15
#         if y < 40:
#             c.showPage()
#             y = height - 40
#     c.save()

# @app.route('/convert', methods=['POST'])
# def convert():
#     if 'file' not in request.files:
#         return 'No file uploaded', 400

#     file = request.files['file']
#     filename = secure_filename(file.filename)
#     docx_path = os.path.join(UPLOAD_FOLDER, filename)
#     pdf_path = docx_path.replace('.docx', '.pdf')

#     file.save(docx_path)
#     docx_to_pdf(docx_path, pdf_path)
#     return send_file(pdf_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)




# from flask import Flask, request, send_file
# from werkzeug.utils import secure_filename
# import os
# from docx import Document
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def docx_to_pdf(docx_path, pdf_path):
#     doc = Document(docx_path)
#     pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
#     styles = getSampleStyleSheet()
#     story = []

#     for para in doc.paragraphs:
#         text = para.text.strip()
#         if text:
#             story.append(Paragraph(text, styles["Normal"]))
#             story.append(Spacer(1, 12))  # space between paragraphs

#     pdf.build(story)

# @app.route('/convert', methods=['POST'])
# def convert():
#     if 'file' not in request.files:
#         return 'No file uploaded', 400

#     file = request.files['file']
#     filename = secure_filename(file.filename)
#     docx_path = os.path.join(UPLOAD_FOLDER, filename)
#     pdf_path = docx_path.replace('.docx', '.pdf')

#     file.save(docx_path)
#     docx_to_pdf(docx_path, pdf_path)
#     return send_file(pdf_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def docx_to_pdf(docx_path, output_dir):
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    
    if not os.path.exists(soffice_path):
        raise RuntimeError("LibreOffice not found at the specified path.")

    try:
        result = subprocess.run([
            soffice_path,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            docx_path
        ], capture_output=True, text=True, check=True)
        print("Conversion success:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e.stderr)
        raise RuntimeError("LibreOffice conversion failed.")

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if not filename.lower().endswith('.docx'):
        return 'Only .docx files are supported.', 400

    docx_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(docx_path)

    try:
        docx_to_pdf(docx_path, UPLOAD_FOLDER)
    except Exception as e:
        return str(e), 500

    pdf_filename = filename.replace('.docx', '.pdf')
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    if not os.path.exists(pdf_path):
        return 'PDF conversion failed.', 500

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
