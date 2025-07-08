import os
import sys

script_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)

class FileChecker:
    """
    A class to check if .tif files have matching .json files in a given folder and vice versa.
    """

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.OUTPUT_FILE = os.path.join(folder, f"{os.path.basename(os.path.normpath(folder_path))}.txt")

    def check_matching_files(self):
        tif_files = {os.path.splitext(f)[0] for f in os.listdir(self.folder_path) if f.lower().endswith('.tif')}
        json_files = {os.path.splitext(f)[0] for f in os.listdir(self.folder_path) if f.lower().endswith('.json')}

        missing_json = tif_files - json_files
        missing_tif = json_files - tif_files

        if not missing_json and not missing_tif:
            with open(self.OUTPUT_FILE, 'a') as f:
                f.write(f"All .tif files have matching .json files in {self.folder_path}\n")
            return False
        else:
            if missing_json:
                with open(self.OUTPUT_FILE, 'a') as f:
                    f.write(f"Missing .json files in {self.folder_path}:\n")
                    for name in sorted(missing_json):
                        f.write(f"{name}\n")
            if missing_tif:
                with open(self.OUTPUT_FILE, 'a') as f:
                    f.write(f"Missing .tif files in {self.folder_path}:\n")
                    for name in sorted(missing_tif):
                        f.write(f"{name}\n")
            return True