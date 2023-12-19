import cv2 
import sys
import numpy as np 
from PIL import Image
import pyautogui
import time


"""
The total number of seconds the yellow strip takes to countdown is: 15 - 18 seconds.
"""

class IsItMyTurnToAct:

	def __init__(self):
		self.guy_to_right_turn = False

	def randomiser(self): 
		"""
		To prevent pokerbros detecting that I am a bot, I should randomise when I act. 
		I can do this by acting on certain yellow strips.
		"""
		pass

	def detect_yellow_strip(self, image): 
		"""
		If a yellow strip is detected this function returns True

		"""
		pixels = list(image.getdata())

		pixel_colour = []
		R_pixels = []
		G_pixels = []
		B_pixels = []

		yellow_count = 0 
		non_yellow_count = 0 

		for pixel in pixels:
			R,G,B,C = pixel
			if R >= (2*B) and G >= (2*B):  # this is a yellow strip! 
				yellow_count += 1
			else: 
				non_yellow_count += 1

		if yellow_count > non_yellow_count: 
			return True



	# def is_it_guy_to_right_to_act(self, guy_to_my_right_still_in_pot_position, my_position): 
	# 	"""
	# 	Grab the four sides that will glow yellow when it is someone's turn to act. 

	# 	I will need to analyse the strips of all players because what if the two peopple to my left folded, then I'll 
	# 	need to detect the strip of the guy at the top of the screen. 

	# 	Since it takes a while for all the scripts to run, let's start running everything when it is the guy to my right's turn to act. 
	# 	Then I'll just need to check if he has bet or folded; I think this will be the only thing missing if I run the scripts when 
	# 	it is his turn to act.

	# 	Can use the fact that I calculated who is left in the top and take the person to my 'closest' right who is still in pot. 


	# 	Just like everything else, I will need to add these strips into relative position, so I can see which strips belongs to which relative seat.
	#     """

	# 	# guy to my left
	# 	right_guy5_top_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/top5_yellow_strip.png", region=(337,1155, 170, 10))
	# 	right_guy5_right_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/right5_yellow_strip.png", region=(495,1155, 10, 90))
	# 	right_guy5_bottom_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/bottom5_yellow_strip.png", region=(337,1233, 170, 10))
	# 	right_guy5_left_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/left5_yellow_strip.png", region=(337,1155, 10, 72))

	# 	right_guy5_image_top = Image.open(f"{sys.path[0]}/photo_dump/top5_yellow_strip.png", "r")
	# 	right_guy5_image_right = Image.open(f"{sys.path[0]}/photo_dump/right5_yellow_strip.png", "r")
	# 	right_guy5_image_bottom = Image.open(f"{sys.path[0]}/photo_dump/bottom5_yellow_strip.png", "r")
	# 	right_guy5_image_left = Image.open(f"{sys.path[0]}/photo_dump/left5_yellow_strip.png", "r")


	# 	# guy to my left + 2
	# 	right_guy4_top_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/top4_yellow_strip.png", region=(397,692, 155, 6))
	# 	right_guy4_right_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/right4_yellow_strip.png", region=(543,688, 10, 80))
	# 	right_guy4_bottom_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/bottom4_yellow_strip.png", region=(397,767, 155, 10))
	# 	right_guy4_left_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/left4_yellow_strip.png", region=(397,697, 10, 72))

	# 	right_guy4_image_top = Image.open(f"{sys.path[0]}/photo_dump/top4_yellow_strip.png", "r")
	# 	right_guy4_image_right = Image.open(f"{sys.path[0]}/photo_dump/right4_yellow_strip.png", "r")
	# 	right_guy4_image_bottom = Image.open(f"{sys.path[0]}/photo_dump/bottom4_yellow_strip.png", "r")
	# 	right_guy4_image_left = Image.open(f"{sys.path[0]}/photo_dump/left4_yellow_strip.png", "r")


	# 	# guy top of screen
	# 	right_guy3_top_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/top3_yellow_strip.png", region=(747,424, 85, 6))
	# 	right_guy3_right_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/right3_yellow_strip.png", region=(823,425, 10, 80))
	# 	right_guy3_bottom_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/bottom3_yellow_strip.png", region=(690,497, 155, 10))
	# 	right_guy3_left_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/left3_yellow_strip.png", region=(680,426, 10, 72))

	# 	right_guy3_image_top = Image.open(f"{sys.path[0]}/photo_dump/top3_yellow_strip.png", "r")
	# 	right_guy3_image_right = Image.open(f"{sys.path[0]}/photo_dump/right3_yellow_strip.png", "r")
	# 	right_guy3_image_bottom = Image.open(f"{sys.path[0]}/photo_dump/bottom3_yellow_strip.png", "r")
	# 	right_guy3_image_left = Image.open(f"{sys.path[0]}/photo_dump/left3_yellow_strip.png", "r")


	# 	# guy top of screen + 1
	# 	right_guy2_top_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/top2_yellow_strip.png", region=(960, 692, 155, 10))
	# 	right_guy2_right_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/right2_yellow_strip.png", region=(1107,692, 10, 80))
	# 	right_guy2_bottom_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/bottom2_yellow_strip.png", region=(960,769, 155, 10))
	# 	right_guy2_left_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/left2_yellow_strip.png", region=(960,695, 10, 72))

	# 	right_guy2_image_top = Image.open(f"{sys.path[0]}/photo_dump/top2_yellow_strip.png", "r")
	# 	right_guy2_image_right = Image.open(f"{sys.path[0]}/photo_dump/right2_yellow_strip.png", "r")
	# 	right_guy2_image_bottom = Image.open(f"{sys.path[0]}/photo_dump/bottom2_yellow_strip.png", "r")
	# 	right_guy2_image_left = Image.open(f"{sys.path[0]}/photo_dump/left2_yellow_strip.png", "r")



	# 	# guy top of screen + 2
	# 	right_guy_top_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/right_guy_top_yellow_strip.png", region=(1013, 1150, 167, 10))
	# 	right_guy_right_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/right_yellow_strip.png", region=(1167,1153, 10, 85))
	# 	right_guy_bottom_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/bottom_yellow_strip.png", region=(1013,1235, 170, 10))
	# 	right_guy_left_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/left_yellow_strip.png", region=(1010,1158, 10, 72))

	# 	right_guy_image_top = Image.open(f"{sys.path[0]}/photo_dump/right_guy_top_yellow_strip.png", "r")
	# 	right_guy_image_right = Image.open(f"{sys.path[0]}/photo_dump/right_yellow_strip.png", "r")
	# 	right_guy_image_bottom = Image.open(f"{sys.path[0]}/photo_dump/bottom_yellow_strip.png", "r")
	# 	right_guy_image_left = Image.open(f"{sys.path[0]}/photo_dump/left_yellow_strip.png", "r")



	# 	relative_position_of_strips = dict()



	# 	# Each of these lists will just hold 4 items that consist of either True or False.
	# 	guy_to_my_left = [self.detect_yellow_strip(right_guy5_image_top), self.detect_yellow_strip(right_guy5_image_right), self.detect_yellow_strip(right_guy5_image_bottom), self.detect_yellow_strip(right_guy5_image_left)]
	# 	guy_to_my_left_plus_2 = [self.detect_yellow_strip(right_guy4_image_top), self.detect_yellow_strip(right_guy4_image_right), self.detect_yellow_strip(right_guy4_image_bottom), self.detect_yellow_strip(right_guy4_image_left)]
	# 	guy_top_of_screen = [self.detect_yellow_strip(right_guy3_image_top), self.detect_yellow_strip(right_guy3_image_right), self.detect_yellow_strip(right_guy3_image_bottom), self.detect_yellow_strip(right_guy3_image_left)]
	# 	guy_top_of_screen_plus_one = [self.detect_yellow_strip(right_guy2_image_top), self.detect_yellow_strip(right_guy2_image_right), self.detect_yellow_strip(right_guy2_image_bottom), self.detect_yellow_strip(right_guy2_image_left)]
	# 	guy_top_of_screen_plus_two = [self.detect_yellow_strip(right_guy_image_top), self.detect_yellow_strip(right_guy_image_right), self.detect_yellow_strip(right_guy_image_bottom), self.detect_yellow_strip(right_guy_image_left)]

	# 	strips = [my_strips, guy_to_my_left, guy_to_my_left_plus_2, guy_top_of_screen, guy_top_of_screen_plus_one, guy_top_of_screen_plus_two]


	# 	# Assign strips to each player in their relative position
	# 	for strip_pos in range(6):
	# 		relative_position_of_strips[my_position] = strips[strip_pos]

	# 		my_position += 1

	# 		my_position %= 7

	# 		if my_position == 0: 
	# 			my_position = 1


	# 	# Check the strips of guy to my right, if any are True it means it's his turn to act
	# 	if any(i for i in relative_position_of_strips[guy_to_my_right_still_in_pot_position]):
	# 		# Start running script
	# 		self.guy_to_right_turn = True
	# 	else: 
	# 		# Do not run script yet
	# 		pass


	def is_it_my_turn_to_act(self, my_position):
		"""
		crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).
		"""


		# my yellow strips
		my_top_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_top_yellow_strip.png", region=(873, 1431, 150, 10))
		my_right_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_right_yellow_strip.png", region=(1024, 1430, 9, 87))
		my_bottom_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_left_yellow_strip.png", region=(876, 1508, 155, 10))
		my_left_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_bottom_yellow_strip.png", region=(878, 1430, 9, 88))

		# my_top_strip.show()
		# my_right_strip.show()
		# my_bottom_strip.show()
		# my_left_strip.show()

		my_image_top = Image.open(f"{sys.path[0]}/photo_dump/my_top_yellow_strip.png", "r")
		my_image_right = Image.open(f"{sys.path[0]}/photo_dump/my_right_yellow_strip.png", "r")
		my_image_bottom = Image.open(f"{sys.path[0]}/photo_dump/my_left_yellow_strip.png", "r")
		my_image_left = Image.open(f"{sys.path[0]}/photo_dump/my_bottom_yellow_strip.png", "r")

		# This list will consist of just True and False values
		my_strips = [self.detect_yellow_strip(my_image_top), self.detect_yellow_strip(my_image_right), self.detect_yellow_strip(my_image_bottom), self.detect_yellow_strip(my_image_left)]

		if any(j for j in my_strips): 
			return True
		else: 
			return False


MTTA = IsItMyTurnToAct()
print(MTTA.is_it_my_turn_to_act(2))
