import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from config_manager import ConfigManager
import markdown

class OutputGenerator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.env = Environment(loader=FileSystemLoader('templates'))

    def generate_output(self, codebase_structure, issues, file_changes, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare report data
        report_data = {
            'issues': issues,
            'refactoring': [],
            'corrections': []
        }
        
        # Log refactoring and corrections
        for change in file_changes:
            file_path = change['file']
            # Adjust path for temp_codebase or output_dir
            rel_path = os.path.relpath(file_path, start='temp_codebase' if file_path.startswith('temp_codebase') else output_dir)
            if 'improvements' in change:
                for improvement in change['improvements']:
                    report_data['refactoring'].append(f"{improvement} in {rel_path}")
            if 'status' in change and change['status'] == 'corrected':
                report_data['corrections'].append(f"Corrected errors in {rel_path}")

        # Generate HTML report
        template = self.env.get_template('report_template.html')
        html_content = template.render(report_data=report_data)
        html_path = os.path.join(output_dir, 'report.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate PDF report
        try:
            HTML(string=html_content).write_pdf(os.path.join(output_dir, 'report.pdf'))
        except Exception as e:
            print(f"Failed to generate PDF report: {e}")
        
        # Generate Markdown report
        md_path = os.path.join(output_dir, 'report.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Code Review Report\n\n")
            for issue in issues:
                f.write(f"## File: {os.path.relpath(issue['file'], start='temp_codebase')}\n")
                for i in issue['issues']:
                    f.write(f"- {i['type']}: {i.get('message', i.get('data', ''))}\n")
            f.write("\n## Refactoring\n")
            for r in report_data['refactoring']:
                f.write(f"- {r}\n")
            f.write("\n## Corrections\n")
            for c in report_data['corrections']:
                f.write(f"- {c}\n")