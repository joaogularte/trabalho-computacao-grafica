import numpy as np
import cv2 as cv
import utils

"""print(img.shape)"""
""" (numero de linhas, numero de colunhas, o item da linha x coluna espeficica)"""

img = cv.imread('./1543245201_231440_1543245268_noticia_normal.jpg')


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