#!/usr/bin/python3
import os
import sys
from dirsync import sync
from shutil import copyfile
import argparse
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--sync', '-s', action="store_true", help='[DANGEROUS] Copy the files from the REPO to the mod folder')

args = parser.parse_args()

CRUSADER_KINGS_3_MOD_DIR = "CRUSADER_KINGS_3_MOD_DIR"
CRUSADER_KINGS_3_REPO_DIR = "CRUSADER_KINGS_3_REPO_DIR"

mod_directory_str = os.environ.get(CRUSADER_KINGS_3_MOD_DIR, '').replace("'", "")
repo_directory_str = os.environ.get(CRUSADER_KINGS_3_REPO_DIR, '').replace("'", "")

modlist = Path(f"{repo_directory_str}/modlist")
mods = modlist.read_text().split('\n')

mods = [m for m in mods if m.strip()]

for m in mods:
    from_path = Path(f"{mod_directory_str}/{m}")
    to_path = Path(f"{repo_directory_str}/mods/{m}")
    if args.sync:
        (from_path, to_path) = (to_path, from_path)
    logging.info(f"from '{from_path}' to '{to_path}'")
    sync(from_path, to_path, "sync", create=True)
