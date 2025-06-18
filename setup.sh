#!/bin/bash
mkdir -p src/utils templates configs tests output
touch configs/default_config.json
touch src/main.py src/input_processor.py src/code_analyzer.py src/code_improver.py src/output_generator.py src/api_server.py src/utils/language_parser.py src/utils/metrics.py src/utils/security.py src/utils/logger.py
touch templates/report.html
touch tests/test_input.py tests/test_analyzer.py tests/test_improver.py
touch requirements.txt README.md
echo "Project structure created. Please populate files with provided code."