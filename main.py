import os
import time
from dotenv import load_dotenv

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_DATA = os.getenv("PAST_DATA")

import pytesseract as ocr
from PIL import Image

ocr.pytesseract.tesseract_cmd = PATH_TESSERACT  # Defini o caminho para Tesseract

from filters import filters
from qr_code import *
from scraping_html import selenium_open
from py_csv import write_csv
import cv2


def files_in_folder(path_folder):
    caminhos = [os.path.join(path_folder, nome) for nome in os.listdir(path_folder)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]

    # print(arquivos)
    return arquivos


def filter_qrcode(name_image):
    fi = filters()

    image_ocr = cv2.imread(name_image)  # cv2.imread(PAST_DATA + name_image)
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

    for i, filtered in enumerate(list_filter):
        image_ocr = filtered

        image_qrcode = Image.fromarray(image_ocr).convert("RGB")
        link_invoice, data_qrcode = recognize_qrcode(image_qrcode)
        if link_invoice:
            break

    if not (link_invoice):
        return False, i + 1

    # image_qrcode = draw_qrcode(image_qrcode, data_qrcode)
    # image_save(image_qrcode, "test21")

    return link_invoice, i


def image_save(image_save, name_image):
    image_save.save(PAST_DATA + f"cache/c_{name_image}_qrcode.jpg")


if __name__ == "__main__":
    name_image = "qr (2).jpg"
    list_check = []
    list_time = []

    for file in files_in_folder(PAST_DATA + "Dataset/"):
        time_init = time.time()
        link, i = filter_qrcode(file)
        time_end = time.time() - time_init
        print(time_end)

        if link:
            link = link.split("'")[1]
        print(link, i)
        list_check.append(i)
        list_time.append(time_end)
        #break

    print(list_check)
    print("4 ", list_check.count(4))
    print("0 ", list_check.count(0))
    print("1 ", list_check.count(1))
    print("2 ", list_check.count(2))
    print("3 ", list_check.count(3))

    print("tempo médio: ", sum(list_time) / len(list_time))
    print(list_time)

    """
    link = filter_qrcode("my/" + name_image).split("'")[1]
    
    data_dict = selenium_open(link)

    print(data_dict)
    write_csv(data_dict)
    """

    # files_in_folder(PAST_DATA + "Test/")

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