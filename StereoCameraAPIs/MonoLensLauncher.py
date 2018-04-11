from StereoCameraAPIs.MonoLensStream import *
from Common import SecToMicrosec


class MonoLensLauncher:
    runningCam = None
    isCamLaunched = False

    def __init__(self, timeToStart, lens=0, framerate=30, resolution=Resolution._Hd.value):
        """
        launch a stereo cameras at a given time
        """
        camAttribs = (lens, framerate, resolution, timeToStart)

        self.camThread = Thread(target=self.start, args=camAttribs).start()

    def start(self, lens, framerate, resolution, atTime):
        """
        start the stereo camera at time give
        """
        while SecToMicrosec(time.time()) <= atTime:
            continue

        print("started at {}".format(time.time()))

        self.runningCam = MonoLensStream(src=lens, framerate=framerate, resolution=resolution).start()
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
