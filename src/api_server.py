from flask import Flask, request, jsonify
from input_processor import InputProcessor
from code_analyzer import CodeAnalyzer
from code_improver import CodeImprover
from output_generator import OutputGenerator
from config_manager import ConfigManager
import os

app = Flask(__name__)
config_manager = ConfigManager()

@app.route('/review', methods=['POST'])
def review_codebase():
    data = request.json
    input_path = data.get('input_path')
    output_dir = data.get('output_dir', 'output')
    
    try:
        processor = InputProcessor(config_manager)
        analyzer = CodeAnalyzer(config_manager)
        improver = CodeImprover(config_manager)
        generator = OutputGenerator(config_manager)

        codebase_structure = processor.process_input(input_path)
        issues = analyzer.analyze_codebase(codebase_structure)
        improver.improve_codebase(codebase_structure, output_dir)
        generator.generate_output(codebase_structure, issues, output_dir)
        
        return jsonify({"status": "success", "output_dir": output_dir})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)