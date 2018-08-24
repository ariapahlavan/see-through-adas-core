from Utils import *
from VideoStitchingAPIs.FrameStitch import PatchImages


class TestBlending:
    stitchedLaplacians = []

    def __init__(self, img, numlayres=6, imgName="unknown"):
        """
        initialize image blending
        """
        self.im = img
        self.numlayres = numlayres
        self.name = imgName
        self.gaussianPyrList = None
        self.laplacianPyrList = None

    def gaussianPyramid(self, debug=False):
        gauss = self.im.copy()
        gaussPyrList = [gauss]
        for i in range(self.numlayres):
            gauss = cv2.pyrDown(gauss)
            gaussPyrList.append(gauss)

            if debug:
                ShowImgAndCloseWhen(gauss, "{} (gauss)".format(self.name))

        self.gaussianPyrList = gaussPyrList
        return gaussPyrList

    def laplacianPyramid(self, debug=False):
        if self.gaussianPyrList is None:
            self.gaussianPyramid(debug=debug)

        indexOfLast = self.numlayres - 1
        gaussList = self.gaussianPyrList

        lapList = [gaussList[indexOfLast]]

        for i in range(indexOfLast, 0, -1):
            prevScaledUpGauss = cv2.pyrUp(gaussList[i])
            currGauss = gaussList[i - 1]

            laplace = cv2.subtract(currGauss, prevScaledUpGauss)
            lapList.append(laplace)

            if debug:
                ShowImgAndCloseWhen(laplace, "{} (laplace)".format(self.name))

        self.laplacianPyrList = lapList
        return lapList

    def stitchedWith(self, other, debug=False):
        otherLap = other.laplacianPyramid(debug=debug)
        selfLap = self.laplacianPyramid(debug=debug)

        for sl, ol in zip(selfLap, otherLap):
            stitched = PatchImages(sl, ol)
            self.stitchedLaplacians.append(stitched)
            if debug:
                ShowImg(sl, windowName="{} (sl)".format(self.name))
                ShowImg(ol, windowName="{} (ol)".format(self.name))
                ShowImgAndCloseAllWhen(stitched, windowName="{} (stitched)".format(self.name))

        return self

    def reconstructed(self, debug=False):
        if len(self.stitchedLaplacians) == 0 or self.laplacianPyrList is None:
            self.stitchedLaplacians = self.laplacianPyramid(debug=debug)

        lap = self.stitchedLaplacians
        finalImage = lap[0]

        for i in range(1, self.numlayres):
            finalImage = cv2.pyrUp(finalImage)
            finalImage = cv2.add(finalImage, lap[i])

            if debug:
                ShowImgAndCloseWhen(finalImage, "{} (blended)".format(self.name))

        return finalImage
