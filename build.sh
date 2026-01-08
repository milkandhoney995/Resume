#!/bin/bash
python3 generate.py
pandoc resume.md \
  --reference-doc=template.docx \
  -o 職務経歴書.docx