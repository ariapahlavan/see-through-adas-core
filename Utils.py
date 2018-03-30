import cv2


def CloseWhenPressed(windowName, keyToWaitOn='q'):
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyWindow(windowName)


def CloseAllWhenPressed(keyToWaitOn='q'):
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyAllWindows()


def ShowImgAndCloseWhen(im, windowName="image", keyToWaitOn='q'):
    cv2.imshow(windowName, im)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyWindow(windowName)


def ShowImgAndCloseAllWhen(im, windowName="image", keyToWaitOn='q'):
    cv2.imshow(windowName, im)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord(keyToWaitOn):
            break

    cv2.destroyAllWindows()


def ShowImg(im, windowName="image"): cv2.imshow(windowName, im)


def PatchImages(bgImg, fgImg):
    grayed = cv2.cvtColor(fgImg, cv2.COLOR_BGR2GRAY)
    _, grayed = cv2.threshold(grayed, 0, 255, cv2.THRESH_BINARY)
    grayedInv = cv2.bitwise_not(grayed)
    # cv2.imshow("maskOfFront", grayed)

    bgfinal = cv2.bitwise_and(bgImg, bgImg, mask=grayedInv)
    fgfinal = cv2.bitwise_and(fgImg, fgImg, mask=grayed)

    finalImage = cv2.add(bgfinal, fgfinal)

    return finalImage


def ShrinkBy(im, numpixels):
    h, w, _ = im.shape
    return im[numpixels:(h - numpixels), numpixels:(w - numpixels)]
