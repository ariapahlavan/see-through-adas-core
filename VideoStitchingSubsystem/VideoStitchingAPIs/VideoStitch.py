import cv2

from VideoStitchingSubsystem.Utils import CarLocationParser

NUM_FRAMES = 2008
IN_DIR = "../Tests/"
TEST_NUM = 3
BACK_PATH = "{}backSync{}".format(IN_DIR, TEST_NUM)
FRONT_PATH = "{}frontSync{}".format(IN_DIR, TEST_NUM)
IMG_NAME = "img"
IMG_FORMAT = ".jpg"

pathOf = lambda path, name, index, fmt: "{}/{}{}{}".format(path, name, index, fmt)
imgPathOf = lambda path, index: pathOf(path, IMG_NAME, index, IMG_FORMAT)
backPathOf = lambda index: imgPathOf(BACK_PATH, index)
frontPathOf = lambda index: imgPathOf(FRONT_PATH, index)

OUT_DIR = "./"
OUT_PATH = "{}overlaid{}".format(OUT_DIR, TEST_NUM)
OUT_IMG_NAME = "img"
OUT_IMG_FORMAT = IMG_FORMAT

outPathOf = lambda index: pathOf(OUT_PATH, OUT_IMG_NAME, index, OUT_IMG_FORMAT)

ROI_FILE = "./roi{}.txt".format(TEST_NUM)
parser = CarLocationParser(ROI_FILE)

frameCount = 1

roi = None
while frameCount != NUM_FRAMES:
    back = cv2.imread(backPathOf(frameCount))
    front = cv2.imread(frontPathOf(frameCount))
    front = front[720, 1280]
    stitched = parser.nextRoi(back, front, frameCount)

    cv2.imwrite(outPathOf(frameCount), stitched)
    print(frameCount)
    frameCount += 1

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
