#!/bin/bash
#
# Script to extract version number of the Python project.
# sh version of get_version.py, usually for cases when Python interpreter is unavailable.
#

ROOT_DIR=$(dirname $(dirname $(realpath "$0")))/../../../

cat "$ROOT_DIR"/pyproject.toml | grep "version = " | cut -d'"' -f 2
