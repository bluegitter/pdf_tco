import fitz
import re
import argparse


def identify_and_merge_headers(doc, page, size_thresholds):
    """Identify and merge headers based on font size and text format."""
    headers = []
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if 'lines' in b:
            previous_span = None
            for line in b["lines"]:
                for span in line["spans"]:
                    if previous_span and span['size'] == previous_span['size']:
                        # Check if the previous span's text is in a specific format
                        if re.match(r"^\d+(\.\d+)*\.?$", previous_span['text']):
                            if span['size'] <= 12:
                                continue

                            merged_text = previous_span['text'] + \
                                " " + span['text']
                            print(merged_text)
                            # print(merged_text,
                            #       '[', span['size'], span['font'], ']', span)
                            determine_header_level(
                                merged_text, span['size'], page.number, headers, size_thresholds)
                            previous_span = None  # Reset previous span
                            continue

                    previous_span = span
    return headers


def determine_header_level(text, font_size, page_num, headers, size_thresholds):
    """Determine the header level based on font size and add to headers list."""
    if font_size <= 12:
        return

    if font_size >= size_thresholds['H1']:
        headers.append(('H1', text, page_num))
    elif font_size >= size_thresholds['H2']:
        headers.append(('H2', text, page_num))
    elif font_size >= size_thresholds['H3']:
        headers.append(('H3', text, page_num))


def create_outline(headers):
    """Create an outline from identified headers."""
    outline = []
    for level, text, page_num in headers:
        outline.append([1 if level == 'H1' else 2 if level ==
                       'H2' else 3, text, page_num + 1])
    return outline


def update_pdf_outline(pdf_path, size_thresholds):
    doc = fitz.open(pdf_path)
    all_headers = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        headers = identify_and_merge_headers(doc, page, size_thresholds)
        all_headers.extend(headers)

    outline = create_outline(all_headers)
    save_file = "updated_" + pdf_path
    doc.set_toc(outline)
    doc.save("updated_" + pdf_path)
    doc.close()
    # print("\033[92mSuccessfully saved the PDF as:", save_file, "\033[0m")
    print("\033[92mSuccessfully saved the PDF as:\033[0m \033[91m" +
          save_file + "\033[0m")


# Size thresholds for H1, H2, and H3
# Adjust these values based on your PDF
size_thresholds = {'H1': 21, 'H2': 18, 'H3': 15}

parser = argparse.ArgumentParser(
    description='Update PDF outline based on header sizes.')
parser.add_argument('pdf_file', type=str,
                    help='The path to the PDF file to be processed')
args = parser.parse_args()

# Usage
update_pdf_outline(args.pdf_file, size_thresholds)
