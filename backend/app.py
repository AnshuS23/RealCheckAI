from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import insert_analysis, fetch_all_analyses
import os, datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "RealCheck AI backend is running"})

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    verdict = "🤖 Likely AI" if "AI" in text or len(text) > 150 else "🧍 Human"
    explanation = "Detected patterns typical of AI text." if "AI" in text else "Human-like variety and tone."
    
    result = {
        "type": "text",
        "input_text": text[:60] + "..." if len(text) > 60 else text,
        "filename": None,
        "verdict": verdict,
        "explanation": explanation,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    insert_analysis(result)
    return jsonify(result)

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    verdict = "🧍 Human" if filename.endswith('.jpg') else "🤖 Likely AI"
    explanation = "JPEG structure suggests a real photo." if filename.endswith('.jpg') else "Non-standard format — likely AI generated."
    
    result = {
        "type": "image",
        "input_text": None,
        "filename": filename,
        "verdict": verdict,
        "explanation": explanation,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    insert_analysis(result)
    return jsonify(result)

@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(fetch_all_analyses())

if __name__ == '__main__':
    app.run(debug=True)
