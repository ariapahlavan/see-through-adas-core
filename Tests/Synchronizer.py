import cv2

frameDiff = (9371 / 3379) + 0.5
print(frameDiff)

fcounter = 1
bcounter = 1
counter = 1
while True:
    # if fcounter >= 12148 or bcounter >= 6476:
    #     break
    #
    # # fg = cv2.imread("/Users/ariapahlavan/Google Drive/Senior Design /Test Data/left_frontcar/img{}.jpg".format(counter))
    # front = cv2.imread("left_frontcar/img{}.jpg".format(int(fcounter)))
    # back = cv2.imread("left_backcar/img{}.jpg".format(bcounter))
    # # back = cv2.pyrDown(back)
    # # front = cv2.pyrDown(front)
    # # cv2.imshow("front", front)
    # # cv2.imshow("back", back)
    # cv2.imwrite("frontKindaSynch2/img{}.jpg".format(bcounter), front)
    # cv2.imwrite("backKindaSynch2/img{}.jpg".format(bcounter), back)
    # fcounter += frameDiff
    # bcounter += 1
    # print(bcounter)

    # front = cv2.imread("frontKindaSynch2/img{}.jpg".format(counter))
    # back = cv2.imread("backKindaSynch2/img{}.jpg".format(counter))
    # back = back
    # front = cv2.pyrDown(cv2.pyrDown(front))
    # cv2.imshow("front", front)
    # cv2.imshow("back", back)
    # counter += 1

    # sleep(1/60)

    front = cv2.imread("left1_frontcar/img{}.jpg".format(fcounter))
    back = cv2.imread("left1_backcar/img{}.jpg".format(int(bcounter)))
    back = back
    front = cv2.pyrDown(cv2.pyrDown(front))
    cv2.imshow("front", front)
    cv2.imshow("back", back)
    fcounter += 1
    bcounter += frameDiff

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
