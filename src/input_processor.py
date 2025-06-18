import os
import zipfile
import shutil
import git
import json
from utils.language_parser import LanguageParser

class InputProcessor:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.language_parser = LanguageParser()

    def process_input(self, input_path, temp_dir="temp_codebase"):
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        if input_path.endswith('.zip'):
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        elif os.path.isdir(input_path):
            shutil.copytree(input_path, temp_dir, dirs_exist_ok=True)
        elif input_path.startswith('git@') or input_path.startswith('https://'):
            git.Repo.clone_from(input_path, temp_dir)
        else:
            raise ValueError("Unsupported input format")

        return self.categorize_files(temp_dir)

    def categorize_files(self, temp_dir):
        codebase_structure = {"files": [], "dependencies": {}, "structure": {}}
        exclude_paths = self.config_manager.get_exclude_paths()

        for root, _, files in os.walk(temp_dir):
            if any(exclude_path in root for exclude_path in exclude_paths):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                language = self.language_parser.detect_language(file_path)
                if language in self.config_manager.get_supported_languages():
                    codebase_structure["files"].append({
                        "path": file_path,
                        "language": language
                    })
                    if file == "requirements.txt" and language == "python":
                        with open(file_path, 'r') as f:
                            codebase_structure["dependencies"]["python"] = f.read().splitlines()
                    elif file == "pom.xml" and language == "java":
                        codebase_structure["dependencies"]["java"] = "pom.xml detected"
                    elif file == "package.json" and language == "javascript":
                        with open(file_path, 'r') as f:
                            codebase_structure["dependencies"]["javascript"] = json.load(f).get("dependencies", {})
        return codebase_structure