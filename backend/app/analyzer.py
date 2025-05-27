from multiprocessing import Pool
import pylint.lint
import bandit.core.manager
import bandit.core.config
import bandit.core.constants
import ast
from radon.complexity import cc_visit


def calculate_complexity(tree):
    """Calculate total cyclomatic complexity from AST using radon."""
    blocks = cc_visit(tree)
    return sum(block.complexity for block in blocks)


def analyze_code(file_path):
    """Analyze code for errors, vulnerabilities, and metrics."""
    report = {
        "syntax_errors": [],
        "security_issues": [],
        "best_practices": [],
        "code_smells": [],
        "complexity": 0,
        "performance_issues": []
    }

    # Syntax and best practices (pylint)
    pylint_output = pylint.lint.Run([file_path], do_exit=False)
    linter_stats = pylint_output.linter.stats

    report["syntax_errors"] = linter_stats.get("by_msg", {}).get("syntax-error", [])
    report["best_practices"] = linter_stats.get("by_msg", {}).get("convention", [])
    report["code_smells"] = linter_stats.get("by_msg", {}).get("refactor", [])

    # Security vulnerabilities (bandit)
    b_conf = bandit.core.config.BanditConfig()
    b_mgr = bandit.core.manager.BanditManager(b_conf, "file")
    b_mgr.discover_files([file_path])
    b_mgr.run_tests()
    report["security_issues"] = [issue.as_dict() for issue in b_mgr.results]

    # Complexity analysis
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    report["complexity"] = calculate_complexity(tree)

    # Performance issues (basic heuristic example)
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "sleep(" in line:  # Example heuristic
                report["performance_issues"].append({
                    "line": i + 1,
                    "issue": "Potential performance bottleneck with sleep"
                })

    return report


def analyze_code_parallel(file_paths):
    """Run code analysis in parallel using multiprocessing."""
    with Pool() as pool:
        results = pool.map(analyze_code, file_paths)
    return results
