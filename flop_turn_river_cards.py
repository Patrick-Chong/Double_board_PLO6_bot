# I wrote some notes in 'Notes' on what to consider on the flop.
import sys
import pyautogui
from PIL import Image
import pytesseract


class TheFlop:

	def number_corrector(self, num_list): 
		"""
		Sometimes the number recogniser reads the number slightly wrong and takes it as a letter.
		I'll map some of the common examples here so that we can correct it, and add to it as I run it on
		many different scenarios. 
		"""
		valid_nums = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
		corrector = {'T': '7', '1': '10', 'v': '7', 'g': '9', 'c': '9', 'S': '6', 'f': '9', 'a': '7', '&': '8', 'i': '6', 'Ty': '7'}

		for pos, i in enumerate(num_list):
			if i not in valid_nums: 
				if i in corrector: 
					num_list[pos] = corrector[i]
		return num_list

	def convert_J_Q_K_A(self, num_list):
		J_Q_K_A_converter = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}

		for pos, i in enumerate(num_list):
			if i in J_Q_K_A_converter: 
				num_list[pos] = J_Q_K_A_converter[i]

		# Now everything should be convertable to an integer
		for pos, i in enumerate(num_list):
			try: 
				num_list[pos] = int(i)
			except: 
				print(f'problem converting a number string on the flop to an integer, num_list: {num_list[pos]}')
				breakpoint()

		return num_list


	def determine_suit_Clubs_Hearts_Diamonds(self, cropped_im_path): 
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

	def determine_black_SPADES(self, cropped_im_path): 
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
			return self.determine_suit_Clubs_Hearts_Diamonds(cropped_im_path)

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
		ss1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop1.png", region=(717, 778, 238, 32))
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop2.png", region=(719, 898, 238, 35))
		image_of_flop1_cards = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop1.png")
		image_of_flop2_cards = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop2.png")
		# image_of_flop1_cards.show()
		# image_of_flop2_cards.show()

		# Get the three individual nums and suits from the TWO separate flop cards
		crop_coordinates_of_flop1_cards = [(0, 2, 29, 47), (97, 0, 129, 45), (200, 1, 226, 51)]
		crop_coordinates_of_flop2_cards = [(6, 2, 34, 44), (101, 0, 130, 44), (200, 1, 226, 51)]
		two_flop_coordinates = [crop_coordinates_of_flop1_cards, crop_coordinates_of_flop2_cards]
		for pos, curr_flop in enumerate(two_flop_coordinates):
			for flop_coord in curr_flop:
				if pos == 0:
					cropped_im = image_of_flop1_cards.crop(flop_coord)
					cropped_im.save(f"{sys.path[0]}/photo_dump/flop1_card.png")
					cropped_im_path = f"{sys.path[0]}/photo_dump/flop1_card.png"
					new_im = Image.open(cropped_im_path)
					# new_im.show()
					current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
					# print(current_num)
					flop1_num.append(current_num)
					# get suit of the card
					flop1_suit.append(self.determine_black_SPADES(cropped_im_path))
				elif pos == 1:
					cropped_im = image_of_flop2_cards.crop(flop_coord)
					cropped_im.save(f"{sys.path[0]}/photo_dump/flop2_card.png")
					cropped_im_path = f"{sys.path[0]}/photo_dump/flop2_card.png"
					new_im = Image.open(cropped_im_path)
					# new_im.show()
					current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
					# print(current_num)
					flop2_num.append(current_num)
					# get suit of the card
					flop2_suit.append(self.determine_black_SPADES(cropped_im_path))

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
		flop1_num = self.convert_J_Q_K_A(flop1_num)
		flop2_num = self.convert_J_Q_K_A(flop2_num)

		flop1 = [flop1_num, flop1_suit]
		flop2 = [flop2_num, flop2_suit]

		return flop1, flop2

	def number_corrector_turn(self, turn):
		"""
		Sometimes the number recogniser reads the number slightly wrong and takes it as a letter.
		I'll map some of the common examples here so that we can correct it, and add to it as I run it on
		many different scenarios.
		"""
		valid_nums = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
		corrector = {'T': '7', '1': '10', 'v': '7', 'g': '9', 'c': '9', 'S': '6', 'f': '9', 'a': '7', '&': '8', 'i': '6', 'Ty': '7'}

		turn_num = turn[3][0]
		if turn_num not in valid_nums:
			if turn_num in corrector:
				turn[3][0] = corrector[turn[3][0]]
		return turn

	def convert_turn_J_Q_K_A(self, turn):
		"""
		turn will look like: [[13, 'S'], [10, 'C'], [9, 'S'], ['14', 'C']]
		"""
		J_Q_K_A_converter = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}

		num_of_turn_card = turn[3][0]
		if num_of_turn_card in J_Q_K_A_converter:
			turn[3][0] = J_Q_K_A_converter[num_of_turn_card]

		# Now turn num should be convertable into an integer
		try:
			turn[3][0] = int(turn[3][0])
		except:
			print(f'problem converting a number string on the flop to an integer, turn_num: {turn[3][0]}')
			breakpoint()
		return turn


	def add_turn_card_num_and_suit_to_flop(self, flop):
		"""
		Thinking ahead, I would still want the structure looking like this on the turn:
		[[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]

		Because I will need to do computation for wrap and straights that involve all 4 cards.
		e.g. to determine if there is a wrap or straight draw made on the turn.
		"""
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_flop.png", region=(676, 829, 32, 35))
		im = Image.open(f"{sys.path[0]}/photo_dump/ss_of_flop.png")
		# im.show()

		# turn card num and suit detection
		crop_rectangle = (0, 2, 31, 46)  # crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).
		cropped_im = im.crop(crop_rectangle)
		# cropped_im.show()
		cropped_im.save(f"{sys.path[0]}/photo_dump/turn_card.png")
		cropped_im_path = f"{sys.path[0]}/photo_dump/turn_card.png"
		new_im = Image.open(cropped_im_path)
		current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
		# print(current_num)
		turn_num = current_num[0]  # could still be J, Q, K, A here

		# get suit of the card
		turn_suit = self.determine_black_SPADES(cropped_im_path)

		if not turn_num or not turn_suit:
			print(f'Either the turn number {turn_num} or turn suit: {turn_suit} was not detected.')
			breakpoint()  # leave this breakpoint here.

		turn_card = [turn_num, turn_suit]
		flop.append(turn_card)  # add both turn num and suit to flop
		turn = flop

		turn = self.number_corrector_turn(turn)
		# convert the turn num to number if it is a face card
		turn = self.convert_turn_J_Q_K_A(turn)
		return turn


