#!/bin/bash
#
# Script to convert text files from CRLF to LF.
#

ROOT_DIR=$(dirname $(dirname $(realpath "$0")))/../../

find $ROOT_DIR -type f -not -path "*/.git/*" -not -path "*/.git" -not -path "*/.venv/*" -exec dos2unix -q {} \;
