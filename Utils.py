from collections import Sized

from collections import Iterator
import cv2


def FpsOf(start):
    return cv2.getTickFrequency() / (cv2.getTickCount() - start)


def CloseWhenPressed(windowName, keyToWaitOn='q'):
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyWindow(windowName)


def CloseAllWhenPressed(keyToWaitOn='q'):
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyAllWindows()


def ShowImgAndCloseWhen(im, windowName="image", keyToWaitOn='q'):
    cv2.imshow(windowName, im)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyWindow(windowName)


def ShowImgAndCloseAllWhen(im, windowName="image", keyToWaitOn='q'):
    cv2.imshow(windowName, im)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyAllWindows()


def ShowImg(im, windowName="image"): cv2.imshow(windowName, im)


def ShrinkBy(im, numpixels):
    h, w, _ = im.shape
    return im[numpixels:(h - numpixels), numpixels:(w - numpixels)]


def MaskWith(imgShape, maskRoi):
    import numpy as np
    h, w, nl = imgShape
    mx0, my0, mx1, my1 = maskRoi
    outImg = np.zeros((h, w), np.uint8)
    outImg[my0:my1, mx0:mx1] = 255

    return outImg


WIGHT, HEIGHT = 1280, 720
CENTER = int(WIGHT / 2), int(HEIGHT / 2)


def ValidatedRoi(roi):
    X = 220
    Y = 130
    x0, y0, x1, y1 = roi
    p = (x1 - x0) * (y1 - y0)
    if p < X * Y:
        x0 -= 56
        y0 -= 80
        return (x0, y0, x0 + X, y0 + Y)
    else:
        return roi


def DistFromCenterOf(centerOfRoi):
    cx, cy = CENTER
    x, y = centerOfRoi

    from math import sqrt
    return sqrt(
        (cx - x) ** 2 + (cy - y) ** 2
    )


def CenterOf(roi):
    x0, y0, x1, y1 = roi
    return (x0 + x1) / 2, (y0 + y1) / 2


def IsCloser(roi, prevRoi):
    distOfRoi = DistFromCenterOf(CenterOf(roi))
    distOfPrev = DistFromCenterOf(CenterOf(prevRoi))
    dist = distOfRoi < distOfPrev

    return dist


class CarParser(Sized):
    def distToPrev(self, roi):
        px, py = CenterOf(self.prevRoi)
        x, y = CenterOf(roi)

        from math import sqrt
        return sqrt(
            (px - x) ** 2 + (py - y) ** 2
        )

    def nextRoi(self, bg, fg):
        """
        :return: next frame's ROI, if any exists
        """
        curFrameObjs = self.objectsOfFrames[self.index]
        roi = None
        minDist = 1500

        for obj in curFrameObjs:
            if obj[0] == "car":
                curRoi = (int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]))
                curDist = self.distToPrev(curRoi)
                if roi is None or curDist < minDist:
                    minDist = curDist
                    roi = curRoi

        if roi is None or self.distToPrev(roi) < 30:
            roi = self.prevRoi

        from VideoStitchingAPIs.FrameStitch import transformPerspective
        stitched = transformPerspective(bg, fg, ValidatedRoi(roi))

        self.index += 1
        self.prevRoi = roi
        return stitched

    def __init__(self, filepath) -> None:
        self.objectsOfFrames = list()
        inf = open(filepath)

        curImgObjects = list()

        for line in inf:
            stripped = line.strip()
            if stripped == "-":
                self.objectsOfFrames.append(curImgObjects)
                curImgObjects = list()
            else:
                curImgObjects.append(stripped.split(','))

        roi = None
        for obj in self.objectsOfFrames[0]:
            if obj[0] == "car":
                curRoi = (int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]))
                if roi is None or IsCloser(curRoi, roi):
                    roi = curRoi

        self.prevRoi = roi
        self.index = 0

    def __sizeof__(self):
        return len(self.objectsOfFrames)

    def __len__(self) -> int:
        return len(self.objectsOfFrames)
