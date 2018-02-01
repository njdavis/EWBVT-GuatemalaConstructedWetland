#!/bin/bash

#compiling 
echo "Compiling and running main.py"
#python3 ../code/main.py

echo "Assembling markdown file"
#pip3 install filter_pandoc_run_py

pandoc markdownWetlandNotes.txt --lua-filter insertCode.lua --filter pandoc-fignos --filter pandoc-tablenos  -o wetlandNotes.pdf

cp wetlandNotes.pdf ~/"Google Drive File Stream"/"My Drive/EWB VT"/"Project Folders"/"Guatemala Group"/"Wastewater Phase 3 (Implementation Trip)"/"Constructed Wetland"


