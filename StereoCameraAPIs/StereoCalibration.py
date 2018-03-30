from StereoCameraAPIs.StereoCameraStream import StereoCameraStream

import numpy as np
import cv2

import time
import random
import sys
import glob
import os

inputAsInt = lambda prompt, default_value: int(input(prompt) or default_value)

LEFT_DIR = "./left"
RIGHT_DIR = "./right"


def createDir(path, name):
    try:
        os.mkdir(path)
    except IOError:
        print("{} directory already exist.".format(name))


createDir(LEFT_DIR, "left")
createDir(RIGHT_DIR, "right")

IMAGE_NAME_FORMAT = "/{:06d}.jpg"
leftPath = LEFT_DIR + IMAGE_NAME_FORMAT
rightPath = RIGHT_DIR + IMAGE_NAME_FORMAT

cameraHeight = DEFAULT_HEIGHT = 720
cameraWidth = DEFAULT_WIDTH = 1280
cropWidth = DEFAULT_CROP_WIDTH = 960
CAMERA_RESOLUTION = (cameraWidth, cameraHeight)

cam1 = DEFAULT_CAM1 = 0
cam2 = DEFAULT_CAM2 = 2

numSamples = DEFAULT_NUM_SAMPLES = 64

chessboardHeight = DEFAULT_CHESSBOARD_HEIGHT = 4
chessboardWidth = DEFAULT_CHESSBOARD_WIDTH = 5

OPTIMIZE_ALPHA = 0.25

outputFile = DEFAULT_OUTPUT_FILE = "./StereoCalibrationConfigs.npz"


if input("Change default setting? (\'y\')") == "y":
    cameraHeight = inputAsInt("Enter camera HEIGHT resolution in pixels ({}): ".format(DEFAULT_HEIGHT), DEFAULT_HEIGHT)
    cameraWidth = inputAsInt("Enter camera WIDTH resolution in pixels ({}): ".format(DEFAULT_WIDTH), DEFAULT_WIDTH)
    print("Camera resolution entered: ({}, {})".format(cameraWidth, cameraHeight))

    cropWidth = inputAsInt("Enter crop WIDTH in pixels ({}): ".format(DEFAULT_CROP_WIDTH), DEFAULT_CROP_WIDTH)
    CAMERA_RESOLUTION = (cameraWidth, cameraHeight)

    cam1 = inputAsInt("Enter camera 1 source ({}): ".format(DEFAULT_CAM1), DEFAULT_CAM1)
    cam2 = inputAsInt("Enter camera 2 source ({}): ".format(DEFAULT_CAM2), DEFAULT_CAM2)
    print("Cameras to be used are {} and {}".format(cam1, cam2))

    numSamples = inputAsInt("Enter the number of frames to capture ({}): ".format(DEFAULT_NUM_SAMPLES),
                            DEFAULT_NUM_SAMPLES)

    chessboardHeight = inputAsInt(
        "Enter HEIGHT of chessboard in number of squares ({}): ".format(DEFAULT_CHESSBOARD_HEIGHT),
        DEFAULT_CHESSBOARD_HEIGHT)

    chessboardWidth = inputAsInt(
        "Enter WIDTH of chessboard in number of squares ({}): ".format(DEFAULT_CHESSBOARD_WIDTH),
        DEFAULT_CHESSBOARD_WIDTH)

    print("Chessboard dimensions entered: ({}, {})".format(chessboardWidth, chessboardHeight))

    outputFile = (
            input("Enter path for storing the calibration configuration file ({}): ".format(DEFAULT_OUTPUT_FILE)) or
            DEFAULT_OUTPUT_FILE)


def cropHorizontal(image):
    return image[:,
           int((cameraWidth - cropWidth) / 2):
           int(cropWidth + (cameraWidth - cropWidth) / 2)]


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


