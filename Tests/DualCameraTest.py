from DualCameraAPIs.DualLenseStream import DualLensStream
from DualCameraAPIs.MonoLensStream import Resolution

import cv2

#closed = 0
#open   = 3

#1
#4
dualCam = DualLensStream(cam1=0, cam2=2, framerate=30, resolution=Resolution._Hd.value)

while True:
    leftFrame, rightFrame = dualCam.read()

    # show the output frame
    cv2.imshow("Frame1", leftFrame)
    cv2.imshow("Frame2", rightFrame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# stop cameras and close windows
dualCam.stop()
