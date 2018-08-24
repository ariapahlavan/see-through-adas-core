# Standard imports
import cv2
import numpy as np

# Read images
from Utils import ShowImgAndCloseWhen as show


def fixed(im):
    return cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(im)))


src = fixed(cv2.imread("airplane.jpg"))
dst = cv2.pyrDown(cv2.imread("sky.jpg"))

# Create a rough mask around the airplane.
h, w, l = src.shape
src_mask = np.zeros(src.shape, src.dtype)
DX = 20
DY = 50
src_mask[DY:h-DY, DX:w-DX] = (255, 255, 255)

show(src_mask)
poly = np.array([[4, 80], [30, 54], [151, 63], [254, 37], [298, 90], [272, 134], [43, 122]], np.int32)
cv2.fillPoly(src_mask, [poly], (255, 255, 255))
show(src_mask)

# This is where the CENTER of the airplane will be placed
center = (800, 100)

# Clone seamlessly.
output = cv2.seamlessClone(src, dst, src_mask, center, cv2.MIXED_CLONE)

# Save result
cv2.imwrite("opencv-seamless-cloning-example.jpg", output)
