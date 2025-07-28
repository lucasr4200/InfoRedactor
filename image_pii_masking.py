import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

'''
This is a file for the beginnings of extracting and masking text from images in pdfs.
Currently text is extracted and printed but only the first little chunk. No masking occurs yet.
'''


#Define path to Tesseract
#Might need adjustment depending on install location

pytesseract.pytesseract.tesseract_cmd = 'installation location of tesseract'

def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    pdf_document.close()
    return images

def ocr_images(images):
    text_results = []
    for img in images:
        text = pytesseract.image_to_string(img)
        text_results.append(text)
    return text_results

def main(pdf_path):
    images = extract_images_from_pdf(pdf_path)
    texts = ocr_images(images)
    for i, text in enumerate(texts):
        print(f"Text from image {i + 1}:\n{text}\n")

if __name__ == "__main__":
    pdf_path = 'Document-And-Text-Web-Masking/calgary_sign.pdf'  # Replace with the path to your PDF
    main(pdf_path)