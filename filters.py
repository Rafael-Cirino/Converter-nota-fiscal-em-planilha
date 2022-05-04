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
    
    def get_grayscale(self, image):
        npimagem = np.asarray(image).astype(np.uint8)
        return cv2.cvtColor(npimagem, cv2.COLOR_BGR2GRAY)
    
    def trunc_bin(self, image_ocr):

        return cv2.threshold(image_ocr, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #return cv2.threshold(image_ocr, 127, 255, cv2.THRESH_TRUNC)[1]
    
    # noise removal
    def remove_noise(self, image):
        return cv2.medianBlur(image,5)

    #dilation
    def dilate(self, image):
        kernel = np.ones((2,2),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)
        
    #erosion
    def erode(self, image):
        kernel = np.ones((2,2),np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(self, image):
        kernel = np.ones((2,2),np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    #skew correction
    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    #template matching
    def match_template(self, image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)