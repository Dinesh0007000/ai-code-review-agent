from flask import Flask, request, jsonify
from app.utils import process_input, categorize_files, detect_project_structure
from app.analyzer import analyze_code
from app.improver import improve_code
from app.report_generator import generate_report
from app.config_manager import load_config
import os
import logging

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/review.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/api/review', methods=['POST'])
def review_code():
    data = request.get_json()
    input_path = data.get('input')
    logging.info(f"Received review request for: {input_path}")
    
    config = load_config()

    try:
        input_dir = process_input(input_path)
        logging.info(f"Processed input directory: {input_dir}")

        file_types = categorize_files(input_dir)
        logging.info(f"Categorized files: {file_types}")

        structure = detect_project_structure(input_dir)
        logging.info(f"Detected project structure: {structure}")
        
        for file_path, file_type in file_types.items():
            if any(excluded in file_path for excluded in config["excluded_files"]):
                logging.info(f"Excluded file: {file_path}")
                continue

            if file_type.startswith("text/x-python"):
                logging.info(f"Analyzing file: {file_path}")
                analysis_report = analyze_code(file_path)

                output_path = file_path.replace("input", "output")
                improve_code(file_path, output_path, analysis_report)
                logging.info(f"Improved file saved to: {output_path}")

                generate_report(file_path, output_path, analysis_report)
                logging.info(f"Report generated for: {file_path}")

        logging.info("Code review completed successfully.")
        return jsonify({"message": "Code review completed", "output_dir": "output"})

    except Exception as e:
        logging.error(f"Error during review: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/webhook', methods=['POST'])
def webhook():
    logging.info("Webhook received")
    return jsonify({"message": "Webhook received"})

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    app.run(debug=True)
