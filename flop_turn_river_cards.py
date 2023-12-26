# I wrote some notes in 'Notes' on what to consider on the flop.
import sys
import pyautogui
from PIL import Image
import pytesseract


class TheFlop:

	def number_corrector(self, num_list_or_turn_or_river_num):
		"""
		Sometimes the number recogniser reads the number slightly wrong and takes it as a letter.
		I'll map some of the common examples here so that we can correct it, and add to it as I run it on
		many different scenarios. 
		"""
		valid_nums = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
		corrector = {'T': '7', '1': '10', 'v': '7', 'g': '9', 'c': '9', 'S': '6', 'f': '9', 'a': '7', '&': '8', 'i': '6', 'Ty': '7'}
		# flop
		if isinstance(num_list_or_turn_or_river_num, list):
			for pos, i in enumerate(num_list_or_turn_or_river_num):
				if i not in valid_nums:
					if i in corrector:
						num_list_or_turn_or_river_num[pos] = corrector[i]
		# turn and river card
		else:
			if num_list_or_turn_or_river_num in corrector:
				num_list_or_turn_or_river_num = corrector[num_list_or_turn_or_river_num]
		return num_list_or_turn_or_river_num

	@staticmethod
	def convert_j_q_k_a(num_list_or_turn_or_river_card):
		j_q_k_a_converter = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}

		if isinstance(num_list_or_turn_or_river_card, list):
			for pos, i in enumerate(num_list_or_turn_or_river_card):
				if i in j_q_k_a_converter:
					num_list_or_turn_or_river_card[pos] = j_q_k_a_converter.get(i)
		else:
			if num_list_or_turn_or_river_card in j_q_k_a_converter:
				num_list_or_turn_or_river_card = j_q_k_a_converter.get(num_list_or_turn_or_river_card)

		# check that the converted face card(s) can be turned into an integer
		if isinstance(num_list_or_turn_or_river_card, list):
			# Now everything should be convertable to an integer
			for pos, i in enumerate(num_list_or_turn_or_river_card):
				try:
					num_list_or_turn_or_river_card[pos] = int(i)
				except:
					print(f'problem converting a number string on the flop to an integer, num_list: {num_list_or_turn_or_river_card[pos]}')
					breakpoint()
		else:
			try:
				num_list_or_turn_or_river_card = int(num_list_or_turn_or_river_card)
			except:
				print(f'problem converting a number string on the flop to an integer, num_list: {num_list_or_turn_or_river_card}')
				breakpoint()

		return num_list_or_turn_or_river_card

	@staticmethod
	def determine_suit_clubs_hearts_diamonds(cropped_im_path):
		image = Image.open(cropped_im_path, "r")
		pixels = list(image.getdata())
		pixel_colour = []
		R_pixels = []
		G_pixels = []
		B_pixels = []
		for pixel in pixels:
			R,G,B,C = pixel
			if R > 180 or R == 0: 
				continue
			elif G > 180 or G == 0: 
				continue
			elif B> 180 or B == 0:
				continue
			else: 
				R_pixels.append(R)
				G_pixels.append(G)
				B_pixels.append(B)
		R_average = sum(R_pixels) / len(R_pixels)
		G_average = sum(G_pixels) / len(G_pixels)
		B_average = sum(B_pixels) / len(B_pixels)

		if R_average > G_average and R_average > B_average: 
			return 'H'
		elif G_average > R_average and G_average > B_average: 
			return 'C'
		elif B_average > R_average and B_average > G_average: 
			return 'D'
		else: 
			raise Exception('something wrong with suit detection')

	@staticmethod
	def determine_black_spades(cropped_im_path):
		image = Image.open(cropped_im_path, "r")
		pixels = list(image.getdata())
		differences = []

		for pixel in pixels: 
			current_H_A_D = 0
			R,G,B,C = pixel
			current_H_A_D += abs(R - G)
			current_H_A_D += abs(G - B)

			differences.append(current_H_A_D)

		differences = list(filter(lambda x: (x > 60), differences))

		# Not a black suit
		if len(differences) > 150: 
			return TheFlop.determine_suit_clubs_hearts_diamonds(cropped_im_path)

		else: 
			return 'S'

	def detect_flop_nums_and_suit(self): 
		# (R)!!!! NOTE THAT FOR NUMBER OF LETTER DETECTION, THE MORE YOU CENTRALISE!! THE CARD THE BETTER IT DETECTS!
		# IT'S NOT ABOUT ENLARGING THE IMAGE, IT'S ABOUT MAKING IT MORE CENTAL, SO IF IT LOOKS TOO FAR TO THE LEFT, THE EXTEND THE 
		# IMAGE LEFT A BIT SO THAT THE NUMBER ITSELF IS MORE IN THE CENTER OF THE OVERALL IMAGE!
		"""(LEFT, UPPER, RIGHT, LOWER)

		N.B. TO DO!!!!!!
		- All numbers except '7' detects okay. The black seven detects okay, but other 7's do not.
		In the real app the definition is clear so maybe it will detect it, but otherwise you need to
		add an extra check; the first thing that came to mind is to scan the larger number on the card as a back up.
		"""
		flop1_num = []
		flop1_suit = []
		flop2_num = []
		flop2_suit = []

		# VIDEO COORDINATES
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop1.png", region=(723, 780, 238, 32))
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop2.png", region=(724, 900, 238, 35))
		image_of_flop1_cards = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop1.png")
		image_of_flop2_cards = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop2.png")
		# image_of_flop1_cards.show()
		# image_of_flop2_cards.show()

		# Get the three individual nums and suits from the TWO separate flop cards
		crop_coordinates_of_flop1_cards = [(0, 2, 29, 47), (97, 0, 129, 45), (200, 1, 230, 53)]
		crop_coordinates_of_flop2_cards = [(6, 2, 34, 44), (102, 0, 130, 44), (200, 1, 226, 51)]
		two_flop_coordinates = [crop_coordinates_of_flop1_cards, crop_coordinates_of_flop2_cards]
		for pos, curr_flop in enumerate(two_flop_coordinates):
			for flop_coord in curr_flop:
				if pos == 0:  # flop1
					cropped_im = image_of_flop1_cards.crop(flop_coord)
					cropped_im.save(f"{sys.path[0]}/photo_dump/flop1_card.png")
					cropped_im_path = f"{sys.path[0]}/photo_dump/flop1_card.png"
					new_im = Image.open(cropped_im_path)
					# new_im.show()
					current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
					flop1_num.append(current_num)
					# get suit of the card
					flop1_suit.append(TheFlop.determine_black_spades(cropped_im_path))
				elif pos == 1:  # flop2
					cropped_im = image_of_flop2_cards.crop(flop_coord)
					cropped_im.save(f"{sys.path[0]}/photo_dump/flop2_card.png")
					cropped_im_path = f"{sys.path[0]}/photo_dump/flop2_card.png"
					new_im = Image.open(cropped_im_path)
					# new_im.show()
					current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
					flop2_num.append(current_num)
					# get suit of the card
					flop2_suit.append(TheFlop.determine_black_spades(cropped_im_path))

		flop1_num = [i[:len(i)-1] for i in flop1_num]  # screenshot has additional chars, so only choose the number
		flop1_num = self.number_corrector(flop1_num)
		for i in flop1_num:
			if len(i) != 1 and i != '10':
				print('Detected a number that is more than 2 chars long that is not a 10 or no number found')
				print(f'here is the flop that was detected: {flop1_num}')
				breakpoint()

		flop2_num = [i[:len(i)-1] for i in flop2_num]  # screenshot has additional chars, so only choose the number
		flop2_num = self.number_corrector(flop2_num)
		for i in flop2_num:
			if len(i) != 1 and i != '10':
				print('Detected a number that is more than 2 chars long that is not a 10 or no number found')
				print(f'here is the flop that was detected: {flop1_num}')
				breakpoint()

		# converting J Q K A to -> 11, 12, 13, 14 ; it also turns all the values into an integer
		flop1_num = TheFlop.convert_j_q_k_a(flop1_num)
		flop2_num = TheFlop.convert_j_q_k_a(flop2_num)

		flop1 = [flop1_num, flop1_suit]
		flop2 = [flop2_num, flop2_suit]
		return flop1, flop2


