#!/usr/bin/env python3

import argparse
import os
import tempfile
import shutil
import subprocess

from pathlib import Path

from lxml import etree
from pathvalidate import sanitize_filename
from pathvalidate import sanitize_filepath


def split_ctd_recursively(current_node, parent_path, indent=0):
    child_nodes = current_node.xpath('node')

    if len(child_nodes) > 0:
        try:
            node_name = sanitize_filepath(str(current_node.xpath('@name')[0]))
            parent_path = Path(parent_path, node_name)
        except:
            pass
    else:
        current_filename = os.path.join(parent_path, sanitize_filename(str(current_node.xpath('@name')[0])) + '.ctd')
        if args.verbose:
            print("[*] Creating file " + current_filename  + " ...")
        current_file_content = etree.tostring(current_node).decode()
        os.makedirs(os.path.dirname(current_filename), exist_ok=True)
        with open(current_filename, "w") as f:
            f.write(current_file_content)

    for node in child_nodes:
        indent += 1
        split_ctd_recursively(node, parent_path, indent)
        indent -= 1


def convert_ctd_files_to_md(input_path):
    ctd_files = Path(input_path).glob('**/*.ctd')
    for ctd_file in ctd_files:
        current_parent_dir = os.path.dirname(ctd_file)
        current_basename = os.path.basename(ctd_file)
        with tempfile.TemporaryDirectory() as tempdir_path:
            if args.verbose:
                print("[*] Attempting conversion of " + str(ctd_file) + " ...")

            # Convert to Markdown using <https://gitlab.com/kibley/cherrytreetomarkdown>
            subprocess.call(["php", "cherrytomd.php", Path(ctd_file), Path(tempdir_path)])

            # Copy the generated files and folders to the same location as the individual CherryTree files
            shutil.copy(Path(tempdir_path, "index.md"), Path(current_parent_dir, current_basename.replace('.ctd', '.md')))
            shutil.copytree(Path(tempdir_path, "files"), Path(current_parent_dir, "_attachments/files/"), dirs_exist_ok=True) 
            shutil.copytree(Path(tempdir_path, "images"), Path(current_parent_dir, "_attachments/images/"), dirs_exist_ok=True) 

            if args.verbose:
                print("[*] Conversion of " + str(ctd_file) + " finished!")

            if not args.keep:
                if args.verbose:
                    print("[*] Deleting original file " + str(ctd_file) + " ...")
                os.remove(ctd_file)
                

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
arg_parser.add_argument("-i", "--input", help="A single CherryTree input file in *.ctd format", required=True)
arg_parser.add_argument("-o", "--output", help="Output directory to write split files to (defaults to current directory)", default=Path("./"))
arg_parser.add_argument("-k", "--keep", help="Keeps all of the individual CherryTree node files instead of deleting them after conversion to Markdown", action="store_true")

args = arg_parser.parse_args()

print("[*] Starting node to individual file conversion.")
root = etree.parse(Path(args.input))
split_ctd_recursively(root, parent_path=Path(args.output))
print("[*] Node to file conversion: All done.")

print("[*] Starting XML to Markdown conversion.")
convert_ctd_files_to_md(Path(args.output))
print("[*] XML to Markdown conversion: All done.")

print("[*] Fixing image and file paths ...")
os.system("find . -type f -name '*.md' -exec sed -i 's|(./images/|(./_attachments/images/|g' {} +")
os.system("find . -type f -name '*.md' -exec sed -i 's|(./files/|(./_attachments/files/|g' {} +")
print("[*] Fixed image and file paths!")
