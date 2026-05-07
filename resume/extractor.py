import os
import pdfplumber
import easyocr

# initialize OCR reader
reader = easyocr.Reader(['en'])


def extract_text_from_pdf(path):

    text = ""

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print("Error reading PDF:", e)

    return text


def extract_text_from_image(path):

    text = ""

    try:
        result = reader.readtext(path)

        for detection in result:
            text += detection[1] + " "

    except Exception as e:
        print("Error reading image:", e)

    return text


def extract_resume_text(path):

    # check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(path)

    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(path)

    else:
        raise ValueError("Unsupported file format")