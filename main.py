import os
from dotenv import load_dotenv

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_DATA = os.getenv("PAST_DATA")

import pytesseract as ocr
from PIL import Image


ocr.pytesseract.tesseract_cmd = PATH_TESSERACT  # Defini o caminho para Tesseract

from filters import filters
import numpy as np
import cv2


def param_tresh(array):
    desvio = np.std(array)
    mediana = np.median(array)
    media = np.average(array)

    print(mediana, media, desvio)
    if mediana < 127:
        return int(media)

    return int(media)


def filter_qrcode(name_image):
    fi = filters()

    image_ocr = cv2.imread(PAST_DATA + "my/" + name_image)
    h, w = image_ocr.shape
    image_ocr = cv2.resize(
        image_ocr, (2 * int(w), 2 * int(h)), interpolation=cv2.INTER_CUBIC
    )

    image_ocr = cv2.cvtColor(image_ocr, cv2.COLOR_BGR2GRAY)

    image_ocr = fi.threshold(image_ocr, param_tresh(image_ocr))

    image_ocr = cv2.bilateralFilter(image_ocr, 20, 100, 30)
    dd = -1
    kernel = np.array([[0, dd, 0], [dd, 5, dd], [0, dd, 0]])
    image_ocr = cv2.filter2D(src=image_ocr, ddepth=-1, kernel=kernel)

    image_ocr = Image.fromarray(image_ocr).convert("RGB")


def image_save(image_save, name_image):
    image_save.save(PAST_DATA + f"cache/c_{name_image}_qrcode.jpg")


if __name__ == "__main__":
    name_image = "n (5).jpg"

# s-------------------------------------
# Mediana, sobel, blur --> sharpein