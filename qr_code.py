from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol

from PIL import ImageDraw
from sympy import false


def recognize_qrcode(image_filter):
    barcode = pyzbar.decode(image_filter, symbols=[ZBarSymbol.QRCODE])
    if barcode:
        barcodeData = barcode[0].data
        # print(str(barcodeData))

        return str(barcodeData), barcode

    return False, False


def draw_qrcode(image_qrcode, data_qrcode=False):
    if not (data_qrcode):
        data_qrcode = pyzbar.decode(image_qrcode)

    draw = ImageDraw.Draw(image_qrcode)
    for barcode in data_qrcode:
        rect = barcode.rect
        draw.rectangle(
            ((rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height)),
            outline=(255, 0, 0),
            width=10,
        )

    return image_qrcode