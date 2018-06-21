#!/bin/bash

# path to the darknet directory
# you may want to change this path so that it path's correctly
directory=

cd $directory

# set this to the number of photos in the directory that contains photos to be detected over
number_of_photos=


for ((i = 1; i <= $number_of_photos; ++i)); do
	# change the last argument in the line below to path to the image directory that contains the images to be detected
	# keep the "img${i}.jpg which should capture the images 
	# images should be named image1.jpg / image2.jpg / image3.jpg 
	./darknet detect cfg/yolov3.cfg yolov3.weights "data/front-test-0/img${i}.jpg"
	echo $path
	
	# if you want to save the detected images in a different directory
	# change the data/test/$i variable to the directory of choice
	cp predictions.png data/test/$i.png
	
done


