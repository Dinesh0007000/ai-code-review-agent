import pytest
import os
from src.output_generator import OutputGenerator
from src.config_manager import ConfigManager

def test_generate_output(tmp_path):
    config = ConfigManager()
    generator = OutputGenerator(config)
    
    codebase = {
        "files": [
            {"path": "temp_codebase/test.py", "language": "python"},
            {"path": "temp_codebase/test.java", "language": "java"},
            {"path": "temp_codebase/test.js", "language": "javascript"}
        ]
    }
    
    issues = [
        {"file": "temp_codebase/test.py", "issues": [{"type": "lint", "message": "Test issue"}]},
        {"file": "temp_codebase/test.java", "issues": [{"type": "lint", "message": "NoPackage"}]},
        {"file": "temp_codebase/test.js", "issues": [{"type": "lint", "message": "Test issue"}]}
    ]
    
    output_dir = tmp_path / "output"
    generator.generate_output(codebase, issues, str(output_dir))
    
    assert os.path.exists(output_dir / "report.html")
    assert os.path.exists(output_dir / "report.md")
    
    with open(output_dir / "report.html", encoding='utf-8') as f:
        content = f.read()
        assert "test.py" in content
        assert "test.java" in content
        assert "test.js" in content
        assert "Added docstrings" in content
        assert "Added Javadoc" in content
        assert "Added JSDoc" in content