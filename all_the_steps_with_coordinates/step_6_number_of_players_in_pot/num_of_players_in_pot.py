import numpy as np
from PIL import ImageChops, Image
import cv2
import sys
import pyautogui
import pytesseract
from pytesseract import pytesseract


class DetectEmptySeat:

	def __init__(self):
		pass

	def read_white_text_on_image(self, image_path):
		# Grayscale, Gaussian blur, Otsu's threshold
		image = cv2.imread(image_path)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (3,3), 0)
		thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

		# Morph open to remove noise and invert image
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
		opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
		invert = 255 - opening

		# Perform text extraction
		data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

		empty_set = ('E', 'M', 'P', 'T', 'Y', 'y')
		count_empty = 0
		for char in data:
			if char in empty_set:
				count_empty += 1

		if count_empty > 3:
			return True
		else:
			return False

	def detect_empty_seat(self, my_position):
		"""
		Sometimes empty_seat_tracker marks a seat empty by mistake, because it detects someone's name as empty.

		I made the check a bit stricter, and if for some reason empty seat doesn't get picked up it is okay,
		because the fold tracker will pick it up; before the issue was that the fold tracker looked for a 'Fold'
		sign above the player's head, but now it scans the card, and an empty seat will NEVER have cards.

		Also, worth noting that having 'FOLD' or 'EMPTY' serves the same purpose.
		"""

		# My seat- even tho this is never empty, I need to calculate it for positioning/indexing or it will be trickier
		# pos1 - MY seat will never be empty

		# Guy to my left
		pos2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos2.png", region=(614, 1087, 81, 28))
		pos2_path = f"{sys.path[0]}/photo_dump/pos2.png"

		# # Guy two to my left
		pos3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos3.png", region=(665, 673, 81, 28))
		pos3_path = f"{sys.path[0]}/photo_dump/pos3.png"

		# # Guy top of screen
		pos4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos4.png", region=(919, 432, 81, 28))
		pos4_path = f"{sys.path[0]}/photo_dump/pos4.png"

		# # Guy top of screen + 1
		pos5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos5.png", region=(1172, 673, 81, 28))
		pos5_path = f"{sys.path[0]}/photo_dump/pos5.png"


		# # Guy top of screen + 2
		pos6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos6.png", region=(1220, 1087, 81, 28))
		pos6_path = f"{sys.path[0]}/photo_dump/pos6.png"

		# pos2.show()
		# pos3.show()
		# pos4.show()
		# pos5.show()
		# pos6.show()

		empty_seat_tracker = dict()
		empty_seat_tracker[my_position] = False  # my seat will never be empty
		pos_paths = [pos2_path, pos3_path, pos4_path, pos5_path, pos6_path]
		curr_position = my_position + 1

		for path in pos_paths:
			is_empty = self.read_white_text_on_image(path)

			curr_position %= 7
			if curr_position == 0:
				curr_position = 1

			empty_seat_tracker[curr_position] = is_empty
			curr_position += 1

		# For empty seats, double check they are empty by checking there are no cards in opp's hands
		# i.e. check that in fold_tracker, their position is True.
		return empty_seat_tracker


