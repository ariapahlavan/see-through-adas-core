import numpy as np
import cv2

cap = cv2.VideoCapture("test.mp4")


def transformPerspective(bgImg, fgImg):
    fgHeight, fgWidth, _ = fgImg.shape
    fgImageCoords = np.array([(0, 0),
                              (0, fgHeight),
                              (fgWidth, fgHeight),
                              (fgWidth, 0)])
    x0 = 550
    x1 = x0+200
    y0 = 270
    y1 = y0+200
    stitchingCoords = np.array([(x0, y0),
                                (x0, y1),
                                (x1, y1),
                                (x1, y0)])
    print("fgImageCoords:\n{}".format(fgImageCoords))
    print("stitchingCoords:\n{}".format(stitchingCoords))
    homography, _ = cv2.findHomography(fgImageCoords, stitchingCoords, 0)

    bgHeight, bgWidth, _ = bgImg.shape
    projectedIm = cv2.warpPerspective(src=fgImg, M=homography, dsize=(bgWidth, bgHeight))

    from VideoStitchingAPIs.FrameStitch import PatchImages
    finalImg = PatchImages(bgImg, projectedIm)
    cv2.imshow("stitched_no_blend", finalImg)


fg = cv2.imread("./front.jpg")
while True:

    _, leftFrame = cap.read()

    # show the output frame
    transformPerspective(leftFrame, leftFrame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
