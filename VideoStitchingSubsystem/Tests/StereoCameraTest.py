from VideoStitchingSubsystem.StereoCameraAPIs.StereoCameraStream import StereoCameraStream
from VideoStitchingSubsystem.StereoCameraAPIs.MonoLensStream import Resolution

import cv2

stereo = StereoCameraStream(cam1=0, cam2=2, framerate=30, resolution=Resolution._Hd.value)

while True:
    leftFrame, rightFrame = stereo.read()

    # show the output frame
    cv2.imshow("left", leftFrame)
    # cv2.imshow("right", rightFrame)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# stop cameras and close windows
stereo.stop()