class TheTurn(TheFlop):

	def sort_turn_and_river_nums(self, street):
		"""
		This function will sort the turn or river, whichever we pass into this function; it will sort it
		using nums, and it will sort it in descending order.
		"""
		return sorted(street, key=lambda x: x[0], reverse=True)

	def number_corrector_turn(self, street):
		"""
		Sometimes the number recogniser reads the number slightly wrong and takes it as a letter.
		I'll map some of the common examples here so that we can correct it, and add to it as I run it on
		many different scenarios.
		"""
		valid_nums = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
		corrector = {'T': '7', '1': '10', 'v': '7', 'g': '9', 'c': '9', 'S': '6', 'f': '9', 'a': '7', '&': '8', 'i': '6', 'Ty': '7'}

		if len(street) == 4:
			turn_num = street[3][0]
			if turn_num not in valid_nums:
				if turn_num in corrector:
					street[3][0] = corrector[street[3][0]]
		elif len(street) == 5:
			river_num = street[4][0]
			if river_num not in valid_nums:
				if river_num in corrector:
					street[4][0] = corrector[street[4][0]]
		return street

	def convert_turn_J_Q_K_A(self, street):
		"""
		This function will convert the face cards into their respective numbers.
		It will convert the turn or river or a single card; turn_num or river_num.
		"""
		J_Q_K_A_converter = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}

		if len(street) == 1:
			# this will be converting either turn_num or river_num
			if street in J_Q_K_A_converter:
				street = int(J_Q_K_A_converter.get(street))

		elif len(street) == 4:
			# this is the turn
			num_of_turn_card = street[3][0]
			if num_of_turn_card in J_Q_K_A_converter:
				street[3][0] = J_Q_K_A_converter.get(num_of_turn_card)

			# Now turn num should be convertable into an integer
			try:
				street[3][0] = int(street[3][0])
			except:
				print(f'problem converting a number string on the flop to an integer, turn_num: {street[3][0]}')
				breakpoint()
		elif len(street) == 5:
			# this is the river
			num_of_turn_card = street[4][0]
			if num_of_turn_card in J_Q_K_A_converter:
				street[4][0] = J_Q_K_A_converter.get(num_of_turn_card)

			# Now turn num should be convertable into an integer
			try:
				street[4][0] = int(street[4][0])
			except:
				print(f'problem converting a number string on the flop to an integer, turn_num: {street[4][0]}')
				breakpoint()

		return street

	def add_turn_card_num_and_suit_to_flop(self, flop):
		"""
		Thinking ahead, I would still want the structure looking like this on the turn:
		[[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]

		Because I will need to do computation for wrap and straights that involve all 4 cards.
		e.g. to determine if there is a wrap or straight draw made on the turn.
		"""
		# KCL MONITOR COORDINATES
		# pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_turn_card.png", region=(1023, 708, 32, 33))

		# HOME MONITOR COORDINATES
		pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_turn_card.png", region=(1023, 708, 32, 37))
		cropped_im = Image.open(f"{sys.path[0]}/photo_dump/ss_of_turn_card.png")
		# cropped_im.show()

		# turn card num and suit detection
		cropped_im.save(f"{sys.path[0]}/photo_dump/turn_card.png")
		cropped_im_path = f"{sys.path[0]}/photo_dump/turn_card.png"
		new_im = Image.open(cropped_im_path)
		current_num = pytesseract.image_to_string(cropped_im, config='--psm 6')
		# print(current_num)
		if current_num[:2] == '10':
			turn_num = '10'
		else:
			turn_num = current_num[0]  # could still be J, Q, K, A here
		turn_num = self.convert_turn_J_Q_K_A(turn_num)

		# get suit of the card
		turn_suit = self.determine_black_SPADES(cropped_im_path)

		if not turn_num or not turn_suit:
			print(f'Either the turn number {turn_num} or turn suit: {turn_suit} was not detected.')
			breakpoint()  # leave this breakpoint here.

		turn_card = [turn_num, turn_suit]
		temp = flop
		temp.append(turn_card)  # add both turn num and suit to flop
		turn = temp

		turn = self.number_corrector_turn(turn)
		# convert the turn num to number if it is a face card
		turn = self.convert_turn_J_Q_K_A(turn)

		# sort the turn in descending order according to nums
		turn = self.sort_turn_and_river_nums(turn)
		return turn, turn_num, turn_suit


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
		river_num = int(self.convert_turn_J_Q_K_A(river_num))

		# get suit of the card
		river_suit = self.determine_black_SPADES(cropped_im_path)

		if not river_num or not river_suit:
			print(f'Either the turn number {river_num} or turn suit: {river_suit} was not detected.')
			breakpoint()  # leave this breakpoint here.

		river_card = [river_num, river_suit]
		turn.append(river_card)  # add both river num and suit to turn
		river = turn  # then assign this new 'turn' with the two rivers cards to 'river'

		river = self.number_corrector_turn(river)
		# convert the turn num to number if it is a face card
		river = self.convert_turn_J_Q_K_A(river)

		# sort the river in descending order according to nums
		river = self.sort_turn_and_river_nums(river)

		return river, river_num, river_suit


# x = TheFlop()
# print(x.detect_flop_nums_and_suit())

# y = TheTurn()
# print(y.add_turn_card_num_and_suit_to_flop([[10, 'H'], [8, 'C'], [12, 'D']]))

# z = TheRiver()
# print(z.add_river_card_num_and_suit_to_turn([[10, 'H'], [8, 'C'], [12, 'D'], [2, 'C']]))
