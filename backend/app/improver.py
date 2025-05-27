import ast
import autopep8
import subprocess
import os

def improve_code(file_path, output_path, analysis_report, language):
    """Refactor and optimize code."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if language == "python":
        # Read original code
        with open(file_path, 'r') as f:
            code = f.read()
        
        # Standardize code style (PEP8)
        improved_code = autopep8.fix_code(code, options={'aggressive': 1})
        
        # Improve documentation
        tree = ast.parse(improved_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    node.body.insert(0, ast.Expr(value=ast.Str(s=f"Function {node.name} description")))
        
        improved_code = ast.unparse(tree)
        
        # Apply security fixes
        for issue in analysis_report["security_issues"]:
            if "hardcoded_secret" in str(issue):
                improved_code = improved_code.replace(issue.text, "os.getenv('SECRET_KEY')")
    
    elif language == "javascript":
        # Standardize code style with Prettier
        try:
            prettier_output = subprocess.run(
                ["npx", "prettier", file_path, "--write", output_path],
                capture_output=True, text=True, check=True
            )
            with open(output_path, 'r') as f:
                improved_code = f.read()
        except subprocess.CalledProcessError as e:
            improved_code = f"// Error formatting with Prettier: {e.stderr}\n"
            with open(file_path, 'r') as f:
                improved_code += f.read()
        
        # Add basic documentation (e.g., JSDoc)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        improved_lines = []
        for line in lines:
            if line.strip().startsWith("function ") and not line.strip().startsWith("/**"):
                function_name = line.split("function ")[1].split("(")[0].strip()
                improved_lines.append(f"/** @function {function_name} */\n")
            improved_lines.append(line)
        improved_code = "".join(improved_lines)
    
    # Write improved code
    with open(output_path, 'w') as f:
        f.write(improved_code)
    
    return improved_code
