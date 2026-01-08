#!/bin/bash
python3 generate.py
pandoc resume.md \
  --reference-doc=template.docx \
  --lua-filter=table_style.lua \
  --lua-filter=pagebreak_by_company.lua \
  -o 職務経歴書.docx