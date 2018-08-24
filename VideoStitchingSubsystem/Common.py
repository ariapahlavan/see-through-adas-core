import os

SecToMillisec = lambda n: n * 1000
SecToMicrosec = lambda n: n * (1000 * 1000)

MilliToMicrosec = lambda n: n * 1000

MillisecToSec = lambda n: n / 1000
MicrosecToSec = lambda n: n / (1000 * 1000)


def createDir(path, name):
    try:
        os.mkdir(path)
    except IOError:
        print("{} directory already exist.".format(name))
