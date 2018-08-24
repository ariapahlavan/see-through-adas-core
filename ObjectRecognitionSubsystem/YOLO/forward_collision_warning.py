import math
from random import *
from functools import reduce

# returns checking if counter isnt 0. If counter is 0 return no collision if there isnt a collision, else return collision
def fcWarning(left, right, up, down, image_h, image_w, counter, lst): # possibly pass in counter as an argument since global variables are poo poo
	# horizon is the y value that dictates the horizon of the image
	horizon = 200.0
	# vertical center of image
	x_center = image_w / 2
	# used to convert pixels to meters
	conversion_factor = float(math.sqrt(math.pow(image_h,2) + math.pow(x_center,2))) / float(horizon)
	# calculated converted distance of meters
	conversion_distance = 0
	# distancee between detected vehicle lower bound and bottom of image frame
	delta_y = image_h - down

	
	
	if(counter != 0):
		# calculate conversio_distance for specific image frame
		conversion_distance = (float(delta_y) / float(image_h)) * float(horizon)
		#print("conversion distance: " + str(conversion_distance))
		lst.append(conversion_distance)
		return "checking"
	elif(counter == 0):
		average_conversion_distance = sum(lst) / len(lst)
		delta_average_conversion_distance = average_conversion_distance / float(10)
		#counter = number_of_images_processed_together
		first_distance = lst[0]
		print("First distance: " + str(first_distance * 0.15))
		print("Delta Average Conversion distance: " + str(delta_average_conversion_distance))
		if(first_distance * (0.15) < delta_average_conversion_distance):
			return "no collision"
		else:
			return "collision"
		
		

def main():
	# testing done in main. Change different variables to test for different collision instances
	counter = 10
	x = 500
	i = 0
	lst = []
	while(i <= 10):
		i += 1
		print("Counter: " + str(counter))
		warning = fcWarning(100,200,300,x, 720, 1280, counter, lst)
		if(randint(0,1) == 0):
			x += 1
		else:
			x -= 1
			
		counter -= 1

		if(warning == "checking"):
			pass
		elif(warning == "collision"):
			print("Collision!")
			counter = 10
			lst = []
		elif(warning == "no collision"):
			print("No Collision")
			counter = 10
			lst = []
		
if __name__ == "__main__":
	main()