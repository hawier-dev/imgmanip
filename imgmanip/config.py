import os
from multiprocessing import cpu_count
from pathlib import Path
from sys import platform

import yaml

if platform == "linux" or platform == "linux2":
    config_path = str(Path.home()) + '/.local/share/imgmanip'
    config_file_path = config_path + '/config.yaml'
elif platform == "win32":
    config_path = str(Path.home()) + '\\AppData\\Local\\imgmanip'
    config_file_path = config_path + '\\config.yaml'
else:
    config_path = None
    config_file_path = None

default_config = {
    'cpu_count': int(cpu_count() / 2),
}


def write_config(config):
    os.makedirs(config_path, exist_ok=True)
    config_file = open(config_file_path, 'w')
    yaml.dump(config, config_file)


def read_config():
    config_file = open(config_file_path)
    config_data = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    return config_data


if not os.path.exists(config_file_path):
    write_config(default_config)
