import threading
import time
from threading import Thread

from DualCameraAPIs.DualLenseStream import DualLensStream
from DualCameraAPIs.MonoLensStream import Resolution
from common import toMicroSec


class DualLensLauncher:
    runningCams = []

    def __init__(self, stereo1=(0, 3), stereo2=(2, 4), interval=5, framerate=30, resolution=Resolution._240p.value):
        """
        initialize two stereo cameras synchronously
        """
        timeToStart = toMicroSec(time.time() + interval)
        stereCam1Attribs = (stereo1, framerate, resolution, timeToStart)
        stereCam2Attribs = (stereo2, framerate, resolution, timeToStart)

        self.stereoThread1 = Thread(target=self.start, args=stereCam1Attribs).start()
        self.stereoThread2 = Thread(target=self.start, args=stereCam2Attribs).start()

    def start(self, stereoCam, framerate, resolution, atTime):
        """
        start the stereo camera at time give
        """
        # (stereoCam, framerate, resolution, atTime, runningCams) = attribs

        print("stere: now = {}, at = {}".format(time.time(), atTime))

        while toMicroSec(time.time()) <= atTime:
            continue

        self.runningCams.append(DualLensStream(stereoCam[0], stereoCam[1], framerate, resolution))

    def getCams(self):
        while len(self.runningCams) != 2:
            continue

        return self.runningCams

    def stop(self):
        """
        stop video stream from dual camera module and destroy windows
        """
        if len(self.runningCams) != 2:
            print("Two cameras have not been started.")

        try:
            self.runningCams[0].stop()
            self.runningCams[1].stop()
        except IOError:
            print("Failed to stop both cameras")
