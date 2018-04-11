from StereoCameraAPIs.OldStereoCameraStream import OldStereoCameraStream
from StereoCameraAPIs.OldMonoLensStream import Resolution

stereo = OldStereoCameraStream(cam1=0, cam2=2, framerate=60, resolution=Resolution._32p.value, debugEnable=True)
avgTime, minTime, maxTime = stereo.debugResults()


toMillisec = lambda n: round(n / 1000)
printResults = lambda title, n: print("{} is {} usec or {} msec".format(title, round(n), toMillisec(n)))

printResults("Avg", avgTime)
printResults("Max", maxTime)
printResults("Min", minTime)
