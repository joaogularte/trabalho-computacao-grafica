import numpy as np
import cv2 as cv
import utils

"""print(img.shape)"""
""" (numero de linhas, numero de colunhas, o item da linha x coluna espeficica)"""

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

def addBsplinesToBottomRightCorner(bsplines, img, bsplinesDimensions, imgDimensions):
    img[imgDimensions['high'] - bsplinesDimensions['high'] : imgDimensions['high'], 
        imgDimensions['width'] - bsplinesDimensions['width'] : imgDimensions['width']] = bsplines
    return img

def addBsplinesToBottomLeftCorner(bsplines, img, bsplinesDimensions, imgDimensions):
    img[imgDimensions['high'] - bsplinesDimensions['high'] : imgDimensions['high'],
        0 : bsplinesDimensions['width']] = bsplines
    return img

def addBsplinesToBottomLeftAndRightCorner(bsplines, img, bsplinesDimensions, imgDimensions):
    imgAlmost = addBsplinesToBottomLeftCorner(bsplines, img, bsplinesDimensions, imgDimensions)
    imgComplete = addBsplinesToBottomRightCorner(bsplines, imgAlmost, bsplinesDimensions, imgDimensions)
    return imgComplete


img = cv.imread('./1543245201_231440_1543245268_noticia_normal.jpg')
bsplines = cv.imread('./bspline3.png')

imgDimen = getDimensions(img)
bsplineDimen = getDimensions(bsplines)

imgParts = cutImage(img, imgDimen['width'])


newPartOne = addBsplinesToBottomRightCorner(bsplines, imgParts['partOne'], bsplineDimen, getDimensions(imgParts['partOne']))
newPartTwo = addBsplinesToBottomLeftAndRightCorner(bsplines, imgParts['partTwo'], bsplineDimen, getDimensions(imgParts['partTwo']))
newPartThree = addBsplinesToBottomLeftCorner(bsplines, imgParts['partThree'], bsplineDimen, getDimensions(imgParts['partThree']))

newImage = np.concatenate((newPartOne, newPartTwo, newPartThree), axis=1)

cv.imshow('test', newImage)
cv.waitKey(0)

#imageParts = cutImage(img, dimensions['width'])