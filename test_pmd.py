import subprocess

result = subprocess.run(
    ['pmd', '-d', 'sample_codebase/test.java', '-f', 'text', '-R', 'rulesets/java/quickstart.xml'],
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)
