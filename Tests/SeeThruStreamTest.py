from StereoCameraAPIs.OldMonoLensStream import OldMonoLensStream
import cv2
import time


left = OldMonoLensStream(src=0, framerate=30, resolution=(320, 240)).start()
right = OldMonoLensStream(src=0, framerate=30, resolution=(320, 240)).start()

iterCount = 1000
iterNum = iterCount
avg = 0
maxDelay = 0
minDelay = 0

while True:
    cur_time_in_micro = time.time() * 1000 * 1000
    leftFrame = left.read()
    cur_time_in_micro2 = time.time() * 1000 * 1000
    rightFrame = right.read()
    cur_time_in_micro3 = time.time() * 1000 * 1000

    print(cur_time_in_micro2 - cur_time_in_micro)
    iterNum -= 2
    curDiff = cur_time_in_micro2 - cur_time_in_micro
    avg += curDiff
    avg += cur_time_in_micro3 - cur_time_in_micro2

    if curDiff > maxDelay:
        maxDelay = curDiff

    if minDelay == 0:
        minDelay = curDiff

    if curDiff < minDelay:
        minDelay = curDiff

    if iterNum == 0:
        break

    # show the output frame
    cv2.imshow("Frame1", leftFrame)
    cv2.imshow("Frame2", rightFrame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

print("average is {} usec".format(avg / iterCount))
print("max is {} usec".format(maxDelay))
print("min is {} usec".format(minDelay))

# do a bit of cleanup
left.stop()
right.stop()
cv2.destroyAllWindows()
