from time import sleep

import cv2

from Utils import CarParser

NUM_FRAMES = 6476
IN_DIR = "../Tests/"
BACK_PATH = "{}backSynch".format(IN_DIR)
FRONT_PATH = "{}frontSynch".format(IN_DIR)
IMG_NAME = "img"
IMG_FORMAT = ".jpg"

pathOf = lambda path, name, index, fmt: "{}/{}{}{}".format(path, name, index, fmt)
imgPathOf = lambda path, index: pathOf(path, IMG_NAME, index, IMG_FORMAT)
backPathOf = lambda index: imgPathOf(BACK_PATH, index)
frontPathOf = lambda index: imgPathOf(FRONT_PATH, index)

OUT_DIR = "./"
OUT_PATH = "{}out".format(OUT_DIR)
OUT_IMG_NAME = "stitchedImg"
OUT_IMG_FORMAT = IMG_FORMAT

outPathOf = lambda index: pathOf(OUT_PATH, OUT_IMG_NAME, index, OUT_IMG_FORMAT)

ROI_FILE = "./roi.txt"
parser = CarParser(ROI_FILE)

frameCount = 1

roi = None
while frameCount != NUM_FRAMES:
    # try:
    #     roi = parser.nextRoi()
    # except StopIteration:
    #     break

    back = cv2.imread(backPathOf(frameCount))
    front = cv2.imread(frontPathOf(frameCount))
    # cv2.imshow("front", front)
    # cv2.imshow("back", back)
    try:
        roi = parser.nextRoi(back, front)
    except StopIteration:
        break

    # if roi is not None:
    #     from VideoStitchingAPIs.FrameStitch import transformPerspective
    #     stitchedFrame = transformPerspective(back, front, roi)
    # else:
    #     stitchedFrame = back
    #
    # cv2.imshow("stitched", stitchedFrame)
    # cv2.imwrite(outPathOf(frameCount), stitchedFrame)

    # sleep(1)

    frameCount += 1

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
