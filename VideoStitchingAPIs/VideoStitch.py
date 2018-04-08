import cv2

from Utils import CarParser, ShrinkBy

NUM_FRAMES = 3001
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
OUT_PATH = "{}stitchedFrames".format(OUT_DIR)
OUT_IMG_NAME = "img"
OUT_IMG_FORMAT = IMG_FORMAT

outPathOf = lambda index: pathOf(OUT_PATH, OUT_IMG_NAME, index, OUT_IMG_FORMAT)

ROI_FILE = "./roi.txt"
parser = CarParser(ROI_FILE)

frameCount = 1

roi = None
while frameCount != NUM_FRAMES:
    back = cv2.imread(backPathOf(frameCount))
    front = ShrinkBy(cv2.imread(frontPathOf(frameCount)), 50)
    stitched = parser.nextRoi(back, front)

    # cv2.imwrite(outPathOf(frameCount), stitched)
    print(frameCount)
    frameCount += 1
    # sleep(1)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
