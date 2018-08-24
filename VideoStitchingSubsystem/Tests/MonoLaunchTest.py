import os
import time
import cv2
from VideoStitchingSubsystem.StereoCameraAPIs.MonoLensLauncher import MonoLensLauncher

t = 1521660060000 * 1000  # a Unix time in microseconds


def createDir(path, name):
    try:
        os.mkdir(path)
    except IOError:
        print("{} directory already exist.".format(name))


DIR = "./out"
createDir(DIR, "out")

launcher = MonoLensLauncher(timeToStart=t, lens=0, framerate=30)

monoCam = launcher.getCams()

startingTime = time.time()

counter = 1
fmt = ".jpg"
DIR = "./out/img"
while True:
    frame, capturedTime = monoCam.read()

    cv2.imshow("frame", frame)

    cv2.imwrite("{}{}__{}__{}".format(DIR, counter, capturedTime, fmt), frame)
    counter += 1

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# stop cameras and close windows
launcher.stop()

print("elapsed time = {}".format(time.time() - startingTime))
