import sys
import pyautogui


class FlopTurnRiver:
	@staticmethod
	def on_flop():
		image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/flop.png", region=(920, 775, 60, 60))
		# image.show()
		return FlopTurnRiver.check_card(image)

	@staticmethod
	def on_turn():
		image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/turn.png", region=(1034, 779, 60, 60))
		# image.show()
		return FlopTurnRiver.check_card(image)

	@staticmethod
	def on_river():
		image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/flop.png", region=(1149, 780, 60, 60))
		# image.show()
		return FlopTurnRiver.check_card(image)

	@staticmethod
	def pre_flop(on_flop, on_turn, on_river):
		return not on_flop and not on_turn and not on_river

	@staticmethod
	def check_card(screenshot_of_card):
		"""
		This function will check if the area being scanned is a card; 
		to help determine if we are on the flop, turn or river street.
		"""
		pixels = list(screenshot_of_card.getdata())
		r_biggest = 0
		g_biggest = 0
		b_biggest = 0
		for pixel in pixels:
			r, g, b, c = pixel
			if r > r_biggest:
				r_biggest = r
			if g > g_biggest:
				g_biggest = g
			if b > b_biggest:
				b_biggest = b
		# print(R_biggest, g_biggest, b_biggest)
		if r_biggest > 230 or b_biggest > 230 or g_biggest > 230:
			return True

	@staticmethod
	def determine_street():
		"""
		Takes a screenshot of where the turn and river cards are and determines if we are on the flop, 
		turn or river.

		(R)!!!! 
		The way to determine if there is a card is to get the largest of the RGB value;
		if there is no card, the largest RGB value will be small, because there is no white
		background, which is what you will have if there is a card. 
		And in which case the largest RBG will be 255.
		"""
		on_flop = FlopTurnRiver.on_flop()
		on_turn = FlopTurnRiver.on_turn()
		on_river = FlopTurnRiver.on_river()
		pre_flop = FlopTurnRiver.pre_flop(on_flop, on_turn, on_river)

		if on_river:
			# print('we are on the river')
			return 'on_river'
		elif on_turn:
			# print('we are on the turn')
			return 'on_turn'
		elif on_flop:
			# print('we are on the flop')
			return 'on_flop'
		elif pre_flop:
			# print('we are pre-flop')
			return 'pre_flop_play'
		else:
			raise Exception('Did not detect if we are on pre_flop_play, flop, turn or river')


x = FlopTurnRiver()
print(x)
# print(x.determine_street())
