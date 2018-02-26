import cv2
import time

BACK_PATH = "./back.jpg"
FRONT_PATH = "./front.jpg"
CHOOSER_WINDOW = "Choose Coordinates"

backImg = cv2.imread(BACK_PATH, cv2.IMREAD_COLOR)
frontImg = cv2.imread(FRONT_PATH, cv2.IMREAD_COLOR)

stitchingCoordinates = []


def justpass(): pass


def onMouse(e, x, y, d, param):
    if e == cv2.EVENT_LBUTTONDOWN:
        if len(stitchingCoordinates) != 4:
            stitchingCoordinates.append((x, y))
            print("added ({}, {})".format(x, y))

        if len(stitchingCoordinates) == 4:
            cv2.setMouseCallback(CHOOSER_WINDOW, justpass)
            cv2.destroyWindow(CHOOSER_WINDOW)

    return


cv2.imshow(CHOOSER_WINDOW, backImg)
cv2.setMouseCallback(CHOOSER_WINDOW, onMouse)

while True:
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
