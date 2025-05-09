from flask import Flask, request, jsonify
import PyPDF2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/api/pdf_to_text", methods=["POST"])
def pdf_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join("/tmp", filename)  # Vercel only allows temp files

    file.save(filepath)

    try:
        text = ""
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
                text += "\n\n" + ("-" * 80) + "\n\n"

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
