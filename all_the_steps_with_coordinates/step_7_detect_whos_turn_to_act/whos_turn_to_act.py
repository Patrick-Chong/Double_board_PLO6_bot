import sys
from PIL import Image
import pyautogui


class IsItMyTurnToAct:

	@staticmethod
	def detect_yellow_strip(image):
		pixels = list(image.getdata())
		yellow_count = 0 
		non_yellow_count = 0 

		for pixel in pixels:
			r, g, b, c = pixel
			if r >= (2*b) and g >= (2*b):  # this is a yellow strip!
				yellow_count += 1
			else: 
				non_yellow_count += 1
		if yellow_count > non_yellow_count: 
			return True

	@staticmethod
	def is_it_my_turn_to_act():
		"""
		crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).

		Instead of scanning the bottom yellow bar, I scan the top yellow bar - there is one at the top where my hand is
		that counts down exactly the same - it is easier to scan that.

		You only want to scan the first part of the bar, because if you scan the whole thing there is an issue
		since a big part of it will be black/grey as the timer runs down! And since we are using colour to
		analyse it, it's best to scan the start of the bar which will stay yellow the longest.
		"""
		# Yellow strip just below my hand at top of screen
		my_strip = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_top_yellow_strip.png", region=(532, 203, 10, 10))
		# my_strip.show()
		my_strip = Image.open(f"{sys.path[0]}/photo_dump/my_top_yellow_strip.png", "r")
		if IsItMyTurnToAct.detect_yellow_strip(my_strip):
			return True
		else: 
			return False


# mtta = IsItMyTurnToAct()
# print(mtta.is_it_my_turn_to_act())
