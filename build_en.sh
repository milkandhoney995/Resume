#!/bin/bash
set -e
python3 generate.py en
pandoc resume_en.md \
  --reference-doc=template_en.docx \
  --lua-filter=table_style.lua \
  --lua-filter=pagebreak_by_company.lua \
  -o CV.docx
python3 postprocess.py en