import numpy as np
import cv2

NUM_FRAMES = 6476
IN_DIR = "./"
BACK_PATH = "{}back".format(IN_DIR)
FRONT_PATH = "{}front".format(IN_DIR)
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

frameCount = 0

while frameCount != NUM_FRAMES:
    back = cv2.imread(backPathOf(frameCount))
    front = cv2.imread(frontPathOf(frameCount))

    from VideoStitching.FrameStitch import transformPerspective

    stitchedFrame = transformPerspective(back, front, ())
    cv2.imshow("stitched", stitchedFrame)
    # cv2.imwrite(outPathOf(frameCount), stitchedFrame)

    frameCount += 1

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
