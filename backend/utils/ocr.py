import fitz

def extract_content_fitz(pdf_data: bytes):
    text = ""
    ocr_res = []
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text()
        text = "\n".join(line for line in text.split("\n") if line.strip())
    pdf_document.close()
    return ocr_res, text