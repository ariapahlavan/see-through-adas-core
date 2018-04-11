import cv2


# Credits: https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


IN_DIR = "Tests/"
BACK_PATH = "{}backSynch".format(IN_DIR)
FRONT_PATH = "{}frontSynch".format(IN_DIR)
IMG_NAME = "img"
IMG_FORMAT = ".jpg"

pathOf = lambda path, name, index, fmt: "{}/{}{}{}".format(path, name, index, fmt)
imgPathOf = lambda path, index: pathOf(path, IMG_NAME, index, IMG_FORMAT)
backPathOf = lambda index: imgPathOf(BACK_PATH, index)
frontPathOf = lambda index: imgPathOf(FRONT_PATH, index)

frameCount = 1

if __name__ == '__main__':

    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[5]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()

    # Define an initial bounding box
    x0 = 501
    y0 = 381
    x1 = 792
    y1 = 553
    frame = cv2.imread(backPathOf(1))
    bbox = (x0, y0, x1-x0, y1-y0)

    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        timer = cv2.getTickCount()

        frame = cv2.imread(backPathOf(frameCount))
        frameCount += 1

        ok, bbox = tracker.update(frame)

        from Utils import FpsOf
        fps = FpsOf(timer)

        # Draw bounding box
        # if ok:
            # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        # else:
        #     Tracking failure
            # cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 50, 50), 2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 50, 50), 2)

        cv2.imshow("Tracking", frame)

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break
