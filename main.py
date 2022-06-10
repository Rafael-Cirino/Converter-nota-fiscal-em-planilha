import os
from dotenv import load_dotenv

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_DATA = os.getenv("PAST_DATA")

import pytesseract as ocr
from PIL import Image

ocr.pytesseract.tesseract_cmd = PATH_TESSERACT  # Defini o caminho para Tesseract

from filters import filters
from qr_code import *
import cv2

def files_in_folder(path_folder):
    caminhos = [os.path.join(path_folder, nome) for nome in os.listdir(path_folder)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]

    print(arquivos)
    return arquivos

def filter_qrcode(name_image):
    fi = filters()

    image_ocr = cv2.imread(PAST_DATA + name_image)
    h, w, d = image_ocr.shape
    image_ocr = cv2.resize(
        image_ocr, (2 * int(w), 2 * int(h)), interpolation=cv2.INTER_CUBIC
    )

    param_image = fi.param_tresh(image_ocr)
    kernel_value = fi.kernel()
    list_filter = [
        cv2.cvtColor(image_ocr, cv2.COLOR_BGR2GRAY),
        fi.threshold(image_ocr, param_image),
        cv2.bilateralFilter(image_ocr, 20, 100, 30),
        cv2.filter2D(src=image_ocr, ddepth=-1, kernel=kernel_value),
    ]

    for filtered in list_filter:
        image_ocr = filtered

        image_qrcode = Image.fromarray(image_ocr).convert("RGB")
        link_invoice, data_qrcode = recognize_qrcode(image_qrcode)
        if link_invoice:
            break

    image_qrcode = draw_qrcode(image_qrcode, data_qrcode)
    image_save(image_qrcode, "test21")


def image_save(image_save, name_image):
    image_save.save(PAST_DATA + f"cache/c_{name_image}_qrcode.jpg")


if __name__ == "__main__":
    name_image = "n_4.jpg"

    #filter_qrcode("Test/" + name_image)

    files_in_folder(PAST_DATA + "Test/")

# s-------------------------------------
# Mediana, sobel, blur --> sharpein

"""
    image_ocr = cv2.cvtColor(image_ocr, cv2.COLOR_BGR2GRAY)

    image_ocr = fi.threshold(image_ocr, param_tresh(image_ocr))

    image_ocr = cv2.bilateralFilter(image_ocr, 20, 100, 30)
    dd = -1
    kernel = np.array([[0, dd, 0], [dd, 5, dd], [0, dd, 0]])
    image_ocr = cv2.filter2D(src=image_ocr, ddepth=-1, kernel=kernel)

    image_ocr = Image.fromarray(image_ocr).convert("RGB")
"""