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


class CarParser(Iterator, Sized):
    def __len__(self) -> int:
        return len(self.lineList)

    def __next__(self):
        """
        :return: next frame's ROI if any remained
        """
        while self.__len__() != self.index:
            obj, roi = self.nextBoundary()
            if obj == "-":   return None
            if obj == "car": return roi  # todo implement check

        raise StopIteration

    def nextRoi(self):
        """
        :return: next frame's ROI if any remained
        """
        while self.__len__() != self.index:
            obj, roi = self.nextBoundary()
            if obj == "-":   return None
            if obj == "car": return roi  # todo implement check

        raise StopIteration

    def __init__(self, filepath) -> None:
        self.lineList = list()
        inf = open(filepath)

        for line in inf:
            self.lineList.append(line.strip().split(','))
        self.index = 0

    def nextBoundary(self):
        """
        :return: boundary box the ROI corresponding to the front car in next frame
        """
        lineWords = self.lineList[self.index]
        if lineWords[0] == "car":
            roi = (lineWords[1], lineWords[2], lineWords[3], lineWords[4])
        else:
            roi = None

        self.index += 1
        return lineWords[0], roi

    def __sizeof__(self):
        return len(self.lineList)
