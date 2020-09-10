#!/usr/bin/python3
import os
import sys
from shutil import copyfile
import argparse
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO)

NUMBERED_FILENAME_SPLIT_CHARACTER = "_"

parser = argparse.ArgumentParser(description='')
parser.add_argument('filepath', help='')
parser.add_argument('--force', '-f', action="store_true", help='Override any existing files')
parser.add_argument('--increment', '-i', action="store_true", help='Increment the version number on the file so 00_X.txt will be copied as 01_X.txt')

args = parser.parse_args()

CRUSADER_KINGS_3_CURRENT_MOD_NAME = "CRUSADER_KINGS_3_CURRENT_MOD_NAME"
CRUSADER_KINGS_3_MAIN_DIR = "CRUSADER_KINGS_3_MAIN_DIR"
CRUSADER_KINGS_3_MOD_DIR = "CRUSADER_KINGS_3_MOD_DIR"

mod_name = os.environ.get(CRUSADER_KINGS_3_CURRENT_MOD_NAME, '')
main_directory_str = os.environ.get(CRUSADER_KINGS_3_MAIN_DIR, '').replace("'", "")
base_mod_directory_str = os.environ.get(CRUSADER_KINGS_3_MOD_DIR, '').replace("'", "")

if not mod_name:
    logging.error(f"The {CRUSADER_KINGS_3_CURRENT_MOD_NAME} environment variable must be set")
    sys.exit(1)

if not main_directory_str:
    logging.error(f"The {CRUSADER_KINGS_3_MAIN_DIR} environment variable must be set")
    sys.exit(1)

if not base_mod_directory_str:
    logging.error(f"The {CRUSADER_KINGS_3_MOD_DIR} environment variable must be set")
    sys.exit(1)


main_path = Path(main_directory_str)
if not main_path.exists() or not main_path.is_dir():
    logging.error(f"Please ensure that {main_directory_str} points to a valid directory")
    sys.exit(1)

base_mod_path = Path(base_mod_directory_str)
if not base_mod_path.exists() or not base_mod_path.is_dir():
    logging.error(f"Please ensure that {base_mod_directory_str} points to a valid directory")
    sys.exit(1)

mod_directory_str = f"{base_mod_directory_str}/{mod_name}"

mod_path = Path(mod_directory_str)
if not mod_path.exists() or not mod_path.is_dir():
    logging.error(f"Please ensure that {mod_directory_str} points to a valid directory")
    sys.exit(1)


filepath_str = f"{main_directory_str}/{args.filepath}"
filepath_path = Path(filepath_str)
if not filepath_path.exists() or not filepath_path.is_file():
    logging.error(f"Please ensure that {filepath_str} points to an existing file")
    sys.exit(1)

# add param --inc to increment the number starting in front of the file
destination_filepath = args.filepath
if args.increment:
    filepath = Path(args.filepath)
    if NUMBERED_FILENAME_SPLIT_CHARACTER in filepath.name:
        (n, tail) = filepath.name.split(NUMBERED_FILENAME_SPLIT_CHARACTER, 1)
        n = str(int(n) + 1).zfill(len(n))
        destination_filepath = str(filepath.parents[0]) + f"/{n}_{tail}"

destination_filepath_str = f"{mod_directory_str}/{destination_filepath}"
destination_filepath_path = Path(destination_filepath_str)
if destination_filepath_path.exists() and not args.force:
    logging.error(f"File exists at {destination_filepath_str} already, please use the --force/-f parameter if you want to write over it")
    sys.exit(1)

destination_filepath_path.parents[0].mkdir(parents=True, exist_ok=True)
destination_filepath_path.touch(exist_ok=True)
destination_filepath_path.write_text(filepath_path.read_text())
logging.info(f"Created at {destination_filepath_path}")
