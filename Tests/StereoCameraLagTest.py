from StereoCameraAPIs.StereoCameraStream import StereoCameraStream
from StereoCameraAPIs.MonoLensStream import Resolution

import cv2
import time

stereo = StereoCameraStream(cam1=0, cam2=2, framerate=60, resolution=Resolution._32p.value)

iterCount = 1000
iterNum = iterCount
avg = 0
maxDelay = 0
minDelay = 0

while True:
    cur_time_in_micro = time.time() * 1000 * 1000
    leftFrame = stereo.readLeft()
    cur_time_in_micro2 = time.time() * 1000 * 1000
    rightFrame = stereo.readRight()
    cur_time_in_micro3 = time.time() * 1000 * 1000

    print(cur_time_in_micro2 - cur_time_in_micro)
    iterNum -= 2
    curDiff = cur_time_in_micro2 - cur_time_in_micro
    avg += curDiff
    avg += cur_time_in_micro3 - cur_time_in_micro2

    if curDiff > maxDelay:
        maxDelay = curDiff

    if minDelay == 0:
        minDelay = curDiff

    if curDiff < minDelay:
        minDelay = curDiff

    if iterNum == 0:
        break

    # show the output frame
    cv2.imshow("Frame1", leftFrame)
    cv2.imshow("Frame2", rightFrame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

toMillisec = lambda n: round(n / 1000)
printResults = lambda title, n: print("{} is {} usec or {} msec".format(title, round(n), toMillisec(n)))

printResults("Avg", avg / iterCount)
printResults("Max", maxDelay)
printResults("Min", minDelay)

# stop cameras and close windows
stereo.stop()
