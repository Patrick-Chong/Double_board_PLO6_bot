import sys
import pyautogui


class FlopTurnRiver:

	def __init__(self):
		# self._2_on_flop = self._2_on_flop()
		# self.on_turn = self.on_turn()
		# self.on_river = self.on_river()
		# self._1_pre_flop = self._1_pre_flop()
		pass

	def on_flop(self):
		image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/flop.png", region=(905, 775, 60, 60))
		# image.show()

		return self.check_card(image)

	def on_turn(self):
		image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/turn.png", region=(1005, 779, 60, 60))
		# image.show()
		return self.check_card(image)

	def on_river(self):
		image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/flop.png", region=(1120, 780, 60, 60))
		image.show()
		return self.check_card(image)

	def pre_flop(self, on_flop, on_turn, on_river):
		return (not on_flop and not on_turn and not on_river)

	def check_card(self, screenshot_of_card): 
		"""
		This function will check if the area being scanned is a card; 
		to help determine if we are on the flop, turn or river street.
		"""
		pixels = list(screenshot_of_card.getdata())

		R_biggest = 0 
		G_biggest = 0 
		B_biggest = 0 

		for pixel in pixels:
			R,G,B,C = pixel

			if R > R_biggest: 
				R_biggest = R

			if G > G_biggest: 
				G_biggest = G

			if B > B_biggest: 
				B_biggest = B

		# print(R_biggest, G_biggest, B_biggest)
		if R_biggest > 230 or B_biggest > 230 or G_biggest > 230: 
			return True

	def determine_street(self): 
		"""
		Takes a screenshot of where the turn and river cards are and determines if we are on the flop, 
		turn or river.


		(R)!!!! 
		The way to determine if there is a card is to get the largest of the RGB value;
		if there is no card, the largestr RGB value will be small, because there is no white 
		background, which is what you will have if there is a card. 
		And in which case the largest RBG will be 255.
		"""
		on_flop = self.on_flop()
		on_turn = self.on_turn()
		on_river = self.on_river()
		pre_flop = self.pre_flop(on_flop, on_turn, on_river)

		if on_river:
			# print('we are on the river')
			return 'on_river'

		elif on_turn:
			# print('we are on the turn')
			return 'on_turn'

		elif on_flop:
			# print('we are on the flop')
			return '_2_on_flop'

		elif pre_flop:
			# print('we are pre-flop')
			return '_1_pre_flop'
		else:
			raise Exception('Did not detect if we are on flop, turn, river or _1_pre_flop')


# x = FlopTurnRiver()
# print(x.determine_street())
