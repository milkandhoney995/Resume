#!/bin/bash
set -e

python3 cover_generate.py

pandoc cover_letter_en.md \
  --reference-doc=cover_template_en.docx \
  -o Cover_Letter.docx