import threading
import time
from threading import Thread

from DualCameraAPIs.DualLenseStream import DualLensStream
from DualCameraAPIs.MonoLensStream import Resolution
from common import SecToMicrosec


class DualLensLauncher:
    runningCam = None
    isCamLaunched = False

    def __init__(self, timeToStart, cam=(0, 3), framerate=30, resolution=Resolution._240p.value):
        """
        launch a stereo cameras at a given time
        """
        camAttribs = (cam, framerate, resolution, timeToStart)

        self.camThread = Thread(target=self.start, args=camAttribs).start()

    def start(self, stereoCam, framerate, resolution, atTime):
        """
        start the stereo camera at time give
        """
        while SecToMicrosec(time.time()) <= atTime:
            continue

        print("started at {}".format(time.time()))

        self.runningCam = DualLensStream(stereoCam[0], stereoCam[1], framerate, resolution)
        self.isCamLaunched = True

    def getCams(self):
        while not self.isCamLaunched:
            continue

        return self.runningCam

    def stop(self):
        """
        stop video stream from dual camera module and destroy windows
        """
        if not self.isCamLaunched:
            print("The camera has not been started.")

        try:
            self.runningCam.stop()
        except IOError:
            print("Failed to stop the camera")
