# mdwatermark

Small utility to convert Markdown files in doc/ to PDFs and apply a centered watermark.

## Project layout

- [doc/fse.md](doc/fse.md) — source Markdown files.
- [generated-pdfs/fse.pdf](generated-pdfs/fse.pdf) — output PDFs.
- [requirements.txt](requirements.txt) — Python dependencies.
- [scripts/generate_pdfs.py](scripts/generate_pdfs.py) — orchestrates conversion and watermarking. See [`convert_md_to_pdf`](scripts/generate_pdfs.py) and [`main`](scripts/generate_pdfs.py).
- [scripts/watermark.py](scripts/watermark.py) — creates and merges a centered watermark. See [`add_watermark_to_pdf`](scripts/watermark.py).
- [scripts/detect_changed_files.py](scripts/detect_changed_files.py) — selects which .md files to process. See [`get_changed_files`](scripts/detect_changed_files.py) and [`get_all_files`](scripts/detect_changed_files.py).
- [scripts/__init__.py](scripts/__init__.py) — package marker.
- [.github/workflows/pdf-generator.yml](.github/workflows/pdf-generator.yml) — CI workflow that runs the generator on push or manual dispatch.

## Features

- Convert Markdown -> PDF using Pandoc/XeLaTeX (`scripts/generate_pdfs.py`).
- Add a single centered semi-transparent watermark (`scripts/watermark.py`).
- GitHub Actions integration to auto-generate and commit PDFs ([.github/workflows/pdf-generator.yml](.github/workflows/pdf-generator.yml)).

## Requirements

- System:
  - pandoc
  - TeX engine with xelatex (e.g., texlive-xetex)
- Python 3.8+
- Python packages: see [requirements.txt](requirements.txt)
  - PyPDF2
  - reportlab
  - Pillow
  - charset-normalizer

## Local usage

1. Install system deps (example for Ubuntu):
```sh
sudo apt-get update
sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended
```
