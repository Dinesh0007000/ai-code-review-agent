import pytest
import os
from src.code_improver import CodeImprover
from src.config_manager import ConfigManager

def test_improve_files(tmp_path):
    config = ConfigManager()
    improver = CodeImprover(config)
    
    temp_codebase = tmp_path / "temp_codebase"
    temp_codebase.mkdir()
    
    py_file = temp_codebase / "test.py"
    py_file.write_text("def hello():\n    print('hello')\n")
    java_file = temp_codebase / "test.java"
    java_file.write_text("public class Test { public static void main(String[] args) {}}\n")
    js_file = temp_codebase / "test.js"
    js_file.write_text("function hello() { console.log('test'); }\n")
    
    codebase = {
        "files": [
            {"path": str(py_file), "language": "python"},
            {"path": str(java_file), "language": "java"},
            {"path": str(js_file), "language": "javascript"}
        ]
    }
    
    output_dir = tmp_path / "output"
    improver.improve_codebase(codebase, str(output_dir))
    
    with open(output_dir / "test.py", encoding='utf-8') as f:
        content = f.read()
        assert '"""Function hello."""' in content
        assert '# Improved by AI Code Review Agent' in content
    
    with open(output_dir / "test.java", encoding='utf-8') as f:
        content = f.read()
        assert '/**' in content
        assert '// Improved by AI Code Review Agent' in content
    
 with open(output_dir / "test.js", encoding='utf-8') as f:
 content = f.read()
 assert '/**' in content
 assert '// Improved by AI Code Review Agent' in content