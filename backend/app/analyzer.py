import pylint.lint
import bandit.core.manager
import subprocess
import json
import ast

def analyze_code(file_path, language):
    """Analyze code for errors, vulnerabilities, and metrics."""
    report = {
        "syntax_errors": [],
        "security_issues": [],
        "best_practices": [],
        "code_smells": [],
        "complexity": 0,
        "performance_issues": []
    }
    
    if language == "python":
        # Syntax and best practices (pylint)
        pylint_output = pylint.lint.Run([file_path], do_exit=False)
        report["syntax_errors"] = [msg.as_dict() for msg in pylint_output.linter.stats.get("by_msg", {}).get("syntax-error", [])]
        report["best_practices"] = [msg.as_dict() for msg in pylint_output.linter.stats.get("by_msg", {}).get("convention", [])]
        report["code_smells"] = [msg.as_dict() for msg in pylint_output.linter.stats.get("by_msg", {}).get("refactor", [])]
        
        # Security vulnerabilities (bandit)
        b_mgr = bandit.core.manager.BanditManager()
        b_mgr.discover_files([file_path])
        b_mgr.run_tests()
        report["security_issues"] = b_mgr.get_issue_list()
        
        # Complexity analysis
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        report["complexity"] = len([node for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While))])
        
        # Performance issues (basic heuristic)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "sleep(" in line:
                    report["performance_issues"].append({"line": i+1, "issue": "Potential performance bottleneck with sleep"})
    
    elif language == "javascript":
        # Run ESLint for syntax, best practices, and code smells
        try:
            eslint_output = subprocess.run(
                ["npx", "eslint", file_path, "--format", "json"],
                capture_output=True, text=True, check=True
            )
            eslint_results = json.loads(eslint_output.stdout)
            for result in eslint_results:
                for message in result.get("messages", []):
                    if message["severity"] == 2:
                        report["syntax_errors"].append({"line": message["line"], "message": message["message"]})
                    elif message["ruleId"].startswith("no-"):
                        report["code_smells"].append({"line": message["line"], "message": message["message"]})
                    else:
                        report["best_practices"].append({"line": message["line"], "message": message["message"]})
        except subprocess.CalledProcessError as e:
            report["syntax_errors"].append({"message": f"ESLint failed: {e.stderr}"})
        
        # Complexity (basic heuristic for JS)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            report["complexity"] = sum(1 for line in lines if any(kw in line for kw in ["if (", "for (", "while ("]))
        
        # Performance issues (basic heuristic)
        for i, line in enumerate(lines):
            if "setTimeout(" in line:
                report["performance_issues"].append({"line": i+1, "issue": "Potential performance bottleneck with setTimeout"})
    
    return report
