from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol

from PIL import ImageDraw


def recognize_qrcode(image_filter):
    barcode = pyzbar.decode(image_filter, symbols=[ZBarSymbol.QRCODE])
    barcodeData = barcode[0].data
    print(str(barcodeData), barcode)


def draw_qrcode(image_qrcode):
    draw = ImageDraw.Draw(image_qrcode)
    for barcode in pyzbar.decode(image_qrcode):
        rect = barcode.rect
        draw.rectangle(
            ((rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height)),
            outline=(255, 0, 0),
            width=10,
        )