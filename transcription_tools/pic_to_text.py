from PIL import Image
import pytesseract
import argparse

# install tesseract-ocr
# uses Tesseract and a python wrapper

# TIPS FOR BETTER RESULTS
# Preprocess the image by converting to grayscale or thresholding for cleaner OCR
# Use image_to_data() or image_to_boxes() for structured output (like bounding boxes)
# Tesseract supports languages like:
# pytesseract.image_to_string(image, lang='eng+fra')
# Use pdf2image or PyMuPDF to convert pages to images, then OCR.



# Import file from CLI
parser = argparse.ArgumentParser()
parser.add_argument("graphical_file", help = "Upload graphical file")
args = parser.parse_args()

# Load the image
image = Image.open(args.graphical_file)

# Extract Text
text = pytesseract.image_to_string(image)

# Save
with open("ocr_output.txt", "w", encoding="utf-8") as f:
  f.write(text)