class TheTurn(TheFlop):

	def sort_turn_and_river_nums(self, street):
		"""
		This function will sort the turn or river, whichever we pass into this function; it will sort it
		using nums, and it will sort it in descending order.
		"""
		return sorted(street, key=lambda x: x[0], reverse=True)

	def detect_turn_nums_and_suit(self):
		"""
		This function will simply take a picture of the two turn cards, and return them in
		two lists, so that they can be easily added to self.flop.

		Detects perfectly, only thing it misreads is the 7 (that is non-black)
		"""
		# VIDEO COORDINATES - check coordinates- they're not right
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop1.png", region=(1022, 781, 30, 33))
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop2.png", region=(1021, 902, 26, 33))
		turn1_image_path = f"{sys.path[0]}/photo_dump/ss_of_flop1.png"
		turn2_image_path = f"{sys.path[0]}/photo_dump/ss_of_flop2.png"
		# turn1_image_path = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop1.png")
		# turn2_image_path = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop2.png")
		# turn1_image_path.show()
		# turn2_image_path.show()

		# turn card num and suit detection
		turn1_string = pytesseract.image_to_string(turn1_image_path, config='--psm 6')
		turn2_string = pytesseract.image_to_string(turn2_image_path, config='--psm 6')

		# here it looks like '6\n' or '10\n'
		if turn1_string[:2] == '10':
			turn1_num = '10'
		else:
			turn1_num = turn1_string[0]
		if turn2_string[:2] == '10':
			turn2_num = '10'
		else:
			turn2_num = turn2_string[0]

		# get suit of the card
		turn1_suit = TheFlop.determine_black_spades(turn1_image_path)
		turn2_suit = TheFlop.determine_black_spades(turn2_image_path)

		# common number recognition problems, try correct
		turn1_num = self.number_corrector(turn1_num)
		turn2_num = self.number_corrector(turn2_num)
		# convert the turn num to number if it is a face card
		turn1_num = self.convert_j_q_k_a(turn1_num)
		turn2_num = self.convert_j_q_k_a(turn2_num)

		turn1_card = [turn1_num, turn1_suit]
		turn2_card = [turn2_num, turn2_suit]

		return turn1_card, turn2_card


