import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="frontend/dist", static_url_path="")
CORS(app, resources={r"/summarize": {"origins": "*"}, r"/*": {"origins": "*"}})

# OpenAI API client (set in .env or environment variable OPENAI_API_KEY)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Add it to .env or environment variables.")

openai_client = OpenAI(api_key=api_key)

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    index_path = os.path.join(BASE_DIR, "frontend", "dist", "index.html")
    if os.path.exists(index_path):
        return app.send_static_file("index.html")
    return "<h1>Frontend not built. Run `npm run build` in frontend/</h1>", 501

@app.errorhandler(404)
def not_found(e):
    # SPA route fallback
    index_path = os.path.join(BASE_DIR, "frontend", "dist", "index.html")
    if os.path.exists(index_path):
        return app.send_static_file("index.html")
    return "Not Found", 404

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
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1500
        )
        ai_output = response.choices[0].message.content
    except Exception as e:
        return jsonify({'error': f'Error generating AI content: {str(e)}'}), 500

    if not ai_output or not ai_output.strip():
        return jsonify({'error': 'AI returned empty output. Verify OPENAI_API_KEY is set and PDF contains text.'}), 500

    return jsonify({'result': ai_output})

if __name__ == "__main__":
    print("Frontend folder:", os.path.join(BASE_DIR, "frontend"))
    app.run(debug=True)
