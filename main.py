import os
from dotenv import load_dotenv
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_DATA = os.getenv("PAST_DATA")

import pytesseract as ocr
from PIL import Image, ImageDraw


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


fi = filters()

name_image = "qr_1.jpeg"

# Colocando os canais em ordem RGB
image_ocr = cv2.imread(PAST_DATA + "Test/" + name_image)
h, w, d = image_ocr.shape
image_ocr = cv2.resize(
    image_ocr, (2 * int(w), 2 * int(h)), interpolation=cv2.INTER_CUBIC
)
# image_ocr = Image.open(PAST_DATA + "Test/" + name_image)
# print(type(image_ocr))

# image_ocr = fi.dim_ruido(image_ocr)
image_ocr = cv2.cvtColor(image_ocr, cv2.COLOR_BGR2GRAY)

# (thresh, image_ocr) = cv2.threshold(image_ocr, 180, 255, cv2.THRESH_BINARY)
print(param_tresh(image_ocr))
image_ocr = fi.threshold(image_ocr, param_tresh(image_ocr))

# image_ocr = cv2.GaussianBlur(image_ocr, (21, 21), 0)
# image_ocr = cv2.medianBlur(image_ocr, 3)
image_ocr = cv2.bilateralFilter(image_ocr, 20, 100, 30)
dd = -1
kernel = np.array([[0, dd, 0], [dd, 5, dd], [0, dd, 0]])
#image_ocr = cv2.filter2D(src=image_ocr, ddepth=-1, kernel=kernel)

# image_ocr = fi.get_grayscale(image_ocr)
# image_ocr = np.where(image_ocr < 190, 0, 250)


# image_ocr = fi.remove_noise(image_ocr)

# image_ocr = fi.canny(image_ocr)
# image_ocr = fi.dilate(image_ocr)
# image_ocr = fi.erode(image_ocr)
# image_ocr = fi.opening(image_ocr)

# Reconvertendo a imagem em um tipo Image.PIL
# detector = cv2.QRCodeDetector()
# data, bbox, straight_qrcode = detector.detectAndDecode(image_ocr)

image_ocr = Image.fromarray(image_ocr).convert('RGB')

barcode = pyzbar.decode(image_ocr, symbols=[ZBarSymbol.QRCODE])
barcodeData = barcode[0].data
# barcodeType = barcode.type
print(str(barcodeData), barcode)

draw = ImageDraw.Draw(image_ocr)
for barcode in pyzbar.decode(image_ocr):
    rect = barcode.rect
    draw.rectangle(
        (
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top + rect.height)
        ),
        outline=(255, 0, 0),
        width=10
    )

    #draw.polygon(barcode.polygon, outline=(135, 206, 235))


#image_ocr.show()
image_ocr.save(PAST_DATA + f"cache/c_{name_image}_qrcode.jpg")


# phrase = ocr.image_to_string(image_ocr, lang="por")
# print(phrase)

# s-------------------------------------
# Mediana, sobel, blur --> sharpein