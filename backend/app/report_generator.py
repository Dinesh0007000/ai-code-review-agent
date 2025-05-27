import os
import difflib
import markdown
from datetime import datetime

def generate_report(original_path, improved_path, analysis_report, output_dir="output"):
    """Generate detailed report and comparisons."""
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, "review_report.md")
    
    # Read original and improved code
    with open(original_path, 'r') as f:
        original_code = f.readlines()
    with open(improved_path, 'r') as f:
        improved_code = f.readlines()
    
    # Generate diff
    diff = difflib.unified_diff(original_code, improved_code, fromfile=original_path, tofile=improved_path)
    
    # Create report
    report_content = f"""
# AI Code Review Report
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Original File**: {original_path}
**Improved File**: {improved_path}

## Analysis Summary
- **Syntax Errors**: {len(analysis_report["syntax_errors"])}
- **Security Issues**: {len(analysis_report["security_issues"])}
- **Code Smells**: {len(analysis_report["code_smells"])}
- **Complexity**: {analysis_report["complexity"]}

## Changes Made
```diff
{''.join(diff)}
```

## Metrics Comparison
- **Original Complexity**: {analysis_report["complexity"]}
- **Improved Complexity**: {analysis_report["complexity"]}  # Update with actual improved metrics
"""
    
    with open(report_file, 'w') as f:
        f.write(report_content)
    
    # Generate HTML report
    html_report = markdown.markdown(report_content)
    with open(os.path.join(output_dir, "review_report.html"), 'w') as f:
        f.write(f"<html><body>{html_report}</body></html>")
    
    return report_file