class TheRiver(TheTurn):

	def add_river_card_num_and_suit_to_turn(self, turn):
		"""
		Thinking ahead, I would still want the structure looking like this on the turn:
		[[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]

		Because I will need to do computation for wrap and straights that involve all 4 cards.
		e.g. to determine if there is a wrap or straight draw made on the turn.
		"""
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_river_card.png", region=(1125, 710, 32, 34))
		cropped_im = Image.open(f"{sys.path[0]}/photo_dump/ss_of_river_card.png")
		# cropped_im.show()

		# turn card num and suit detection
		cropped_im.save(f"{sys.path[0]}/photo_dump/river_card.png")
		cropped_im_path = f"{sys.path[0]}/photo_dump/river_card.png"
		new_im = Image.open(cropped_im_path)
		current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
		# print(current_num)

		river_num = current_num[0]  # could still be J, Q, K, A here
		river_num = int(self.convert_j_q_k_a(river_num))

		# get suit of the card
		river_suit = TheFlop.determine_black_spades(cropped_im_path)

		if not river_num or not river_suit:
			print(f'Either the turn number {river_num} or turn suit: {river_suit} was not detected.')
			breakpoint()  # leave this breakpoint here.

		river_card = [river_num, river_suit]
		turn.append(river_card)  # add both river num and suit to turn
		river = turn  # then assign this new 'turn' with the two rivers cards to 'river'

		river = self.number_corrector(river)
		# convert the turn num to number if it is a face card
		river = self.convert_j_q_k_a(river)

		# sort the river in descending order according to nums
		river = self.sort_turn_and_river_nums(river)

		return river, river_num, river_suit


# x = TheFlop()
# print(x.detect_flop_nums_and_suit())

y = TheTurn()
print(y.detect_turn_nums_and_suit())

# z = TheRiver()
# print(z.add_river_card_num_and_suit_to_turn([[10, 'H'], [8, 'C'], [12, 'D'], [2, 'C']]))
