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
