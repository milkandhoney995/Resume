#!/bin/bash
set -e

python3 cover_generate.py

pandoc cover_letter.md \
  --reference-doc=templates/cover_template.docx \
  -o Cover_Letter.docx