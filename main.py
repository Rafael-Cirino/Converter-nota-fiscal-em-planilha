import os
from dotenv import load_dotenv

load_dotenv()

import pytesseract as ocr
from PIL import Image


from filters import filters
fi = filters()

PATH_TESSERACT = os.getenv('PATH_TESSERACT')
PAST_TEST = os.getenv('PAST_TEST')
ocr.pytesseract.tesseract_cmd = PATH_TESSERACT

# Colocando os canais em ordem RGB
image_ocr = Image.open(PAST_TEST + 'nota-fiscal_dedo.jpg').convert('RGB')

image_ocr = fi.dim_ruido(image_ocr)
image_ocr = fi.trunc_bin(image_ocr)

#Reconvertendo a imagem em um tipo Image.PIL
image_ocr = Image.fromarray(image_ocr) 
image_ocr.show()
phrase = ocr.image_to_string(image_ocr, lang='por')
print(phrase)
print("fim")