#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)

import os
import git
import yaml
from pathlib import Path

REDIRECT_URL = 'https://github.com/mitre/'
PLUGINS_DIR = '../plugins/'
CONF_DIR = '../conf/'
LOCAL_YML = 'local.yml'
CALDERA_PATH = '/path/to/your/caldera/installation'  # Update this path to your actual CALDERA installation path

def clone_repo(repo_url, local_dir):
    if Path(local_dir).exists():
        g = git.cmd.Git(local_dir)
        g.pull()
    else:
        git.Repo.clone_from(repo_url, local_dir)

def generate_local_yml():
    local_yml_path = os.path.join(CONF_DIR, LOCAL_YML)
    caldera_local_yml_path = os.path.join(CALDERA_PATH, CONF_DIR, LOCAL_YML)
    if not os.path.exists(local_yml_path):
        if os.path.exists(caldera_local_yml_path):
            os.system(f'cp {caldera_local_yml_path} {local_yml_path}')
        else:
            with open(local_yml_path, 'w') as f:
                yaml.dump({'plugins': []}, f)

    with open(local_yml_path, 'r') as f:
        local_yml = yaml.safe_load(f)

    plugins = [p.name for p in Path(PLUGINS_DIR).iterdir() if p.is_dir()]
    local_yml['plugins'] = plugins

    with open(local_yml_path, 'w') as f:
        yaml.dump(local_yml, f)

def main():
    for plugin in os.listdir(PLUGINS_DIR):
        clone_repo(REDIRECT_URL + plugin, os.path.join(PLUGINS_DIR, plugin))

    if input('Do you want to generate a local.yml file and activate all plugins? (y/n): ') == 'y':
        generate_local_yml()

if __name__ == "__main__":
    main()

