import os
import hashlib

from io import BytesIO

PATHS_TO_KEEP = {
    "/etc/passwd": "/var/opt/wd",
    "/etc/sudoers": "/var/opt/ss",
    "/etc/group": "/var/opt/g"
}
FILES_HASHES = {}


def main():
    while True:
        new_files = input("[x] Please enter file to keep and a new path - file_path,new_path:\n[x] Enter 'e' to continue.\n")
        if new_files == "e":
            break
        file, output_file = new_files.split(",")
        PATHS_TO_KEEP[file] = output_file

    handle_files()
    if FILES_HASHES:
        os.environ["base_hashes"] = str(FILES_HASHES) 
        with open("/var/base_hashes", "w") as hashes_file:
            hashes_file.write(str(FILES_HASHES))
        os.environ["base_hashes"] = str(PATHS_TO_KEEP)             
        with open("/var/path_map", "w") as hashes_file:
            hashes_file.write(str(PATHS_TO_KEEP))
    

def calculate_file_hash(file_path: BytesIO):
    with open(file_path, "rb") as file_:
        return hashlib.sha256(file_.read()).hexdigest()


def handle_files():
    for file_path in PATHS_TO_KEEP:
        file_bytes = open(os.path.join(file_path))
        with open(PATHS_TO_KEEP.get(file_path), "w") as output:
            output.write(file_bytes.read())
        file_bytes.close()
        file_sha256 = calculate_file_hash(file_path=file_path)
        FILES_HASHES[file_path] = file_sha256
    return 



if __name__ == "__main__":
    main()