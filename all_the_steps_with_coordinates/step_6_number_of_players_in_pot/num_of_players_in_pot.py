import numpy as np
from PIL import ImageChops, Image
import cv2
import sys
import pyautogui
import pytesseract
from pytesseract import pytesseract


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

	def detect_if_cards_in_hand(self, my_position):
		"""
		The below 'fold_tracker' checks if there are cards in a players' hand.
		If someone has folded there is never cards in their hand.
		"""

		fold_tracker = dict()

		# # VIDEO coordinates
		# # My position
		# image1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img1.png", region=(563, 1359, 76, 33))
		# image1_path = f"{sys.path[0]}/photo_dump/img1.png"
		# # Guy to my left
		# image2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img2.png", region=(547, 1044, 82, 47))
		# image2_path = f"{sys.path[0]}/photo_dump/img2.png"
		# # Guy two to left
		# image3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img3.png", region=(600, 635, 82, 47))
		# image3_path = f"{sys.path[0]}/photo_dump/img3.png"
		# # Guy top of screen
		# image4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img4.png", region=(974, 390, 82, 47))
		# image4_path = f"{sys.path[0]}/photo_dump/img4.png"
		# # Guy top of screen + 1
		# image5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img5.png", region=(1227, 630, 82, 47))
		# image5_path = f"{sys.path[0]}/photo_dump/img5.png"
		# # Guy top of screen + 2
		# image6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/img6.png", region=(1276, 1047, 82, 47))
		# image6_path = f"{sys.path[0]}/photo_dump/img6.png"

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
			if self.calcdiff(image, f"{sys.path[0]}/photo_dump/not_folded.png") > 65 and \
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


# x = PlayersLeftInPot()
# print(f"fold_tracker is {x.detect_if_cards_in_hand(2, {1: False, 2: False, 3: False, 4: False, 5: False, 6: False})}")
