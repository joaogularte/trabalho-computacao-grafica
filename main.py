import numpy as np
import cv2 as cv
import utils
import matplotlib.pyplot as plt

"""
    Retorna as dimensões de uma imagem 
    Inputs: imagem
    Return: dicionario com high e width
"""
def getDimensions(img):
    return {
        'high': img.shape[0],
        'width': img.shape[1]
    }

"""
    Divide uma imagem em três partes, mantendo intersecção entre as mesmas
    Inputs: imagem e width(largura) da imagem
    Return: dicionario com as três partes da imagem
"""
def cutImage(img, width):
    PARTS = 3
    sizePart = int(width/PARTS)
    return {
        'partOne': img[:, 0:sizePart + 100],
        'partTwo': img[:, sizePart - 250 :sizePart*(PARTS-1) + 250 ],
        'partThree': img[:, sizePart*(PARTS-1) : sizePart*PARTS ]
    } 

"""
    Posiciona o grafico b-splines no canto inferior direito da imagem
    Inputs: bsplines, img, bsplinesDimensions e imgDimensions
    Return: uma nova imagem com a bsplines no canto inferior direito da imagem
"""
def addBsplinesToBottomRightCorner(bsplines, img, bsplinesDimensions, imgDimensions):

    img[
        # eixo y = start point : finish point 
        # start point = ALTURA MAXIMA DA IMAGEM - ALTURA MAXIMA BSPLINE 
        # finish point = ALTURA MAXIMA DA IMAGEM
        imgDimensions['high'] - bsplinesDimensions['high'] : imgDimensions['high'], 
        
        # # eixo x = start point : finish point 
        # start point = LARGURA MAXIMA DA IMAGEM - LARGURA MAXIMA BSPLINE 
        # finish point = LARGURA MAXIMA DA IMAGEM
        imgDimensions['width'] - bsplinesDimensions['width'] : imgDimensions['width']
    ] = bsplines
    return img

"""
    Posiciona o grafico b-splines no canto inferior esquerdo da imagem
    Inputs: bsplines, img, bsplinesDimensions e imgDimensions
    Return: uma nova imagem com a bsplines no canto inferior esquerdo da imagem
"""
def addBsplinesToBottomLeftCorner(bsplines, img, bsplinesDimensions, imgDimensions):
    img[
        # eixo y = start point : finish point 
        # start point = ALTURA MAXIMA DA IMAGEM - ALTURA MAXIMA BSPLINE 
        # finish point = ALTURA MAXIMA DA IMAGEM
        imgDimensions['high'] - bsplinesDimensions['high'] : imgDimensions['high'],

        # # eixo x = start point : finish point 
        # start point = 0 
        # finish point = LARGURA MAXIMA DA IMAGEM
        0 : bsplinesDimensions['width']
    ] = bsplines
    return img

"""
    Posiciona o grafico b-splines no canto inferior esquerdo e direito da imagem
    Inputs: bsplines, img, bsplinesDimensions e imgDimensions
    Return: uma nova imagem com a bsplines no canto inferior esquerdo e direito da imagem
"""
def addBsplinesToBottomLeftAndRightCorner(bsplines, img, bsplinesDimensions, imgDimensions):
    #Chama as funções acimas
    imgAlmost = addBsplinesToBottomLeftCorner(bsplines, img, bsplinesDimensions, imgDimensions)
    imgComplete = addBsplinesToBottomRightCorner(bsplines, imgAlmost, bsplinesDimensions, imgDimensions)
    return imgComplete

"""
    Faz a escala da imagem informada baseada nos valores de x e y
    Inputs: img, x e y
    Return: uma nova imagem com novo tamanho
"""
def scaleImage(img, x, y):
    return cv.resize(img, None, fx=x, fy=y)


"""
    Faz a rotação da imagem informada baseada no grau informado
    Inputs: img, dimensions, degree
    Return: uma nova imagem com novo tamanho
"""
def rotateImage(img, dimensions, degree):
    cols = dimensions['width']
    rows = dimensions['high']

    M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0), degree, 1)
    return cv.warpAffine(img, M, (cols, rows))

"""
    Aplica a tecnica stitch para o conjunto de imagens
    Inputs: setOfImages
    Return: uma nova imagem,  constituida através do conjunto
"""
def makeStitch(setOfImages):
    stitcher = cv.Stitcher_create()
    s, r = stitcher.stitch(setOfImages)
    return r

img = cv.imread('./1.png')
bsplines = cv.imread('./bspline2.jpg')

imgDimen = getDimensions(img)
bsplineDimen = getDimensions(bsplines)

imgParts = cutImage(img, imgDimen['width'])


newPartOne = addBsplinesToBottomRightCorner(bsplines, imgParts['partOne'], bsplineDimen, getDimensions(imgParts['partOne']))
newPartTwo = addBsplinesToBottomLeftAndRightCorner(bsplines, imgParts['partTwo'], bsplineDimen, getDimensions(imgParts['partTwo']))
newPartThree = addBsplinesToBottomLeftCorner(bsplines, imgParts['partThree'], bsplineDimen, getDimensions(imgParts['partThree']))

#cv.imshow('Added b-splines',np.concatenate((newPartOne, newPartTwo, newPartThree), axis=1))
#cv.waitKey(0)

partOneScaled = scaleImage(newPartOne, 0.2, 0.2)
partThreeRotated = rotateImage(newPartThree, getDimensions(imgParts['partThree']), 5)

setOfImages = []
setOfImages.append(partOneScaled)
setOfImages.append(newPartTwo)
setOfImages.append(partThreeRotated)

finalImage = makeStitch(setOfImages)

cv.imshow('After made stitch',finalImage)
cv.waitKey(0)

