from DualCameraAPIs.dualcamerastream import DualCameraStream

import glob
import os
import random
import sys
import time

import cv2
import numpy as np


inputAsInt = lambda prompt: int(input(prompt))

LEFT_DIR = "./left"
RIGHT_DIR = "./right"
IMAGE_NAME_FORMAT = "/{:06d}.jpg"
LEFT_PATH = LEFT_DIR + IMAGE_NAME_FORMAT
RIGHT_PATH = RIGHT_DIR + IMAGE_NAME_FORMAT

CAMERA_HEIGHT = inputAsInt("Enter camera HEIGHT resolution in pixels (720?): ")

CAMERA_WIDTH = inputAsInt("Enter camera WIDTH resolution in pixels (1280?): ")

print("Camera resolution entered: ({}, {})".format(CAMERA_WIDTH, CAMERA_HEIGHT))

CROP_WIDTH = inputAsInt("Enter crop WIDTH in pixels (960?): ")

CAMERA_RESOLUTION = (CAMERA_WIDTH, CAMERA_HEIGHT)

# CAMERA_WIDTH = 1280
# CAMERA_HEIGHT = 720

# CROP_WIDTH = 960

cam1 = 0
cam2 = 2
dualCam = DualCameraStream(cam1=cam1, cam2=cam2, resolution=CAMERA_RESOLUTION)


def cropHorizontal(image):
    return image[:,
           int((CAMERA_WIDTH - CROP_WIDTH) / 2):
           int(CROP_WIDTH + (CAMERA_WIDTH - CROP_WIDTH) / 2)]


frameId = 0

# capture:
print("Press enter to start taking 64 pictures of the chessboard...")
input()
time.sleep(2)

while frameId != 64:
    leftFrame, rightFrame = dualCam.read()

    leftFrame = cropHorizontal(leftFrame)
    rightFrame = cropHorizontal(rightFrame)

    cv2.imwrite(LEFT_PATH.format(frameId), leftFrame)
    cv2.imwrite(RIGHT_PATH.format(frameId), rightFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frameId += 1
    print(frameId)

    time.sleep(0.125)

# stop cameras and close windows
dualCam.stop()

# calibration:
print("Press enter to continue calibrating...")
input()

CHESSBOARD_HEIGHT = inputAsInt("Enter HEIGHT of chessboard in number of squares: ")

CHESSBOARD_WIDTH = inputAsInt("Enter WIDTH of chessboard in number of squares: ")

print("Chessboard dimensions entered: ({}, {})".format(CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT))

CHESSBOARD_SIZE = (CHESSBOARD_WIDTH, CHESSBOARD_WIDTH)

CHESSBOARD_OPTIONS = (cv2.CALIB_CB_ADAPTIVE_THRESH |
                      cv2.CALIB_CB_NORMALIZE_IMAGE |
                      cv2.CALIB_CB_FAST_CHECK)

OBJECT_POINT_ZERO = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3),
                             np.float32)
OBJECT_POINT_ZERO[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0],
                           0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

OPTIMIZE_ALPHA = 0.25

TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30,
                        0.001)

MAX_IMAGES = 64

leftImageDir = LEFT_PATH
rightImageDir = RIGHT_PATH
outputFile = input("Enter path for storing the calibration configuration file: ")


def readImagesAndFindChessboards(imageDirectory):
    cacheFile = "{0}/chessboards.npz".format(imageDirectory)
    try:
        cache = np.load(cacheFile)
        print("Loading image data from cache file at {0}".format(cacheFile))
        return (list(cache["filenames"]), list(cache["objectPoints"]),
                list(cache["imagePoints"]), tuple(cache["imageSize"]))
    except IOError:
        print("Cache file at {0} not found".format(cacheFile))

    print("Reading images at {0}".format(imageDirectory))
    imagePaths = glob.glob("{0}/*.jpg".format(imageDirectory))

    filenames = []
    objectPoints = []
    imagePoints = []
    imageSize = None

    for imagePath in sorted(imagePaths):
        image = cv2.imread(imagePath)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        newSize = grayImage.shape[::-1]
        if imageSize != None and newSize != imageSize:
            raise ValueError(
                "Calibration image at {0} is not the same size as the others".format(imagePath))
        imageSize = newSize

        hasCorners, corners = cv2.findChessboardCorners(grayImage,
                                                        CHESSBOARD_SIZE, cv2.CALIB_CB_FAST_CHECK)

        if hasCorners:
            filenames.append(os.path.basename(imagePath))
            objectPoints.append(OBJECT_POINT_ZERO)
            cv2.cornerSubPix(grayImage, corners, (11, 11), (-1, -1),
                             TERMINATION_CRITERIA)
            imagePoints.append(corners)

        cv2.drawChessboardCorners(image, CHESSBOARD_SIZE, corners, hasCorners)
        cv2.imshow(imageDirectory, image)

        # Needed to draw the window
        cv2.waitKey(1)

    cv2.destroyWindow(imageDirectory)

    print("Found corners in {0} out of {1} images"
          .format(len(imagePoints), len(imagePaths)))

    np.savez_compressed(cacheFile,
                        filenames=filenames, objectPoints=objectPoints,
                        imagePoints=imagePoints, imageSize=imageSize)
    return filenames, objectPoints, imagePoints, imageSize


(leftFilenames, leftObjectPoints, leftImagePoints, leftSize
 ) = readImagesAndFindChessboards(leftImageDir)
(rightFilenames, rightObjectPoints, rightImagePoints, rightSize
 ) = readImagesAndFindChessboards(rightImageDir)

if leftSize != rightSize:
    print("Camera resolutions do not match")
    sys.exit(1)
imageSize = leftSize

