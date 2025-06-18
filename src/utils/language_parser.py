import os
import ast
import javalang
import esprima

class LanguageParser:
    def detect_language(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.py':
            return 'python'
        elif ext == '.java':
            return 'java'
        elif ext in ('.js', '.jsx'):
            return 'javascript'
        return None

    def parse_file(self, file_path, language):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if language == 'python':
            try:
                return ast.parse(content)
            except SyntaxError:
                return None
        elif language == 'java':
            try:
                return javalang.parse.parse(content)
            except javalang.parser.JavaSyntaxError:
                return None
        elif language == 'javascript':
            try:
                return esprima.parseScript(content)
            except esprima.Error:
                return None
        return None