"""
Script to generate class diagrams of all packages in plantuml (.puml) format.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

ROOTPATH: Path = Path(__file__).absolute().parents[3]
DOCSPATH: Path = ROOTPATH / "docs" / "architecture"


def parse_args() -> argparse.Namespace:
    """Parse the script arguments."""
    args = None if sys.argv[1:] else ["-h"]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directory",
        type=Path,
        required=True,
        dest="path",
        help="directory with Python source code"
    )
    return parser.parse_args(args)


def run_cmd(cmd: str) -> subprocess.CompletedProcess:
    """Launch the specified command in specific wrapping."""
    return subprocess.run(cmd, shell=True, check=True)


def clean_dir() -> None:
    """Create a clean docs directory."""
    shutil.rmtree(DOCSPATH, ignore_errors=True)
    os.makedirs(DOCSPATH)


def generate_docs(path: Path) -> None:
    """Generate .puml files."""
    for elem in os.listdir(path):
        full_path = path / elem
        if full_path.is_dir() and "__init__.py" in os.listdir(full_path):
            package_docs_path = DOCSPATH / elem
            os.makedirs(package_docs_path, exist_ok=True)
            run_cmd(f"pyreverse {path / elem} -o puml -d {package_docs_path}")
            # edit "class" into "interface" for interfaces
            if elem == "interfaces":
                data = ""
                with open(package_docs_path / "classes.puml", "r") as f:
                    data = f.read()
                data = data.replace("class ", "interface ")
                with open(package_docs_path / "classes.puml", "w") as f:
                    f.write(data)


def main(args: argparse.Namespace) -> None:
    clean_dir()
    generate_docs(args.path.absolute())


if __name__ == "__main__":
    main()
