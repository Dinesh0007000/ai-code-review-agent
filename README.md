AI Code Review Agent
Overview
A command-line tool that analyzes and improves codebases in Python, Java, and JavaScript, generating refactored code and detailed reports.
Setup

Create and activate a virtual environment:python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows


Install dependencies:pip install -r requirements.txt


Install system dependencies for WeasyPrint:sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0


Create project structure:bash setup.sh


Populate files with provided code.

Usage
Run the CLI:
python src/main.py /path/to/codebase --output-dir output --config configs/default_config.json

Start the API server:
python src/api_server.py

Make a POST request to http://localhost:5000/review with JSON:
{
    "input_path": "/path/to/codebase",
    "output_dir": "output"
}

Features

Supports ZIP, folder, and Git repository inputs.
Analyzes Python, Java, and JavaScript code for syntax, bugs, security, and best practices.
Refactors code for readability, performance, and security.
Generates reports in HTML, PDF, and Markdown.
Configurable via JSON for priorities and custom rules.
REST API for CI/CD integration.

Requirements Addressed

Functional: Input processing, code analysis, improvement, output generation, configuration.
Non-Functional: Performance, security, reliability, usability.
Interfaces: CLI, REST API.
Constraints: Runs on standard hardware, supports major OS, integrates with version control.

Testing
Run tests:
pytest tests/

