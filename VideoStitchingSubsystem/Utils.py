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


def ShrinkBy(im, dw, dh):
    h, w, _ = im.shape
    return im[dh:(h - dh), dw:(w - dw)]


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

    # return roi
    offset = lambda n: (int(n * 12.8), int(n * 7.2))
    dx, dy = offset(35)
    return 800, 25, 800+dx, 25+dy

    if p < X * Y:
        x0 -= 80
        y0 -= 50
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


def IntCenterOf(roi):
    x0, y0, x1, y1 = roi
    return int((x0 + x1) / 2), int((y0 + y1) / 2)


def IsCloser(roi, prevRoi):
    distOfRoi = DistFromCenterOf(CenterOf(roi))
    distOfPrev = DistFromCenterOf(CenterOf(prevRoi))
    dist = distOfRoi < distOfPrev

    return dist


# Bounding trapezoid coordinates
TRAP_DX_TOP = 15
TRAP_DX_BOT = 30
TRAP_DY_TOP = 10
TRAP_DY_BOT = 0
TRAP_X1, TRAP_Y1 = 575 + TRAP_DX_TOP, 392 + TRAP_DY_TOP
TRAP_X2, TRAP_Y2 = 310 + TRAP_DX_BOT, 620 - TRAP_DY_BOT
TRAP_X3, TRAP_Y3 = 620 - TRAP_DX_TOP, 392 + TRAP_DY_TOP
TRAP_X4, TRAP_Y4 = 880 - TRAP_DX_BOT, 620 - TRAP_DY_BOT

TRAP_P1 = (TRAP_X1, TRAP_Y1)
TRAP_P2 = (TRAP_X2, TRAP_Y2)
TRAP_P3 = (TRAP_X3, TRAP_Y3)
TRAP_P4 = (TRAP_X4, TRAP_Y4)


def IsWithinBounds(roi):
    cx, cy = CenterOf(roi)
    lineEq = lambda x1, y1, x2, y2: lambda x: int(y1 + (((y2 - y1) * (x - x1)) / (x2 - x1)))
    yLeft = lineEq(TRAP_X1, TRAP_Y1, TRAP_X2, TRAP_Y2)
    yRight = lineEq(TRAP_X3, TRAP_Y3, TRAP_X4, TRAP_Y4)

    if cy < TRAP_Y1 or cy > TRAP_Y2:
        return False

    if yLeft(cx) > cy:
        return False

    if yRight(cx) > cy:
        return False

    return True


class CarLocationParser(Sized):
    def distToPrev(self, roi):
        px, py = CenterOf(self.prevRoi)
        x, y = CenterOf(roi)

        from math import sqrt
        return sqrt(
            (px - x) ** 2 + (py - y) ** 2
        )

    def nextRoi(self, bg, fg, i=None):
        """
        :return: next frame's ROI, if any exists
        """
        if i is None: i = self.index
        curFrameObjs = self.objectsOfFrames[i]
        roi = None
        minDist = 1500

        carsDetected = 0
        DEBUGGING = False

        if DEBUGGING:
            cv2.line(bg, TRAP_P1, TRAP_P3, (255, 0, 0), 2)
            cv2.line(bg, TRAP_P2, TRAP_P4, (255, 0, 0), 2)
            cv2.line(bg, TRAP_P1, TRAP_P2, (255, 0, 0), 2)
            cv2.line(bg, TRAP_P3, TRAP_P4, (255, 0, 0), 2)

        for obj in curFrameObjs:
            if obj[0] == "car":
                carsDetected += 1
                curRoi = (int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]))

                if not IsWithinBounds(curRoi):
                    if DEBUGGING:
                        cv2.circle(bg, IntCenterOf(curRoi), 4, (0, 0, 255), -1)
                    continue
                else:
                    if DEBUGGING:
                        cv2.circle(bg, IntCenterOf(curRoi), 4, (0, 255, 0), -1)

                curDist = self.distToPrev(curRoi)
                if roi is None or curDist < minDist:
                    minDist = curDist
                    roi = curRoi

        if roi is None or ((self.distToPrev(roi) < 10 or self.distToPrev(roi) > 40) and carsDetected != 1):
            roi = self.prevRoi

        x0Temp, y0Temp, x1Temp, y1Temp = roi
        # x0Temp, y0Temp, x1Temp, y1Temp = x0Temp-20, y0Temp-40, x1Temp-20, y1Temp-40
        roiTemp = x0Temp, y0Temp, x1Temp, y1Temp
        from VideoStitchingAPIs.FrameStitch import transformPerspective
        stitched = transformPerspective(bg, fg, ValidatedRoi(roiTemp))

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

        # self.prevRoi = 539, 422, 561, 439
        self.prevRoi = roi
        self.index = 0

    def __sizeof__(self):
        return len(self.objectsOfFrames)

    def __len__(self) -> int:
        return len(self.objectsOfFrames)
