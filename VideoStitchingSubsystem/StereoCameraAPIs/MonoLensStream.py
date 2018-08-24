from enum import Enum
from threading import Thread

import cv2
import time


class Resolution(Enum):
    _32p = (64, 32)
    _96p = (128, 96)
    _120p = (160, 120)
    _144p = (256, 144)
    _240p = (360, 240)
    _288p = (480, 272)
    _360p = (480, 360)
    _480p = (720, 480)
    _576p = (720, 576)
    _Hd = (1280, 720)


class MonoLensStream:
    def setParam(self, param, value, name):
        if self.stream.set(param, value):
            pass
        else:
            import logging
            log = logging.getLogger()
            log.warning("[WARN] cannot set "+name)

    def __init__(self, src=0, framerate=30, resolution=Resolution._240p.value, fourcc="MJPG", exposure=-10,
                 debugEnable=False, debugCount=1000):
        """
        initialize the video stream
        """
        self.stream = cv2.VideoCapture(src)

        # set resolution
        w, h = resolution
        self.setParam(cv2.CAP_PROP_FRAME_WIDTH, w, "width")
        self.setParam(cv2.CAP_PROP_FRAME_HEIGHT, h, "height")
        self.setParam(cv2.CAP_PROP_FPS, framerate, "fps")
        self.setParam(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc), "fourcc")
        self.setParam(cv2.CAP_PROP_EXPOSURE, exposure, "exposure")

        self.fpsDelay = 1 / framerate

        # read first frame
        (self.grabbed, self.frame) = self.stream.read()

        # frame reader thread
        if not debugEnable:
            self.frameReaderThread = Thread(target=self.update, args=())
        else:
            self.min = self.avg = self.max = 0
            self.debugCount = debugCount
            self.frameReaderThread = Thread(target=self.debugUpdate, args=())

        self.streamStopped = False
        self.grabbedTime = time.time()
        self.returnedTime = self.grabbedTime

    def start(self):
        """
        start the thread to read frames from the video stream
        :return reference to itself
        """
        self.frameReaderThread.daemon = True
        self.frameReaderThread.start()
        return self

    def update(self):
        """
        grab the next frame from the stream infinitely until the stream is stopped
        """
        while True:
            if self.streamStopped:  # done with streaming
                return

            (self.grabbed, self.frame) = self.stream.read()
            self.grabbedTime = time.time()
            # time.sleep(self.fpsDelay)

    def read(self):
        """
        :return: the current frame
        """
        while self.returnedTime == self.grabbedTime:
            continue

        self.returnedTime = self.grabbedTime
        return self.frame, self.returnedTime

    def stop(self):
        """
        stop the video stream
        """
        self.streamStopped = True
        self.frameReaderThread.join()
        self.stream.release()

    def debugUpdate(self):
        """
        **FOR DEBUGGING PURPOSES ONLY**
        grab the next frame from the stream infinitely until the stream is stopped
        """

        startTime = time.time() * 1000 * 1000
        (self.grabbed, self.frame) = self.stream.read()
        endTime = time.time() * 1000 * 1000
        self.max = self.min = endTime - startTime

        counter = self.debugCount

        while self.debugCount != 0:
            startTime = time.time() * 1000 * 1000
            (self.grabbed, self.frame) = self.stream.read()
            endTime = time.time() * 1000 * 1000
            ellapsedTime = endTime - startTime

            print(ellapsedTime)

            self.avg += ellapsedTime

            if self.min > ellapsedTime:
                self.min = ellapsedTime

            if self.max < ellapsedTime:
                self.max = ellapsedTime

            self.debugCount -= 1

            time.sleep(self.fpsDelay)

        self.avg = (self.avg / counter)

    def debugResults(self):
        """
        **FOR DEBUGGING PURPOSES ONLY**
        :return average, min, and max from debugging results
        """
        self.frameReaderThread.join()
        self.stream.release()

        return self.avg, self.min, self.max
