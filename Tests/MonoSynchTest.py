import os
import sys
import glob
import cv2

BACK_DIR = "./back_out"
FRONT_DIR = "./front_out"


if not os.path.exists(BACK_DIR) or not os.path.exists(FRONT_DIR):
    print("image dir does not exist, exiting...")
    sys.exit(-1)

counter = 1
fmt = ".jpg"
BACK_DIR = "{}/img".format(BACK_DIR)
FRONT_DIR = "{}/img".format(FRONT_DIR)

readFormat = "{}{}_*{}"


def timeStampOf(path):
    filesFound = glob.glob(path)
    if len(filesFound) == 0:
        print("Done!")
        sys.exit(0)

    if len(filesFound) > 1:
        print("Found more than one file with same index, exiting...")
        sys.exit(-1)

    filename = filesFound[0]
    timeAndFormat = filename.split("__")
    timeStamp = float(timeAndFormat[1].strip("jpg"))
    return timeStamp


while True:
    # filesFound = glob.glob(readFormat.format(BACK_DIR, counter, fmt))
    # if len(filesFound) == 0:
    #     break
    #
    # if len(filesFound) > 1:
    #     print("Found more than one file with same index, exiting...")
    #     sys.exit(-1)
    #
    # filename = filesFound[0]
    # timeStamp = float(filename.split("_")[1].strip(".jpg"))
    # print("{} - {}".format(counter, filename))
    # print(timeStamp)
    # with open(filename, 'r') as f:
    #     for line in f:
    #         print(line)

    # frame, capturedTime = monoCam.read()

    # cv2.imshow("frame", frame)
    #
    # cv2.imwrite("{}{}_{}{}".format(DIR, counter, capturedTime, fmt), frame)
    print(timeStampOf(readFormat.format(BACK_DIR, counter, fmt)))
    print(timeStampOf(readFormat.format(FRONT_DIR, counter, fmt)))
    counter += 1

    # key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    # if key == ord("q"):
    #     break

# stop cameras and close windows
# launcher.stop()
