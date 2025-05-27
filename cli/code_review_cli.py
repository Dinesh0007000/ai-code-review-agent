import argparse
import os
from app.utils import process_input, categorize_files, detect_project_structure
from app.analyzer import analyze_code
from app.improver import improve_code
from app.report_generator import generate_report
from app.config_manager import load_config

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("input", help="Path to codebase (ZIP, Git URL, or folder)")
    parser.add_argument("--config", default="config.yaml", help="Configuration file")
    args = parser.parse_args()
    
    config = load_config(args.config)
    input_path = process_input(args.input)
    file_types = categorize_files(input_path)
    structure = detect_project_structure(input_path)
    
    print("Processing files...")
    for file_path, file_type in file_types.items():
        if any(excluded in file_path for excluded in config["excluded_files"]):
            continue
        if file_type.startswith("text/x-python"):
            print(f"Analyzing {file_path}...")
            analysis_report = analyze_code(file_path)
            output_path = file_path.replace("input", "output")
            improve_code(file_path, output_path, analysis_report)
            generate_report(file_path, output_path, analysis_report)
            print(f"Completed {file_path}")

if __name__ == "__main__":
    main()