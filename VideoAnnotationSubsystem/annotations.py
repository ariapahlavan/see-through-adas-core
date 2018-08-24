import numpy as np
import cv2
import math
from random import *
from functools import reduce

def fcWarning(down, image_h, image_w, counter,
              lst):  # possibly pass in counter as an argument since global variables are poo poo
    # horizon is the y value that dictates the horizon of the image unit is meters
    horizon = 200.0
    # vertical center of image
    x_center = image_w / 2
    # used to convert pixels to meters
    conversion_factor = float(math.sqrt(math.pow(image_h, 2) + math.pow(x_center, 2))) / float(horizon)
    # calculated converted distance of meters
    conversion_distance = 0
    # distancee between detected vehicle lower bound and bottom of image frame
    delta_y = image_h - down

    if counter != 0:
        # calculate conversion_distance for specific image frame
        conversion_distance = (float(delta_y) / float(image_h)) * float(horizon)
        # print("conversion distance: " + str(conversion_distance))
        lst.append(conversion_distance)
        return "checking"
    elif counter == 0:
        print(lst)
        delta_c = 0  # sum(lst) / len(lst)
        for i in range(0, len(lst) - 1):
            delta_c += lst[i + 1] - lst[i]

        first_distance = lst[0]
        print("First distance: " + str(first_distance * 0.15))
        print("Delta Average Conversion distance: " + str(delta_c))
        if (first_distance * (0.15) < (-1 * delta_c)):
            return "collision"
        else:
            return "no collision"


def main():
    cap = cv2.VideoCapture('stitched_video.mp4')
    frame_num = 0

    img1 = cv2.imread('img1-test.jpg')
    height, width, layers = img1.shape

    # split text file by new line
    with open('test1_front.txt', 'r') as myfile:
        data = myfile.read()
    frames_front = data.split('-')

    with open('test1_back.txt', 'r') as myfile:
        data = myfile.read()
    frames_back = data.split('-')

    # object_name,left,top,right,bot

    stop_count = 0
    light_count = 0
    ped_count = 0
    collision_count = 10
    lst = []
    collision_status = None

    while (cap.isOpened()):
        ret, frame = cap.read()

        objects_front = frames_front[frame_num]
        objects_back = frames_back[frame_num]

        # collision warning implementation
        objects_back_separate = objects_back.split("\n")
        if not objects_back_separate:
            midline = width / 2
            current_object = objects_back_separate[0]
            current_distance = midline
            for line in objects_back_separate:
                parameters = line.split(",")
                if (parameters[0] == 'car'):
                    object_middle = int(parameters[1]) + (int(parameters[3]) - int(parameters[1])) / 2
                    if (abs(midline - object_middle) < current_distance):
                        current_object = line
                        current_distance = abs(midline - object_middle)
            coordinates = current_object.split(",")
            print(current_object)
            collision_status = fcWarning(int(coordinates[4]), height, width, collision_count, lst)

        # traffic light improvement
        proper_light = True
        if 'traffic light' in objects_front:
            objects_front_light = objects_front.split("\n")
            for line in objects_front_light:
                if 'traffic light' in line:
                    params = line.split(',')
                    if (int(params[1]) < 50 or int(params[3]) > width-50):
                        proper_light = False

        # pedestrian
        overlay = frame.copy()
        pedestrian = frame.copy()
        alpha = 0.3
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 255), -1)
        cv2.addWeighted(overlay, alpha, pedestrian, 1 - alpha, 0, pedestrian)
        s_img = cv2.imread("pedestrian_icon.png")
        x_offset = y_offset = 20
        pedestrian[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

        # stop sign
        overlay = frame.copy()
        stop = frame.copy()
        alpha = 0.3
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 255, 255), -1)
        cv2.addWeighted(overlay, alpha, stop, 1 - alpha, 0, stop)
        s_img = cv2.imread("stopsign_icon.png")
        x_offset = 20
        y_offset = int(height / 2) - 50
        stop[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

        # traffic light
        overlay = frame.copy()
        light = frame.copy()
        alpha = 0.3
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 255, 255), -1)
        cv2.addWeighted(overlay, alpha, light, 1 - alpha, 0, light)
        s_img = cv2.imread("trafficlight_icon.png")
        x_offset = 20
        y_offset = int(height / 2) - 50
        light[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

        # collision
        overlay = frame.copy()
        collision = frame.copy()
        alpha = 0.3
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 255), -1)
        cv2.addWeighted(overlay, alpha, collision, 1 - alpha, 0, collision)
        s_img = cv2.imread("collision_icon.png")
        x_offset = y_offset = 20
        collision[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

        image_name = "img" + str(frame_num) + ".jpg"

        if 'person' in objects_front or 'person' in objects_back or ped_count > 0:
            cv2.imwrite(image_name,pedestrian)
            ped_count += 1
            if (ped_count > 5):
                ped_count = 0
        elif collision_status == "collision":
            cv2.imwrite(image_name, collision)
            collision_count = 11
            lst = []
        elif 'stop sign' in objects_front or 'stop sign' in objects_back or stop_count > 0:
            cv2.imwrite(image_name, stop)
            stop_count += 1
            if (stop_count > 5):
                stop_count = 0
        elif ('traffic light' in objects_front or light_count > 0) and proper_light is True:
            cv2.imwrite(image_name, light)
            light_count += 1
            if (light_count > 5):
                light_count = 0
        else:
            cv2.imwrite(image_name, frame)

        frame_num += 1

        # check if there is no collision which means 10 frames so reset lst and count
        if (collision_status == "no collision"):
            collision_count = 11
            lst = []
        collision_count -= 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
