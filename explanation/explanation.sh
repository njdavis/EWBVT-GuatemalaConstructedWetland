#!/bin/bash


#compiling 
echo "Compiling and running main.py"
#python3 ../code/main.py

echo "Assembling markdown file"
#pip3 install filter_pandoc_run_py

pandoc markdownWetlandNotes.txt  --from markdown+raw_tex+escaped_line_breaks --variable documentclass=article  --lua-filter insertCode.lua --filter pandoc-fignos --filter pandoc-tablenos  --filter pandoc-eqnos -o wetlandNotes.pdf

cp wetlandNotes.pdf ~/"Google Drive File Stream"/"My Drive/EWB VT"/"Project Folders"/"Guatemala Group"/"Wastewater Phase 3 (Current Design Work)"/"Project Packet Info"