if input("Recapture chessboard images? (\'y\')") == "y":
    # capture:
    input("Press enter to start taking {} pictures of the chessboard...".format(numSamples))
    time.sleep(2)

    dualCam = StereoCameraStream(cam1=cam1, cam2=cam2, resolution=CAMERA_RESOLUTION)

    frameId = 0

    while frameId != numSamples:
        leftFrame, rightFrame = dualCam.read()

        leftFrame = cropHorizontal(leftFrame)
        rightFrame = cropHorizontal(rightFrame)

        cv2.imwrite(leftPath.format(frameId), leftFrame)
        cv2.imwrite(rightPath.format(frameId), rightFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frameId += 1
        print(frameId)

        # time.sleep(0.125)

    # stop cameras and close windows
    dualCam.stop()

if input("Recalibrate the camera? (\'y\')") == "y":
    # calibration:
    input("Press enter to continue calibrating...")

    CHESSBOARD_SIZE = (chessboardWidth, chessboardHeight)

    CHESSBOARD_OPTIONS = (cv2.CALIB_CB_ADAPTIVE_THRESH |
                          cv2.CALIB_CB_NORMALIZE_IMAGE |
                          cv2.CALIB_CB_FAST_CHECK)

    OBJECT_POINT_ZERO = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3),
                                 np.float32)
    OBJECT_POINT_ZERO[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0],
                               0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

    TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30,
                            0.001)

    MAX_IMAGES = numSamples

    leftImageDir = LEFT_DIR
    rightImageDir = RIGHT_DIR

    print("The output file is: '{}'".format(outputFile))

    (leftFilenames, leftObjectPoints, leftImagePoints, leftSize) = readImagesAndFindChessboards(leftImageDir)
    (rightFilenames, rightObjectPoints, rightImagePoints, rightSize) = readImagesAndFindChessboards(rightImageDir)

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

    leftObjectPoints, leftImagePoints = \
        getMatchingObjectAndImagePoints(filenames, leftFilenames, leftObjectPoints, leftImagePoints)

    rightObjectPoints, rightImagePoints = \
        getMatchingObjectAndImagePoints(filenames, rightFilenames, rightObjectPoints, rightImagePoints)

    # TODO: Fix this validation
    # Keep getting "Use a.any() or a.all()" even though it's already used?!
    # if (leftObjectPoints != rightObjectPoints).all():
    #     print("Object points do not match")
    #     sys.exit(1)
    objectPoints = leftObjectPoints

    print("Calibrating left camera...")
    _, leftCameraMatrix, leftDistortionCoefficients, _, _ = \
        cv2.calibrateCamera(objectPoints, leftImagePoints, imageSize, None, None)

    print("Calibrating right camera...")
    _, rightCameraMatrix, rightDistortionCoefficients, _, _ = \
        cv2.calibrateCamera(objectPoints, rightImagePoints, imageSize, None, None)

    print("Calibrating cameras together...")
    (_, _, _, _, _, rotationMatrix, translationVector, _, _) = \
        cv2.stereoCalibrate(objectPoints, leftImagePoints, rightImagePoints,
                            leftCameraMatrix, leftDistortionCoefficients,
                            rightCameraMatrix, rightDistortionCoefficients,
                            imageSize, None, None, None, None,
                            cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

    print("Rectifying cameras...")
    # TODO: Why do I ccdare about the disparityToDepthMap?
    (leftRectification, rightRectification, leftProjection, rightProjection, dispartityToDepthMap, leftROI, rightROI) = \
        cv2.stereoRectify(leftCameraMatrix, leftDistortionCoefficients,
                          rightCameraMatrix, rightDistortionCoefficients,
                          imageSize, rotationMatrix, translationVector,
                          None, None, None, None, None,
                          cv2.CALIB_ZERO_DISPARITY, OPTIMIZE_ALPHA)

    print("Saving calibration...")
    leftMapX, leftMapY = \
        cv2.initUndistortRectifyMap(leftCameraMatrix, leftDistortionCoefficients,
                                    leftRectification, leftProjection, imageSize,
                                    cv2.CV_32FC1)

    rightMapX, rightMapY = \
        cv2.initUndistortRectifyMap(rightCameraMatrix, rightDistortionCoefficients,
                                    rightRectification, rightProjection, imageSize,
                                    cv2.CV_32FC1)

    np.savez_compressed(outputFile, imageSize=imageSize, leftMapX=leftMapX,
                        leftMapY=leftMapY, leftROI=leftROI, rightMapX=rightMapX,
                        rightMapY=rightMapY, rightROI=rightROI)

    cv2.destroyAllWindows()

# stereo depth:
input("Press enter to continue with stereo depth step...")

REMAP_INTERPOLATION = cv2.INTER_LINEAR

DEPTH_VISUALIZATION_SCALE = 2048

calibration = np.load(outputFile, allow_pickle=False)

imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

dualCam = StereoCameraStream(cam1=cam1, cam2=cam2, framerate=30, resolution=CAMERA_RESOLUTION)

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

LEFT_DIR = "./left/img"
RIGHT_DIR = "./right/img"
DEPTH_DIR = "./depth/img"
counter = 0
fmt = ".jpg"

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

    cv2.imwrite("{}{}{}".format(LEFT_DIR, counter, fmt), fixedLeft)

    cv2.imwrite("{}{}{}".format(RIGHT_DIR, counter, fmt), fixedRight)
    cv2.imwrite("{}{}{}".format(DEPTH_DIR, counter, fmt), depth / DEPTH_VISUALIZATION_SCALE)

    counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

dualCam.stop()
