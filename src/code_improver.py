import os
import ast
import javalang
import esprima

class CodeImprover:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def improve_codebase(self, codebase_structure, issues):
        improved_files = []
        corrected_files = []
        os.makedirs("output/sample_codebase/corrected", exist_ok=True)

        for file_info, file_issues in zip(codebase_structure["files"], issues):
            file_path = file_info["path"]
            language = file_info["language"]
            improvements = []
            corrected_content = None

            with open(file_path, 'r') as f:
                original_content = f.read()

            if language == 'python':
                corrected_content, python_improvements = self.improve_python(file_path, original_content, file_issues)
                improvements.extend(python_improvements)
            elif language == 'java':
                corrected_content, java_improvements = self.improve_java(file_path, original_content, file_issues)
                improvements.extend(java_improvements)
            elif language == 'javascript':
                corrected_content, js_improvements = self.improve_javascript(file_path, original_content, file_issues)
                improvements.extend(js_improvements)

            # Save improved (original with docstrings) and corrected files
            rel_path = os.path.relpath(file_path, "sample_codebase")
            output_path = os.path.join("output/sample_codebase", rel_path)
            corrected_output_path = os.path.join("output/sample_codebase/corrected", rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            os.makedirs(os.path.dirname(corrected_output_path), exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(original_content if corrected_content is None else corrected_content)
            if corrected_content:
                with open(corrected_output_path, 'w') as f:
                    f.write(corrected_content)

            improved_files.append({"file": file_path, "improvements": improvements})
            if corrected_content:
                corrected_files.append({"file": corrected_output_path, "status": "corrected"})

        return improved_files, corrected_files

    def improve_python(self, file_path, content, issues):
        improvements = []
        try:
            tree = ast.parse(content)
            # Add docstrings
            new_content = content
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        docstring = '    """Function description."""\n'
                        lines = new_content.splitlines()
                        insert_line = node.lineno
                        lines.insert(insert_line, docstring)
                        new_content = '\n'.join(lines)
                        improvements.append("Added docstring to function")

            # Fix W292 (no newline at end)
            for issue in issues["issues"]:
                if issue["type"] == "lint" and "W292" in issue["message"]:
                    new_content = new_content.rstrip() + '\n'
                    improvements.append("Added newline at end of file")

            return new_content, improvements
        except SyntaxError:
            return content, improvements

    def improve_java(self, file_path, content, issues):
        improvements = []
        try:
            tree = javalang.parse.parse(content)
            # Add Javadoc
            new_content = content
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    if not node.documentation:
                        javadoc = f'    /**\n     * Method description.\n     */\n'
                        lines = new_content.splitlines()
                        insert_line = node.position[0] - 1
                        lines.insert(insert_line, javadoc)
                        new_content = '\n'.join(lines)
                        improvements.append("Added Javadoc to method")

            # Fix NoPackage
            for issue in issues["issues"]:
                if issue["type"] == "lint" and "NoPackage" in issue["message"]:
                    new_content = f"package com.example;\n\n{new_content}"
                    improvements.append("Added package declaration")

            # Fix UseUtilityClass (add private constructor)
            for issue in issues["issues"]:
                if issue["type"] == "lint" and "UseUtilityClass" in issue["message"]:
                    class_name = None
                    for path, node in tree:
                        if isinstance(node, javalang.tree.ClassDeclaration):
                            class_name = node.name
                            break
                    if class_name:
                        constructor = f'\n    private {class_name}() {{}}\n'
                        lines = new_content.splitlines()
                        insert_line = next((i for i, line in enumerate(lines) if f"class {class_name}" in line), -1) + 1
                        lines.insert(insert_line, constructor)
                        new_content = '\n'.join(lines)
                        improvements.append("Added private constructor for utility class")

            return new_content, improvements
        except javalang.parser.JavaSyntaxError:
            return content, improvements

    def improve_javascript(self, file_path, content, issues):
        improvements = []
        try:
            # Enable comment parsing
            tree = esprima.parseScript(content, {"loc": True, "comment": True, "range": True})
            # Attach comments to nodes
            esprima.parseScript(content, {"loc": True, "comment": True, "range": True, "tokens": True, "attachComment": True})
            new_content = content
            for node in tree.body:
                if node.type == 'FunctionDeclaration':
                    # Safely check leadingComments
                    leading_comments = node.leadingComments if hasattr(node, 'leadingComments') and node.leadingComments else []
                    if not any(c.type == 'BlockComment' and '/**' in c.value for c in leading_comments):
                        jsdoc = '/**\n * Function description.\n */\n'
                        lines = new_content.splitlines()
                        insert_line = node.loc.start.line - 1
                        lines.insert(insert_line, jsdoc)
                        new_content = '\n'.join(lines)
                        improvements.append("Added JSDoc to function")

            # Fix no-unused-vars
            for issue in issues["issues"]:
                if issue["type"] == "lint" and "no-unused-vars" in issue["message"]:
                    lines = new_content.splitlines()
                    try:
                        line_num = int(issue["message"].split(":")[1].split(",")[0].strip()) - 1
                        if line_num < len(lines):
                            lines[line_num] = f"// Removed unused: {lines[line_num]}"
                            improvements.append(f"Commented out unused variable/function at line {line_num + 1}")
                        new_content = '\n'.join(lines)
                    except (IndexError, ValueError):
                        improvements.append("Failed to parse line number for no-unused-vars")

            return new_content, improvements
        except esprima.Error as e:
            improvements.append(f"JavaScript parsing failed: {str(e)}")
            return content, improvements