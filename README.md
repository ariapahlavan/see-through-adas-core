# see-through-video-stitching

See-through display for automated driver assistance system (ADAS) utilizing input information from a stereo camera on the front car and a stero camera on the back car. Images are passed through the You Only Look Once v3 (YOLOv3) convolutional neural network to classify and localize objects of interest in the video files. Video files are then stitched together such that the front car camera feed is stitched onto the front car in the back car camera feed, providing a see-through view. The system is composed of 4 different subsystems: synchronization subsystem, object recognition subsystem, video stitching subsystem, GUI application subsystem.

## Object Recognition Subsystem 

The object recognition subsystem is composed of the YOLOv3 convolutional neural network as well as code to determine the efficiency of the CNN utilizing the mean average precision (mAP) score.

### YOLOv3

YOLOv3 is created by pjreddie and was utilized for this project as its object recognition subsystem's recognition network. To utilize this CNN, clone the pjreddie's repository form: https://github.com/pjreddie/darknet
Take the image.c file from the repository and replace the image.c file in the src folder in the darknet repository and run the neural network accordingly. 

### mAP

mAP was generated utilizing the github repository: https://github.com/Cartucho/mAP 
The predicted image files are generated using the detection.sh shell script which will generate the predicted image files. 
