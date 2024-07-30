from modules import utils

import subprocess
import shutil
import pathlib
import json

webcrack_path = shutil.which("webcrack")
if not webcrack_path:
    raise FileNotFoundError("Webcrack is not installed, or it is not in your PATH.")

# Call webcrack to deobfuscate a js file
def process_file(js_string):
    child = subprocess.Popen([webcrack_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = child.communicate(input=js_string.encode())
    return out[0].decode()

def unbundle_file(js_string, out_dir):
    child = subprocess.Popen([webcrack_path, "-o", str(out_dir)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    child.communicate(input=js_string.encode())
    return

# Recursively deobfuscate a directory
# This will overwrite the files that are processed
def process_directory(dir_path, unbundle=False):
    path = pathlib.Path(dir_path)
    items = []
    for item in path.rglob("*"):
        items.append(item)
    
    for item in items:
        if not item.is_file():
            continue
        if item.suffix == ".json":
            utils.logger.debug(f"Formatting JSON: {item}")
            try:
                json_string = item.read_text(encoding='utf-8')
                json_pretty = json.dumps(json.loads(json_string), indent=2, sort_keys=True)
                item.write_text(json_pretty, encoding='utf-8')
            except Exception as e:
                utils.logger.error(f"Error formatting JSON {item}: {e}")
            continue
        if not item.suffix == ".js":
            continue

        utils.logger.debug(f"Deobfuscating JS: {item}")
        try:
            js_string = item.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            utils.logger.error(f"UnicodeDecodeError reading {item}: {e}")
            continue

        if unbundle:
            item.unlink()
            unbundle_file(js_string, item)
            continue

        processed_string = process_file(js_string)
        try:
            item.write_text(processed_string, encoding='utf-8')
        except Exception as e:
            utils.logger.error(f"Error writing processed JS {item}: {e}")