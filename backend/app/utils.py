import os
import zipfile
import git
import shutil
import magic

def process_input(input_path, temp_dir="input"):
    """Handle input codebases (ZIP, Git, folder)."""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    if input_path.endswith(".zip"):
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        return temp_dir
    
    if input_path.startswith("http") or input_path.startswith("git@"):
        repo_name = input_path.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(temp_dir, repo_name)
        git.Repo.clone_from(input_path, repo_path)
        return repo_path
    
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
            if file_type.startswith("text/x-python"):
                file_types[file_path] = "python"
            elif file_type in ["text/javascript", "application/javascript"]:
                file_types[file_path] = "javascript"
            else:
                file_types[file_path] = "unsupported"
    return file_types

def detect_project_structure(directory):
    """Identify project structure, dependencies, and configurations."""
    structure = {"files": [], "dependencies": {}, "build_config": None}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            structure["files"].append(file_path)
            if file == "requirements.txt":
                with open(file_path, 'r') as f:
                    structure["dependencies"]["python"] = f.read().splitlines()
            elif file == "package.json":
                with open(file_path, 'r') as f:
                    structure["dependencies"]["javascript"] = f.read()
            elif file in ["pyproject.toml", "package.json"]:
                structure["build_config"] = file
    return structure
