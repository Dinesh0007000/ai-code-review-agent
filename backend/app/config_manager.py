import yaml

def load_config(config_file="config.yaml"):
    """Load configuration settings."""
    default_config = {
        "priorities": ["readability", "security", "performance"],
        "excluded_files": [],
        "style_rules": {"max_line_length": 88},
        "improvement_threshold": 0.5
    }
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            user_config = yaml.safe_load(f)
        default_config.update(user_config)
    
    return default_config

def save_config(config, config_file="config.yaml"):
    """Save configuration settings."""
    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f)