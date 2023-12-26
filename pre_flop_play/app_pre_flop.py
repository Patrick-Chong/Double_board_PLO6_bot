import cv2
import sys
import pyautogui
from PIL import Image
import pytesseract

from analyse_my_hand_pre_flop import ShouldWePlayThisPreFlopHand


def read_white_text_on_image(image_path, ss):
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
	image_string_detected = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

	if not image_string_detected:
		# verify it was Checked by scanning the button; if it is a blue background it means it is a check.

		# crop the right side of the image so none of the white 'check' is in the picutre, then detect blue colour
		im = Image.open(image_path)
		cropped_image_for_blue = im.crop((120, 8, 200, 200))
		pixels = list(ss.getdata())
		total_pixels = len(pixels)
		num_of_blue_pixel = 0
		for pixel in pixels:
			R,G,B,C = pixel
			if B > 110:
				num_of_blue_pixel += 1
		if num_of_blue_pixel >= 0.8*total_pixels:
			return 0
		else:
			print('no number detected on button and not enough blue on button detected')
			breakpoint()
	else:
		# number_on_button looks something like Call 1:64 or Call 0.40 or Call'2:24 or Call'13.44
		# gather all the numbers into a string
		bet_amount = ''
		for num in image_string_detected:
			try:
				curr_num = int(num)
				bet_amount = bet_amount + f'{curr_num}'
			except:
				pass
		# add decimal point to three spaces from the right
		bet_amount = bet_amount[:len(bet_amount)-2] + '.' + bet_amount[len(bet_amount)-2:]
		try:
			final_bet_amount = float(bet_amount)
			return final_bet_amount
		except:
			print(f'bet amount looks like {bet_amount}')
			breakpoint()

def scan_call_button_to_see_bet_amount():
	"""
	This function simply scans my 'call' button at the bottom of the screen, which shows the
	largest bet amount that I need to call to continue the hand.

	(R)!!! Two things to note:
	1) The detector cannot detect 'checks', because of the blur background of the button.
	so when it is my turn and I want to see if it has been 'checked' - do two things 1) the detector is ''
	and 2) scan a bit of the background of the button and check that it is blue.

	2) Otherwise if there is an amount to call the background of the button is green and it detects fine.
	"""
	# bet size on my button
	ss = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/largest_bet_size_my_button.png", region=(889, 1607, 149, 41))

	# image = Image.open(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/largest_bet_size_my_button.png")
	# image.show()

	image_path = f"{sys.path[0]}/photo_dump/screenshots_of_stacks/largest_bet_size_my_button.png"
	final_bet_amount = read_white_text_on_image(image_path, ss)
	print(f'bet to call detected is:{final_bet_amount}')

	return final_bet_amount


class RunPreFlop(ShouldWePlayThisPreFlopHand):

	def __init__(self, my_position, num_list, suit_list, big_blind, stack_tracker, empty_seat_tracker):
		ShouldWePlayThisPreFlopHand.__init__(self, my_position, empty_seat_tracker, num_list, suit_list)
		self.big_blind = big_blind
		self.stack_tracker = stack_tracker
		self.pre_flop_bet_amount = scan_call_button_to_see_bet_amount()

	def limped_or_3_bet_to_me_pre_flop(self):
		"""
		This function tells us whether it has been limped to us or has been three_bet behind or more.

		The way to calculate is to scan my button and see what the amount is to call.

		Then there is a running 'pot' amount, and it includes the bet I am facing.
		So if you subtract the amount I need to call from the running bet, you get a good idea of whether it's been
		bet, 3-bet or more.

		Because before when I just
		"""
		folded_or_empty = ('Fold', 'Empty')
		if self.pre_flop_bet_amount <= self.big_blind:
			return 'limped'
		elif self.big_blind < self.pre_flop_bet_amount <= 4 * self.big_blind:
			return 'bet'
		elif 4 * self.big_blind < self.pre_flop_bet_amount <= 10 * self.big_blind:
			return 'three_bet'
		elif self.pre_flop_bet_amount > 10 * self.big_blind:
			return 'four_bet'
		else:
			print(f"Issue with limped bet or three bet detection, pre_flop bet size detected is {self.pre_flop_bet_amount}")
			breakpoint()

	def action_pre_flop(self, limped_or_3_bet_to_me_pre_flop):
		"""
		To begin with, as less 'risky' approach is NOT to 3-bet pre_flop, though I'm quite sure this
		is profitable if done right, I still think the equity is too close to be doing this.
		Better to see a flop 'cheaply', then go ham if I connected hard with the flop.

		My play strategy with regards to position will be as follows, if I meet the 3 pillars:
		- If I am in position 5 or 6:
			- call a 3-bet (maybe I'll fold - play and see; what if it's 4-bet behind me?)
			The only way this is worth it is if I incorporate bluffs in, with position, I think.
			- raise if it has been limped
		- If I am in any other position:
			- Call any bets and limp if it has been limped.

		IN THIS FUNCTION I should consider all things I noted down on notepad to make the
		decision to 'bet', 'call' or 'fold' pre_flop:
		- SPR (only if SPR is now extremely low is this a consideration otherwise doesn't matter)
		- action behind me (particularly has it been 3-bet)
		- am I in position, play as per what it says above.
		- do I meet at least 3/4 pillars
		"""
		if not self.does_my_hand_meet_at_least_three_pillars():
			return 'FOLD'
		premium_positions = (5, 6)
		if self.my_position in premium_positions:
			if limped_or_3_bet_to_me_pre_flop in ('three_bet', 'bet'):
				return 'CALL'
			if limped_or_3_bet_to_me_pre_flop == 'limped':
				return 'BET'
		else:
			if limped_or_3_bet_to_me_pre_flop in ('bet', 'limped'):
				return 'CALL'
		return 'FOLD'

	def pre_flop_action(self):
		extra_information = dict()  # store if someone 3-bet pre_flop

		limped_or_3_bet_to_me_pre_flop = self.limped_or_3_bet_to_me_pre_flop()
		action = self.action_pre_flop(limped_or_3_bet_to_me_pre_flop)
		extra_information['three_bet_pre_flop'] = True if limped_or_3_bet_to_me_pre_flop == 'three_bet' else False

		return action, extra_information

# x = RunPreFlop()
# print(scan_call_button_to_see_bet_amount())
# print(x.pre_flop_action())
