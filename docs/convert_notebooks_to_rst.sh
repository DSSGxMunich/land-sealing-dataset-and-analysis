#!/bin/bash

# Convert all notebooks to rst files
INPUT_DIR='../src'
OUTPUT_DIR='../docs/source/content/notebooks'

jupyter nbconvert --to rst $INPUT_DIR/*.ipynb --output-dir $OUTPUT_DIR