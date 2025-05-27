import os
import zipfile
import git
import shutil
import magic
import yaml

def process_input(input_path, temp_dir="input"):
    """Handle input codebases (ZIP, Git, folder)."""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Handle ZIP files
    if input_path.endswith(".zip"):
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        return temp_dir
    
    # Handle Git repositories
    if input_path.startswith("http") or input_path.startswith("git@"):
        repo_name = input_path.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(temp_dir, repo_name)
        git.Repo.clone_from(input_path, repo_path)
        return repo_path
    
    # Handle local folder
    if os.path.isdir(input_path):
        dest_path = os.path.join(temp_dir, os.path.basename(input_path))
        shutil.copytree(input_path, dest_path, dirs_exist_ok=True)
        return dest_path
    
    raise ValueError("Unsupported input format")

def categorize_files(directory):
    """Categorize files by language and functionality."""
    file_types = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            file_types[file_path] = file_type
    return file_types

def detect_project_structure(directory):
    """Identify project structure, dependencies, and configurations."""
    structure = {"files": [], "dependencies": {}, "build_config": None}
    for root, _, files in os.walk(directory):
        for file in files:
            structure["files"].append(os.path.join(root, file))
            if file == "requirements.txt":
                with open(os.path.join(root, file), 'r') as f:
                    structure["dependencies"]["python"] = f.read().splitlines()
            elif file == "pyproject.toml":
                structure["build_config"] = "pyproject.toml"
    return structure