class PlayersLeftInPot:

	def have_I_folded(self, image_path): 

		im = Image.open(image_path)
		new_im = im.resize((60, 60))
		current_str = pytesseract.image_to_string(new_im, config='--psm 6')
		current_str = current_str[:4]
		
		fold_letters = ('F', 'o', 'l', 'd')
		fold_count = 0 
		for char in current_str: 
			if char in fold_letters: 
				fold_count += 1

		return fold_count >= 2

	def calcdiff(self, im1_path, im2_path):
		"""
		Difference in image of cards vs. no cards.
		If two images have cards, the difference is 28, if one has cards and the other doesn't, difference is 91.
		"""

		im1 = Image.open(im1_path)
		im2 = Image.open(im2_path)
		dif = ImageChops.difference(im1, im2)
		return np.mean(np.array(dif))

	def detect_if_cards_in_hand(self, my_position, empty_seat_tracker):
		"""
		The below 'fold_tracker' checks if there are cards in a players' hand.
		If someone has folded there is never cards in their hand.
		"""

		fold_tracker = dict()

		# VIDEO coordinates
		# My position
		image1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img1.png", region=(563, 1359, 76, 33))
		image1_path = f"{sys.path[0]}/photo_dump/img1.png"
		# Guy to my left 
		image2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img2.png", region=(547, 1044, 82, 47))
		image2_path = f"{sys.path[0]}/photo_dump/img2.png"
		# Guy two to left
		image3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img3.png", region=(600, 635, 82, 47))
		image3_path = f"{sys.path[0]}/photo_dump/img3.png"
		# Guy top of screen
		image4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img4.png", region=(974, 390, 82, 47))
		image4_path = f"{sys.path[0]}/photo_dump/img4.png"
		# Guy top of screen + 1
		image5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img5.png", region=(1227, 630, 82, 47))
		image5_path = f"{sys.path[0]}/photo_dump/img5.png"
		# Guy top of screen + 2
		image6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img6.png", region=(1276, 1047, 82, 47))
		image6_path = f"{sys.path[0]}/photo_dump/img6.png"

		# REAL APP coordinates
		# My position
		image1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img1.png", region=(571, 1359, 76, 33))
		image1_path = f"{sys.path[0]}/photo_dump/img1.png"
		# Guy to my left
		image2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img2.png", region=(557, 1044, 82, 47))
		image2_path = f"{sys.path[0]}/photo_dump/img2.png"
		# Guy two to left
		image3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img3.png", region=(608, 635, 82, 47))
		image3_path = f"{sys.path[0]}/photo_dump/img3.png"
		# Guy top of screen
		image4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img4.png", region=(982, 390, 82, 47))
		image4_path = f"{sys.path[0]}/photo_dump/img4.png"
		# Guy top of screen + 1
		image5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img5.png", region=(1235, 630, 82, 47))
		image5_path = f"{sys.path[0]}/photo_dump/img5.png"
		# Guy top of screen + 2
		image6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img6.png", region=(1284, 1044, 82, 47))
		image6_path = f"{sys.path[0]}/photo_dump/img6.png"

		# image1.show()
		# image2.show()
		# image3.show()
		# image4.show()
		# image5.show()
		# image6.show()

		# Add my position 
		fold_tracker[my_position] = self.have_I_folded(image1_path) 

		images = [image2_path, image3_path, image4_path, image5_path, image6_path]
		my_position = my_position + 1
		my_position %= 7
		if my_position == 0: 
			my_position = 1

		for image in images:
			# N.B. For empty seat tracker one issue is that peoples' names sometimes get read for EMPTY, so I do extra checks.
			if empty_seat_tracker[my_position] and \
					self.calcdiff(image, f"{sys.path[0]}/photo_dump/not_folded.png") > 65 and \
					self.calcdiff(image, f"{sys.path[0]}/photo_dump/folded.png") < 45:
				fold_tracker[my_position] = True
				my_position += 1
				my_position %= 7

				if my_position == 0: 
					my_position = 1
			elif self.calcdiff(image, f"{sys.path[0]}/photo_dump/not_folded.png") > 65 and \
					self.calcdiff(image, f"{sys.path[0]}/photo_dump/folded.png") < 45:
				fold_tracker[my_position] = True
				my_position += 1
				my_position %= 7

				if my_position == 0: 
					my_position = 1
			else:
				fold_tracker[my_position] = False
				my_position += 1
				my_position %= 7

				if my_position == 0: 
					my_position = 1

		return fold_tracker


x = PlayersLeftInPot()
print(f"fold_tracker is {x.detect_if_cards_in_hand(2, {1: False, 2: False, 3: False, 4: False, 5: False, 6: False})}")

# x = DetectEmptySeat()
# print(x.detect_empty_seat(2))
