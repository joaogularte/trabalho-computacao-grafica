import numpy as np
import cv2 as cv
import utils

def getDimensions(img):
    return {
        'high': img.shape[0],
        'width': img.shape[1]
    }

def cutImage(img, width):
    PARTS = 3
    sizePart = int(width/PARTS)
    return {
        'partOne': img[:, 0:sizePart],
        'partTwo': img[:, sizePart:sizePart*(PARTS-1)],
        'partThree': img[:, sizePart*(PARTS-1) : sizePart*PARTS ]
    } 
    
"""print(img.shape)"""
""" (numero de linhas, numero de colunhas, o item da linha x coluna espeficica)"""

img = cv.imread('./1543245201_231440_1543245268_noticia_normal.jpg')
print(getDimensions(img))

HIGH = img.shape[0]
WIDTH = img.shape[1]

firstPart = img[:, 0:400]
secondPart = img[:, 400:800] 
thirdPart = img[:, 800:1200]

color = tuple((0, 0, 0))

cv.line(firstPart, (100,300), (400,300), color, 2, )

newImg = np.concatenate((firstPart, secondPart, thirdPart), axis=1)
cv.imshow('test', firstPart)
cv.waitKey(0)