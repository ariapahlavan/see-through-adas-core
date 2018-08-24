import cv2

NUM_FRAMES = 3001

IN_DIR = "./"
STITCHED_PATH = "{}test_out".format(IN_DIR)
IMG_NAME = ""
IMG_FORMAT = ".png"

pathOf = lambda path, name, index, fmt: "{}/{}{}{}".format(path, name, index, fmt)
imgPathOf = lambda path, index: pathOf(path, IMG_NAME, index, IMG_FORMAT)
stitchedPathOf = lambda index: imgPathOf(STITCHED_PATH, index)

frameCount = 1

while frameCount != NUM_FRAMES:
    print(stitchedPathOf(frameCount))
    stitched = cv2.imread(stitchedPathOf(frameCount))
    cv2.imshow("stitched", stitched)
    frameCount += 1

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