filenames = list(set(leftFilenames) & set(rightFilenames))
if len(filenames) > MAX_IMAGES:
    print("Too many images to calibrate, using {0} randomly selected images"
          .format(MAX_IMAGES))
    filenames = random.sample(filenames, MAX_IMAGES)
filenames = sorted(filenames)
print("Using these images:")
print(filenames)


def getMatchingObjectAndImagePoints(requestedFilenames,
                                    allFilenames, objectPoints, imagePoints):
    requestedFilenameSet = set(requestedFilenames)
    requestedObjectPoints = []
    requestedImagePoints = []

    for index, filename in enumerate(allFilenames):
        if filename in requestedFilenameSet:
            requestedObjectPoints.append(objectPoints[index])
            requestedImagePoints.append(imagePoints[index])

    return requestedObjectPoints, requestedImagePoints


leftObjectPoints, leftImagePoints = getMatchingObjectAndImagePoints(filenames,
                                                                    leftFilenames, leftObjectPoints, leftImagePoints)
rightObjectPoints, rightImagePoints = getMatchingObjectAndImagePoints(filenames,
                                                                      rightFilenames, rightObjectPoints,
                                                                      rightImagePoints)

# TODO: Fix this validation
# Keep getting "Use a.any() or a.all()" even though it's already used?!
# if (leftObjectPoints != rightObjectPoints).all():
#     print("Object points do not match")
#     sys.exit(1)
objectPoints = leftObjectPoints

print("Calibrating left camera...")
_, leftCameraMatrix, leftDistortionCoefficients, _, _ = cv2.calibrateCamera(
    objectPoints, leftImagePoints, imageSize, None, None)
print("Calibrating right camera...")
_, rightCameraMatrix, rightDistortionCoefficients, _, _ = cv2.calibrateCamera(
    objectPoints, rightImagePoints, imageSize, None, None)

print("Calibrating cameras together...")
(_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(
    objectPoints, leftImagePoints, rightImagePoints,
    leftCameraMatrix, leftDistortionCoefficients,
    rightCameraMatrix, rightDistortionCoefficients,
    imageSize, None, None, None, None,
    cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

print("Rectifying cameras...")
# TODO: Why do I care about the disparityToDepthMap?
(leftRectification, rightRectification, leftProjection, rightProjection,
 dispartityToDepthMap, leftROI, rightROI) = cv2.stereoRectify(
    leftCameraMatrix, leftDistortionCoefficients,
    rightCameraMatrix, rightDistortionCoefficients,
    imageSize, rotationMatrix, translationVector,
    None, None, None, None, None,
    cv2.CALIB_ZERO_DISPARITY, OPTIMIZE_ALPHA)

print("Saving calibration...")
leftMapX, leftMapY = cv2.initUndistortRectifyMap(
    leftCameraMatrix, leftDistortionCoefficients, leftRectification,
    leftProjection, imageSize, cv2.CV_32FC1)
rightMapX, rightMapY = cv2.initUndistortRectifyMap(
    rightCameraMatrix, rightDistortionCoefficients, rightRectification,
    rightProjection, imageSize, cv2.CV_32FC1)

np.savez_compressed(outputFile, imageSize=imageSize,
                    leftMapX=leftMapX, leftMapY=leftMapY, leftROI=leftROI,
                    rightMapX=rightMapX, rightMapY=rightMapY, rightROI=rightROI)

cv2.destroyAllWindows()

# stereo depth:
print("Press enter to continue with stereo depth step...")
input()

REMAP_INTERPOLATION = cv2.INTER_LINEAR

DEPTH_VISUALIZATION_SCALE = 2048

if len(sys.argv) != 2:
    print("Syntax: {0} CALIBRATION_FILE".format(sys.argv[0]))
    sys.exit(1)

calibration = np.load(outputFile, allow_pickle=False)

imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

dualCam = DualCameraStream(cam1=cam1, cam2=cam2, framerate=30, resolution=CAMERA_RESOLUTION)


def cropHorizontal(image):
    return image[:, int((CAMERA_WIDTH - CROP_WIDTH) / 2):int(CROP_WIDTH + (CAMERA_WIDTH - CROP_WIDTH) / 2)]


# TODO: Why these values in particular?
# TODO: Try applying brightness/contrast/gamma adjustments to the images
stereoMatcher = cv2.StereoBM_create()
stereoMatcher.setMinDisparity(4)
stereoMatcher.setNumDisparities(128)
stereoMatcher.setBlockSize(21)
stereoMatcher.setROI1(leftROI)
stereoMatcher.setROI2(rightROI)
stereoMatcher.setSpeckleRange(16)
stereoMatcher.setSpeckleWindowSize(45)


# Grab both frames first, then retrieve to minimize latency between cameras
while True:
    leftFrame, rightFrame = dualCam.read()

    leftFrame = cropHorizontal(leftFrame)
    leftHeight, leftWidth = leftFrame.shape[:2]

    rightFrame = cropHorizontal(rightFrame)
    rightHeight, rightWidth = rightFrame.shape[:2]

    if (leftWidth, leftHeight) != imageSize:
        print("Left camera has different size than the calibration data")
        break

    if (rightWidth, rightHeight) != imageSize:
        print("Right camera has different size than the calibration data")
        break

    fixedLeft = cv2.remap(leftFrame, leftMapX, leftMapY, REMAP_INTERPOLATION)
    fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)

    grayLeft = cv2.cvtColor(fixedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(fixedRight, cv2.COLOR_BGR2GRAY)
    depth = stereoMatcher.compute(grayLeft, grayRight)

    cv2.imshow('left', fixedLeft)
    cv2.imshow('right', fixedRight)
    cv2.imshow('depth', depth / DEPTH_VISUALIZATION_SCALE)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

dualCam.stop()
