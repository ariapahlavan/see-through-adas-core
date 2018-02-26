from DualCameraAPIs.DualLensLauncher import DualLensLauncher
from DualCameraAPIs.DualLenseStream import DualLensStream
from DualCameraAPIs.MonoLensStream import Resolution

import cv2

#closed = 0
#open   = 3

#1
#4
launcher = DualLensLauncher(interval=5)

stereo1, stereo2 = launcher.getCams()

while True:
    leftFrame1, rightFrame1 = stereo1.read()
    leftFrame2, rightFrame2 = stereo2.read()

    # show the output frame
    cv2.imshow("cam 1 left", leftFrame1)
    cv2.imshow("cam 1 right", rightFrame1)
    cv2.imshow("cam 2 left", leftFrame2)
    cv2.imshow("cam 2 right", rightFrame2)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# stop cameras and close windows
launcher.stop()
