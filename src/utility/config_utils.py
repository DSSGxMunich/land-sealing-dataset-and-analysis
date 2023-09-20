import os
import yaml

def get_project_root_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_source_path():
    return os.path.join(get_project_root_path(), "src")

def get_config_path():
    return os.path.join(get_project_root_path(), "config")

def get_data_path():
    return os.path.join(get_project_root_path(), "data")

def read_yaml(path):
    with open(path, 'r',encoding='utf8') as f:
        config = yaml.safe_load(f)
    return config