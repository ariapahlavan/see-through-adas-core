import os
import cv2

from VideoStitchingSubsystem.StereoCameraAPIs.StereoCameraLauncher import StereoCameraLauncher


t = 1521660060000 * 1000  # a Unix time in microseconds

launcher = StereoCameraLauncher(timeToStart=t, cam=(0, 0))

stereoCam = launcher.getCams()

LEFT_DIR = "./left"
RIGHT_DIR = "./right"


def createDir(path, name):
    try:
        os.mkdir(path)
    except IOError:
        print("{} directory already exist.".format(name))


createDir(LEFT_DIR, "left")
createDir(RIGHT_DIR, "right")

IMAGE_NAME_FORMAT = "/{:06d}.jpg"
leftPath = LEFT_DIR + IMAGE_NAME_FORMAT
rightPath = RIGHT_DIR + IMAGE_NAME_FORMAT

counter = 0
fmt = ".jpg"
LEFT_DIR = "./left/img"
# RIGHT_DIR = "./right/img"
while True:
    leftData, rightData = stereoCam.read()
    leftFrame, leftTime = leftData
    rightFrame, rightTime = rightData

    # cv2.imshow("left cam", leftFrame)
    # cv2.imshow("right cam", rightFrame)

    cv2.imwrite("{}{}{}".format(LEFT_DIR, counter, fmt), leftFrame)
    # cv2.imwrite("{}{}{}".format(RIGHT_DIR, counter, fmt), rightFrame)
    counter += 1

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# stop cameras and close windows
launcher.stop()
