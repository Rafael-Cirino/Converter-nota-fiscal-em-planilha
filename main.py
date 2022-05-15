import os
from dotenv import load_dotenv
from pyzbar import pyzbar

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_DATA = os.getenv("PAST_DATA")

import pytesseract as ocr
from PIL import Image
from PIL import ImageFilter


ocr.pytesseract.tesseract_cmd = PATH_TESSERACT  # Defini o caminho para Tesseract

from filters import filters
import numpy as np
import cv2

def param_tresh(array):
    desvio = np.std(array)
    mediana = np.median(array)
    media = np.average(array)

    if (mediana < 127):
        return int(media + desvio)

    return int(media - desvio)

fi = filters()

name_image = "n_3.png"

# Colocando os canais em ordem RGB
image_ocr = cv2.imread(PAST_DATA + "Test/" + name_image)
h, w, d = image_ocr.shape
image_ocr = cv2.resize(
    image_ocr, (2*int(w), 2*int(h)), interpolation=cv2.INTER_CUBIC
)
# image_ocr = Image.open(PAST_DATA + "Test/" + name_image)
# print(type(image_ocr))

#image_ocr = fi.dim_ruido(image_ocr)
image_ocr = cv2.cvtColor(image_ocr, cv2.COLOR_BGR2GRAY)

#(thresh, image_ocr) = cv2.threshold(image_ocr, 180, 255, cv2.THRESH_BINARY)
print(param_tresh(image_ocr))
image_ocr = fi.threshold(image_ocr, 160)

#image_ocr = cv2.GaussianBlur(image_ocr, (21, 21), 0)
#image_ocr = cv2.medianBlur(image_ocr, 3) 
image_ocr = cv2.bilateralFilter(image_ocr, 10, 200, 30)
dd = -1
kernel = np.array([[0, dd, 0],
                   [dd, 5, dd],
                   [0, dd, 0]])
image_ocr = cv2.filter2D(src=image_ocr, ddepth=-1, kernel=kernel)

image_ocr_a = Image.fromarray(image_ocr)
image_ocr_a.show()
image_ocr_a.save(PAST_DATA + f"cache/c_{name_image}_sharpein.jpg")

# image_ocr = fi.get_grayscale(image_ocr)
#image_ocr = np.where(image_ocr < 190, 0, 250)


# image_ocr = fi.remove_noise(image_ocr)

# image_ocr = fi.canny(image_ocr)
#image_ocr = fi.dilate(image_ocr)
#image_ocr = fi.erode(image_ocr)
#image_ocr = fi.opening(image_ocr)

# Reconvertendo a imagem em um tipo Image.PIL
#detector = cv2.QRCodeDetector()
#data, bbox, straight_qrcode = detector.detectAndDecode(image_ocr)


image_ocr = Image.fromarray(image_ocr)
image_ocr.show()
image_ocr.save(PAST_DATA + f"cache/c_{name_image}_test.jpg")


phrase = ocr.image_to_string(image_ocr, lang="por")
print(phrase)

barcode = pyzbar.decode(image_ocr)
barcodeData = barcode[0].data
#barcodeType = barcode.type

print(str(barcodeData))

# s-------------------------------------
# Mediana, sobel, blur --> sharpein