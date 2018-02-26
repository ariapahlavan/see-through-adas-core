import cv2

from DualCameraAPIs.MonoLensStream import MonoLensStream


class DualLensStream:
    def __init__(self, cam1=0, cam2=2, framerate=30, resolution=(320, 240), debugEnable=False, debugCount=1000):
        """
        initialize the dual camera module
        """
        if not debugEnable:
            self.left = MonoLensStream(cam1, framerate, resolution).start()
            self.right = MonoLensStream(cam2, framerate, resolution).start()
            self.debugEnable = False
        else:
            self.left = MonoLensStream(cam1, framerate, resolution, debugEnable=True, debugCount=debugCount).start()
            self.right = MonoLensStream(cam2, framerate, resolution, debugEnable=True, debugCount=debugCount).start()
            self.debugEnable = True

    def read(self):
        """
        :return: current frame tuple from both cameras
        """
        return self.left.read(), self.right.read()

    def readLeft(self):
        """
        :return: current frame from left camera
        """
        return self.left.read()

    def readRight(self):
        """
        :return: current frame from right camera
        """
        return self.right.read()

    def stop(self):
        """
        stop video stream from dual camera module and destroy windows
        """
        self.left.stop()
        self.right.stop()
        cv2.destroyAllWindows()

    def debugResults(self):
        """
        **FOR DEBUGGING PURPOSES ONLY**
        :return average, min, and max time taken for reading frames
        """
        leftAvg, leftMin, leftMax = self.left.debugResults()
        rightAvg, rightMin, rightMax = self.right.debugResults()
        cv2.destroyAllWindows()

        return max(leftAvg, rightAvg), min(leftMin, rightMin), max(leftMax, rightMax)
