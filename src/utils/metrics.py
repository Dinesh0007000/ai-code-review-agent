import os
import radon.complexity
import radon.metrics

def calculate_metrics(file_path, language):
    metrics = {"lines_of_code": 0, "complexity": 0}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            metrics["lines_of_code"] = len(content.splitlines())
        
        if language == 'python':
            blocks = radon.complexity.cc_visit(content)
            metrics["complexity"] = sum(block.complexity for block in blocks) / max(1, len(blocks))
        else:
            metrics["complexity"] = "Not calculated for non-Python files"
    except Exception as e:
        metrics["error"] = f"Failed to calculate metrics: {str(e)}"
    return metrics