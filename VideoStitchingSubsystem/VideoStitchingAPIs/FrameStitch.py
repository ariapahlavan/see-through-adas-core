import numpy as np

from VideoStitchingSubsystem.Utils import *


def PatchImages(bgImg, fgImg):
    grayed = cv2.cvtColor(fgImg, cv2.COLOR_BGR2GRAY)
    _, grayed = cv2.threshold(grayed, 0, 255, cv2.THRESH_BINARY)
    grayedInv = cv2.bitwise_not(grayed)

    bgfinal = cv2.bitwise_and(bgImg, bgImg, mask=grayedInv)
    fgfinal = cv2.bitwise_and(fgImg, fgImg, mask=grayed)

    finalImage = cv2.add(bgfinal, fgfinal)

    return finalImage


def PoissonBlend(bgImg, fgImg, roi):
    mask = MaskWith(fgImg.shape, roi)

    cx, cy = CenterOf(roi)
    out = cv2.seamlessClone(fgImg,
                            bgImg,
                            mask,
                            (int(cx), int(cy)),
                            cv2.NORMAL_CLONE)

    return out

def PoissonBlendNoMask(bgImg, fgImg, mask, roi):

    cx, cy = CenterOf(roi)
    out = cv2.seamlessClone(fgImg,
                            bgImg,
                            mask,
                            (int(cx), int(cy)),
                            cv2.NORMAL_CLONE)

    return out


def stitch(bg, fg, roi):
    out = PoissonBlend(bg, fg, roi)
    out = PatchImages(bg, fg)
    return out


def transformPerspective(bgImg, fgImg, roi):
    fgHeight, fgWidth, _ = fgImg.shape
    fgImageCoords = np.array([(0, 0),
                              (0, fgHeight),
                              (fgWidth, fgHeight),
                              (fgWidth, 0)])
    x0, y0, x1, y1 = roi
    stitchToCoords = np.array([(x0, y0),
                               (x0, y1),
                               (x1, y1),
                               (x1, y0)])

    homography, _ = cv2.findHomography(fgImageCoords, stitchToCoords, 0)

    bgHeight, bgWidth, _ = bgImg.shape
    projectedIm = cv2.warpPerspective(src=fgImg, M=homography, dsize=(bgWidth, bgHeight))

    return stitch(bgImg, projectedIm, roi)
