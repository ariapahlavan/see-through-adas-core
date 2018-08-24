import os
import sys
import glob
from time import sleep

import cv2
from VideoStitchingSubsystem.Common import SecToMillisec, createDir

BACK_DIR = "./back_out"
FRONT_DIR = "./front_out"

BACK_SYNC_DIR = "./backSync"
FRONT_SYNC_DIR = "./frontSync"

if not os.path.exists(BACK_DIR) or not os.path.exists(FRONT_DIR):
    print("image dir does not exist, exiting...")
    sys.exit(-1)

createDir(BACK_SYNC_DIR, "back sync")
createDir(FRONT_SYNC_DIR, "front sync")


def saveSync(im, index, dir):
    cv2.imwrite("{}/img{}.jpg".format(dir, index), im)


counter = 1
fmt = ".jpg"
BACK_DIR = "{}/img".format(BACK_DIR)
FRONT_DIR = "{}/img".format(FRONT_DIR)

readFormat = "{}{}_*{}"

backTimeStamps = []
frontTimeStamps = []


def timeStampOf(path):
    filesFound = glob.glob(path)
    if len(filesFound) == 0:
        print("Done!")
        return -1, ""

    if len(filesFound) > 1:
        print("Found more than one file with same index, exiting...")
        sys.exit(-1)

    filename = filesFound[0]
    timeStamp = float(filename.split("__")[1].strip("jpg"))
    return timeStamp, filename


while True:
    print("counter={}".format(counter))
    bts, name = timeStampOf(readFormat.format(BACK_DIR, counter, fmt))

    if bts == -1:
        break

    backTimeStamps.append({'ts': bts, 'name': name})
    counter += 1

counter = 1
while True:
    print("counter={}".format(counter))
    fts, name = timeStampOf(readFormat.format(FRONT_DIR, counter, fmt))

    if fts == -1:
        break

    frontTimeStamps.append({'ts': fts, 'name': name})
    counter += 1

backFinal, frontFinal = [], []
i, j = 0, 0


def addSynchedFrames(ai, bi):
    backFinal.append(backTimeStamps[ai])
    frontFinal.append(frontTimeStamps[bi])


backTimeStampOf = lambda i: backTimeStamps[i].get("ts")
frontTimeStampOf = lambda i: frontTimeStamps[i].get("ts")

while i != len(backTimeStamps) and j != len(frontTimeStamps):
    print("i={}, j={}".format(i, j))
    if backTimeStampOf(i) == frontTimeStampOf(j):
        addSynchedFrames(i, j)
        i += 1
        j += 1
    elif backTimeStampOf(i) > frontTimeStampOf(j):  # move j
        prevDiff = backTimeStampOf(i) - frontTimeStampOf(j)
        j += 1
        while j != len(frontTimeStamps) and prevDiff > abs(backTimeStampOf(i) - frontTimeStampOf(j)):
            prevDiff = abs(backTimeStampOf(i) - frontTimeStampOf(j))
            j += 1
        addSynchedFrames(i, j - 1)
        i += 1
    else:
        prevDiff = frontTimeStampOf(j) - backTimeStampOf(i)
        i += 1
        while i != len(backTimeStamps) and prevDiff > abs(frontTimeStampOf(j) - backTimeStampOf(i)):
            prevDiff = abs(frontTimeStampOf(j) - backTimeStampOf(i))
            i += 1
        addSynchedFrames(i - 1, j)
        j += 1


index = 1

maxTime, minTime, avg = 0, 999999, 0


def addTime(newT, maxT, minT, avgT):
    if newT > maxT:
        maxT = newT
    if newT < minT:
        minT = newT

    return maxT, minT, avgT + newT


for b, f in zip(backFinal, frontFinal):
    backTime = b.get("ts")
    frontTime = f.get("ts")

    bf = cv2.imread(b.get("name"))
    ff = cv2.imread(f.get("name"))
    saveSync(bf, index, BACK_SYNC_DIR)
    saveSync(ff, index, FRONT_SYNC_DIR)



    t = SecToMillisec(abs(backTime - frontTime))
    maxTime, minTime, avg = addTime(t, maxTime, minTime, avg)
    print("(%d)\t%.4f\t\t---  %.4f\t\t--> %.4f" % (index, backTime, frontTime, t))
    index += 1

    sleep(1 / 10)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
print("max=%.4f" % maxTime)
print("min=%.4f" % minTime)
print("avg=%.4f" % (avg / len(backFinal)))
