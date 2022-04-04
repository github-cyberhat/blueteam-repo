#Run crontab every 1 minute: */1 * * * * DISPLAY=:0.0 /usr/bin/env python3 /home/ubuntu/checkFileHashes.py


import hashlib
import json
import logging

from datetime import datetime
from io import BytesIO

with open("/var/base_hashes", "r") as base_hashes, open("/var/path_map", "r") as path_map:
    FILES_HASHES = json.loads(base_hashes.read().replace("'", "\""))
    PATHS_MAP = json.loads(path_map.read().replace("'", "\""))


def main():
    for file, copy in PATHS_MAP.items():
        current_file_hash = calculate_file_hash(file)
        if FILES_HASHES.get(file) != current_file_hash:
            with open(copy, "r") as file_copy, open(file, "w") as current_file:
                current_file.write(file_copy.read()) 
                logging.critical(f"[x] {datetime.now()} The hash of '{file}' had changed, reverted to the saved copy file.")


def calculate_file_hash(file_path: BytesIO):
    with open(file_path, "rb") as file_:
        return hashlib.sha256(file_.read()).hexdigest()


if __name__ == "__main__":
    logging.basicConfig(filename='file_changes.log', level=logging.CRITICAL)
    main()
