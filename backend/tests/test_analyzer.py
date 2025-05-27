import pytest
from app.analyzer import analyze_code

def test_analyze_code():
    with open("test.py", "w") as f:
        f.write("def example():\n    print('Hello')")
    report = analyze_code("test.py")
    assert isinstance(report, dict)
    assert "syntax_errors" in report