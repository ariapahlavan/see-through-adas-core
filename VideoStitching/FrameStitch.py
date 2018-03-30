import numpy as np

from MyTests.TestBlending import TestBlending
from Utils import *


def stitch(bg, fg): return PatchImages(bg, fg)


def transformPerspective(bgImg, fgImg, roi):
    fgHeight, fgWidth, _ = fgImg.shape
    fgImageCoords = np.array([(0, 0),
                              (0, fgHeight),
                              (fgWidth, fgHeight),
                              (fgWidth, 0)])
    y0 = roi.y0
    y1 = roi.y1
    x0 = roi.x0
    x1 = roi.y1
    stitchToCoords = np.array([(x0, y0),
                               (x0, y1),
                               (x1, y1),
                               (x1, y0)])
    homography, _ = cv2.findHomography(fgImageCoords, stitchToCoords, 0)

    bgHeight, bgWidth, _ = bgImg.shape
    projectedIm = cv2.warpPerspective(src=fgImg, M=homography, dsize=(bgWidth, bgHeight))

    stitch(bgImg, projectedIm)
