# PDF Outline Updater

## Description

This Python script updates the outline (table of contents) of a PDF file based on the size of headers. It identifies text that resembles H1, H2, and H3 headers based on font size, and creates a structured outline for the PDF. The script also has the capability to merge lines that follow a specific numbering format (e.g., "1.", "1.1", "1.1.1") with their subsequent lines, provided they share the same font size.

## Requirements

- Python 3.x
- PyMuPDF (fitz) library

## Installation

Before running the script, ensure you have Python installed on your system. You can then install the required PyMuPDF library using pip:

```shell
pip install PyMuPDF
```

## Usage
```shell
python toc.py -h                   
usage: toc.py [-h] pdf_file

Update PDF outline based on header sizes.

positional arguments:
  pdf_file    The path to the PDF file to be processed

options:
  -h, --help  show this help message and exit
```

Run the script from the command line, passing the path to the PDF file as an argument:

```shell
python toc.py path/to/your/file.pdf
```


## How it Works

- The script reads the PDF and analyzes the font sizes of different text spans.
- It identifies headers based on predefined size thresholds for H1, H2, and H3 headers.
- If a line with a specific numbering format is detected and its font size matches the following line, these lines are merged.
- The script then creates a new outline based on these headers and writes it back into the PDF.
- The updated PDF is saved under a new file name, prefixed with "updated_".

## Customization

You can adjust the size thresholds for H1, H2, and H3 in the script according to your specific PDF file's formatting.

## Author

[bluegitter](https://github.com/bluegitter)
