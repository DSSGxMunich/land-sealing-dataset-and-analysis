import os

import yaml


def get_project_root_path():
    """Returns the path to the project root folder"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_source_path():
    """Returns the path to the src folder"""
    return os.path.join(get_project_root_path(), "src")


def get_config_path():
    """Returns the path to the config folder"""
    return os.path.join(get_project_root_path(), "config")


def get_data_path():
    """Returns the path to the data folder"""
    return os.path.join(get_project_root_path(), "data")


def read_yaml(path):
    """Reads a yaml file and returns a dictionary"""
    with open(path, 'r', encoding='utf8') as f:
        config = yaml.safe_load(f)
    return config
