import cv2

img1 = cv2.imread('t1/img1.jpg')
height , width , layers =  img1.shape

fourcc = cv2.VideoWriter_fourcc(*'X264')
video = cv2.VideoWriter('stitched_video.mp4',fourcc,7.0,(width,height))

frame_num = 1
while (frame_num <= 3000):
	frame_name = "t1/img" + str(frame_num) + ".jpg"
	img = cv2.imread(frame_name)
	video.write(img)
	frame_num += 1

frame_num = 1
while (frame_num <= 1545):
	frame_name = "t2/img" + str(frame_num) + ".jpg"
	img = cv2.imread(frame_name)
	video.write(img)
	frame_num += 1

frame_num = 1
while (frame_num <= 2008):
	frame_name = "t3/img" + str(frame_num) + ".jpg"
	img = cv2.imread(frame_name)
	video.write(img)
	frame_num += 1

cv2.destroyAllWindows()
video.release()
