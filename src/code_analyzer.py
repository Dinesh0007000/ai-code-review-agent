import subprocess
import bandit
from bandit.core import config, manager
from utils.metrics import calculate_metrics
from utils.security import check_security_issues
import os
import shutil

class CodeAnalyzer:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.bandit_config = config.BanditConfig()

    def analyze_codebase(self, codebase_structure):
        issues = []
        for file_info in codebase_structure["files"]:
            file_path = file_info["path"]
            language = file_info["language"]
            file_issues = []

            if language == 'python':
                try:
                    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
                    file_issues.extend([{"type": "lint", "message": line} for line in result.stdout.splitlines()])
                    b_mgr = manager.BanditManager(config=self.bandit_config, agg_type='file')
                    b_mgr.discover_files([file_path], recursive=False)
                    b_mgr.run_tests()
                    file_issues.extend(check_security_issues(b_mgr.get_issue_list()))
                except FileNotFoundError:
                    file_issues.append({"type": "error", "message": "flake8 or bandit not installed; Python analysis incomplete"})
            elif language == 'java':
                try:
                    result = subprocess.run(
                        ['/home/dk/pmd/bin/run.sh', 'pmd', '-d', file_path, '-f', 'text', '-R', 'rulesets/java/quickstart.xml'],
                        capture_output=True, text=True
                    )
                    file_issues.extend([{"type": "lint", "message": line} for line in result.stdout.splitlines()])
                except (FileNotFoundError, OSError) as e:
                    file_issues.append({"type": "error", "message": f"PMD not executable at /home/dk/pmd/bin/run.sh; Java analysis skipped: {str(e)}"})
                except subprocess.CalledProcessError as e:
                    file_issues.append({"type": "error", "message": f"PMD analysis failed: {e.stderr}"})
            elif language == 'javascript':
                eslint_path = '/home/dk/.npm-global/bin/eslint'
                if not eslint_path:
                    file_issues.append({"type": "error", "message": "ESLint not found in PATH"})
                else:
                    try:
                        print(f"Running ESLint: {eslint_path} {file_path} --format compact")
                        result = subprocess.run(
                            [eslint_path, file_path, '--format', 'compact'],
                            capture_output=True, text=True, check=False
                        )
                        # Capture both stdout and stderr, handle non-zero exit codes
                        output = result.stdout.strip() or result.stderr.strip()
                        if output:
                            file_issues.extend([{"type": "lint", "message": line} for line in output.splitlines()])
                        else:
                            file_issues.append({"type": "lint", "message": "No issues found"})
                    except Exception as e:
                        file_issues.append({"type": "error", "message": f"ESLint analysis failed: {str(e)}"})

            metrics = calculate_metrics(file_path, language)
            file_issues.append({"type": "metrics", "data": metrics})

            issues.append({"file": file_path, "issues": file_issues})
        return issues