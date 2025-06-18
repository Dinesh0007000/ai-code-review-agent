import json
import os

class ConfigManager:
    def __init__(self, config_path='configs/default_config.json'):
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "supported_languages": ["python", "java", "javascript"],
            "exclude_paths": ["__pycache__", ".git", "node_modules", "venv"],
            "analysis_tools": {
                "python": ["flake8", "bandit"],
                "java": ["pmd"],
                "javascript": ["eslint"]
            }
        }

    def get_supported_languages(self):
        return self.config.get("supported_languages", ["python", "java", "javascript"])

    def get_exclude_paths(self):
        return self.config.get("exclude_paths", [])

    def get_analysis_tools(self, language):
        return self.config.get("analysis_tools", {}).get(language, [])