import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import openai

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# OpenAI API key (set as environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/summarize', methods=['POST'])
def summarize():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"})

    # Extract PDF text
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t

    if not text.strip():
        text = "[No text in PDF]"

    prompt = f"""
You are an AI study assistant. Analyze the study material below and generate:
1. Topic-wise summary
2. Key takeaways
3. Flashcards (Q&A)
4. Quiz questions (with answers)

Study material:
{text[:4000]}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1500
        )
        ai_output = response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({'error': f'Error generating AI content: {str(e)}'})

    return jsonify({'result': ai_output})

if __name__ == "__main__":
    print("Frontend folder:", os.path.join(BASE_DIR, "frontend"))
    app.run(debug=True)
