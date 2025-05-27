from flask import Flask, request, jsonify, send_from_directory
from app.utils import process_input, categorize_files, detect_project_structure
from app.analyzer import analyze_code
from app.improver import improve_code
from app.report_generator import generate_report
from app.config_manager import load_config
import os
import logging

app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')

# Configure logging
logging.basicConfig(filename='logs/review.log', level=logging.INFO)

@app.route('/api/review', methods=['POST'])
def review_code():
    data = request.get_json()
    input_path = data.get('input')
    config = load_config()
    
    try:
        input_dir = process_input(input_path)
        file_types = categorize_files(input_dir)
        structure = detect_project_structure(input_dir)
        
        for file_path, language in file_types.items():
            if any(excluded in file_path for excluded in config["excluded_files"]) or language == "unsupported":
                continue
            logging.info(f"Analyzing {file_path} ({language})")
            analysis_report = analyze_code(file_path, language)
            output_path = file_path.replace("input", "output")
            improve_code(file_path, output_path, analysis_report, language)
            generate_report(file_path, output_path, analysis_report)
        
        return jsonify({"message": "Code review completed", "output_dir": "output"})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/webhook', methods=['POST'])
def webhook():
    return jsonify({"message": "Webhook received"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
