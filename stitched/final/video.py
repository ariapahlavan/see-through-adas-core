import cv2

img1 = cv2.imread('img1.jpg')
height , width , layers =  img1.shape

fourcc = cv2.VideoWriter_fourcc(*'X264')
video = cv2.VideoWriter('stitched_video.mp4',fourcc,7.0,(width,height))

frame_num = 1
while (frame_num <= 6552):
	frame_name = "img" + str(frame_num) + ".jpg"
	img = cv2.imread(frame_name)
	video.write(img)
	frame_num += 1

cv2.destroyAllWindows()
video.release()
