from collections import Sized

from collections import Iterator
import cv2


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


CENTER = 1280 / 2, 720 / 2


def DistFromCenterOf(centerOfRoi):
    print("center={}".format(CENTER))
    print("centerRoi={}".format(centerOfRoi))
    cx, cy = CENTER
    x, y = centerOfRoi

    from math import sqrt
    return sqrt(
        (cx - x)**2 + (cy - y)**2
    )


def CenterOf(roi):
    print("roi={}".format(roi))
    x0, y0, x1, y1 = roi
    return (x0 + x1) / 2, (y0 + y1) / 2


def IsCloser(roi, prevRoi):
    distOfRoi = DistFromCenterOf(CenterOf(roi))
    distOfPrev = DistFromCenterOf(CenterOf(prevRoi))
    dist = distOfRoi < distOfPrev

    print("dist of cur={}, prev={}".format(distOfRoi, distOfPrev))
    return dist
    # return DistFromCenterOf(CenterOf(roi)) > \
    #        DistFromCenterOf(CenterOf(prevRoi))


class CarParser(Iterator, Sized):
    def __len__(self) -> int:
        return len(self.objectsOfFrames)

    def __next__(self):
        """
        :return: next frame's ROI if any remained
        """
        if self.__len__() == self.index:
            raise StopIteration

        # return self.nextRoi()

    def nextRoi(self, bg, fg):
        """
        :return: next frame's ROI, if any exists
        """
        curFrameObjs = self.objectsOfFrames[self.index]
        roi = None

        for obj in curFrameObjs:
            if obj[0] == "car":
                curRoi = (int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]))
                if roi is None or IsCloser(curRoi, roi):
                    roi = curRoi

        if roi is None:
            self.index += 1
            cv2.imshow("stitching", bg)
            return roi

        from VideoStitchingAPIs.FrameStitch import transformPerspective
        stitched = transformPerspective(bg, fg, roi)

        for obj in curFrameObjs:
            if obj[0] == "car":
                curRoi = (int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]))
                x, y = CenterOf(curRoi)
                print("center=({}, {})".format(x,y))
                cv2.circle(stitched, (int(x), int(y)), 10, (0, 0, 255), thickness=-1)

        cv2.circle(stitched, (640, 360), 10, (0, 255, 0), thickness=-1)
        cv2.imshow("stitching", stitched)

        from time import sleep
        sleep(1/30)

        print("index={}".format(self.index))
        self.index += 1
        return roi
        # curFrameObjs = self.objectsOfFrames[self.index]
        # roi = None
        #
        # for obj in curFrameObjs:
        #     if obj[0] == "car":
        #         curRoi = (int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]))
        #         if roi is None or IsCloser(curRoi, roi):
        #             roi = curRoi
        #             # break
        #
        # self.index += 1
        # return roi

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

        self.index = 0

    def __sizeof__(self):
        return len(self.objectsOfFrames)
