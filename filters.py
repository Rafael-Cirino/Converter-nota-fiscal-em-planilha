from PIL import Image
import numpy as np
import cv2

class filters:
    def dim_ruido(self, image_ocr):
        # convertendo em um array editável de numpy[x, y, CANALS]
        npimagem = np.asarray(image_ocr).astype(np.uint8)  

        # diminuição dos ruidos antes da binarização
        npimagem[:, :, 0] = 0 # zerando o canal R (RED)
        npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

        image_ocr = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)

        return image_ocr
    
    def trunc_bin(self, image_ocr):
        ret, thresh = cv2.threshold(image_ocr, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

        return thresh