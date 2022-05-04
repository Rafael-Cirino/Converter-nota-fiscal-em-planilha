import os
from dotenv import load_dotenv

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_TEST = os.getenv("PAST_TEST")

import pytesseract as ocr
from PIL import Image

ocr.pytesseract.tesseract_cmd = PATH_TESSERACT  # Defini o caminho para Tesseract

from filters import filters

fi = filters()

# Colocando os canais em ordem RGB
image_ocr = Image.open(PAST_TEST + "n_5.jpg").convert("RGB")

image_ocr = fi.dim_ruido(image_ocr)

# image_ocr = fi.get_grayscale(image_ocr)
# image_ocr = fi.remove_noise(image_ocr)
image_ocr = fi.trunc_bin(image_ocr)

# image_ocr = fi.canny(image_ocr)
# image_ocr = fi.dilate(image_ocr)
# image_ocr = fi.erode(image_ocr)
# image_ocr = fi.opening(image_ocr)

# Reconvertendo a imagem em um tipo Image.PIL
image_ocr = Image.fromarray(image_ocr)

image_ocr.show()
phrase = ocr.image_to_string(image_ocr, lang="por")
print(phrase)
print("fim")