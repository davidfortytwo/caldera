#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)

import os
import sys
import yaml
import readchar
import logging
from pathlib import Path
from secrets import token_hex
import readchar

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_default_yml():
    logger.debug("Searching for default.yml file")
    for root, dirs, files in os.walk("/"):
        if "default.yml" in files:
            logger.debug(f"Found default.yml at {root}")
            return os.path.join(root, "default.yml")
    return None

def copy_file_to_exec_dir(filepath):
    exec_dir = Path(__file__).parent.absolute()
    logger.debug(f"Copying file to {exec_dir}")
    os.system(f"cp {filepath} {exec_dir}")

def generate_random_key(bit_length, debug=False):
    key = secrets.token_urlsafe(bit_length // 8)  # 8 bits per byte
    if debug:
        print(f"Generated {bit_length}-bit key: {key}")
    return key    

def modify_yml(filepath):
    with open(filepath, 'r') as f:
        doc = yaml.safe_load(f)

    logger.debug("Modifying YAML file")
    doc["users"]["admin"]["admin"] = "# Commented out"
    doc["users"]["red"]["admin"] = generate_random_key(64, debug)

    with open(filepath, 'w') as f:
        yaml.safe_dump(doc, f)

def handle_auto_mode():
    logger.info("Running in auto mode")
    filepath = find_default_yml()
    if filepath is None:
        logger.error("default.yml file not found")
        sys.exit(1)
    copy_file_to_exec_dir(filepath)
    modify_yml(filepath)

def handle_manual_mode():
    filepath = input("Enter the path of the default.yml file: ")
    if not os.path.exists(filepath):
        logger.error("File does not exist")
        sys.exit(1)
    copy_file_to_exec_dir(filepath)
    modify_yml(filepath)

def main():
    print("Press 'A' for auto mode, 'M' for manual mode, or 'E' to exit.")
    mode = readchar.readchar().lower()

    if mode == 'a':
        handle_auto_mode()
    elif mode == 'm':
        handle_manual_mode()
    elif mode == 'e':
        logger.info("Exiting script")
        sys.exit(0)
    else:
        print("Invalid input. Please press 'A', 'M', or 'E'.")

if __name__ == "__main__":
    main()

