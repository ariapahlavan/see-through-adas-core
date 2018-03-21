from DualCameraAPIs.DualLensLauncher import DualLensLauncher
from DualCameraAPIs.DualLenseStream import DualLensStream
from DualCameraAPIs.MonoLensStream import Resolution

import cv2

t = 1520444990000*1000  # a Unix time in microseconds

launcher = DualLensLauncher(timeToStart=t, cam=(0, 2))

stereoCam = launcher.getCams()

while True:
    leftFrame, rightFrame = stereoCam.read()

    # show the output frame
    cv2.imshow("cam left", leftFrame)
    cv2.imshow("cam right", rightFrame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# stop cameras and close windows
launcher.stop()
