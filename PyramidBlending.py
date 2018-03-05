from Utils import *
import cv2
import numpy as np


def gaussianOf(im, numLayers=6, debug=False):
    gauss = im.copy()
    gaussPyrList = [gauss]
    for i in range(numLayers):
        gauss = cv2.pyrDown(gauss)
        gaussPyrList.append(gauss)

        if debug:
            cv2.imshow("image", gauss)
            CloseAllWhenPressed()

    return gaussPyrList


def laplacianOf(guassList, numLayers=6, debug=False):
    indexOfLast = numLayers - 1
    lapList = [guassList[indexOfLast]]
    for i in range(indexOfLast, 0, -1):
        GE = cv2.pyrUp(guassList[i])
        laplace = cv2.subtract(guassList[i - 1], GE)
        lapList.append(laplace)
        if debug:
            cv2.imshow("image", laplace)
            CloseAllWhenPressed()

    return lapList


def addHalves(leftHalfLapList, rightHalfLapList):
    stitchedLaplacians = []
    for la, lb in zip(leftHalfLapList, rightHalfLapList):
        rows, cols, dpt = la.shape
        ls = np.hstack((la[:, 0:int(cols / 2)], lb[:, int(cols / 2):]))
        stitchedLaplacians.append(ls)

    return stitchedLaplacians


def reconstructFromLapPyr(lapPyr, numLayers=6):
    finalImage = lapPyr[0]
    for i in range(1, numLayers):
        finalImage = cv2.pyrUp(finalImage)
        finalImage = cv2.add(finalImage, lapPyr[i])

    return finalImage


def cropTo(im, width=None, height=None):
    h, w, d = im.shape

    if height is None:
        height = h + 1

    if width is None:
        width = w + 1

    return im[1:(height + 1), 1:(width + 1)]


left = cv2.imread('apple.jpg')
right = cv2.imread('orange.jpg')
layersDeep = 5

origHeight, origWidth, dpt = left.shape
directBlend = np.hstack((left[:, :int(origWidth / 2)], right[:, int(origWidth / 2):]))

gaussPyrOfleft = gaussianOf(left, layersDeep)

gaussPyrOfright = gaussianOf(right, layersDeep)

lapPyrOfleft = laplacianOf(gaussPyrOfleft, layersDeep)

lapPyrOfright = laplacianOf(gaussPyrOfright, layersDeep)

LS = addHalves(lapPyrOfleft, lapPyrOfright)

ls_ = reconstructFromLapPyr(LS, layersDeep)

cv2.imwrite('Pyramid_blending{}.jpg'.format(layersDeep), ls_)
cv2.imwrite('Direct_blending.jpg', directBlend)
