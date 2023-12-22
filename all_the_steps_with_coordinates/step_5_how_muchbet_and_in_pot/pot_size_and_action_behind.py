import cv2
import sys
import pyautogui
from PIL import Image
import pytesseract


def read_colour_of_billboard_to_determine_action_of_each_player(position_of_player_to_position_of_image_path, stack_tracker):
	"""
	This function will try and ready the colour of the billboard, this is because I know that:
	1) Green = Call
	2) Orange = Bet
	3) Pink = All in
	4) Blue = Check
	5) Fold = Grey - need to detect this, to make distinction with someone who hasn't acted yet.

	If none of the above conditions are met, then the person hasn't acted yet; the above represent
	all of the possible actions - if any are missing, add to it.

	I will pass stack_tracker as an argument, because someone's stack is 0 if they have folded,
	so by default, I can mark their billboard as 'Fold' - note, I DO NOT mark it as None, because this
	implies that they are yet to act!!! - but fold represents the fact that they will not be acting,
	which is what this billboard thing is about- to determine if someone is yet to act ahead of me. Or if someone
	has bet behind me.

	Caveats/edge cases:
	1) if someone hasn't acted yet, then there is no sign on their head.
	Usually when you scan the top of their head it will be the pokerbros background which is grey.
	So I make the distinction between this and folding (which also looks at greyness), by checking white pixels.
	In FOLD there are white pixels, but the pokerbros background does not.
	- The above holds try for all players, except for the guy ONE TO MY LEFT, when he hasn't acted, and we are on
	the flop or beyond, the cards gets in the way and lots of white is detected on his billboard, so I set a range of num_of_white_pixels
	and this works.

	2) 'SB'-small blind and 'BB' are also blue - but they only come up pre_flop, so need to consider this.
	I HAVE NOT YET CODED ANYTHING FOR THIS- THINK ABOUT IT.

	3) When players have folded, sometimes it does NOT show the 'Fold' billboard above their head.
	And I think for others too, but their stack will be 0.
	So this combination will be enough to tell you what you need to know, just need to keep this in
	mind when coding things.

	4) As mentioned further up, if someone has folded or empty seat their stack is 0, so mark as folded.
	The one caveat is if someone goes all in! Their stack will also be 0.
	But this is dealt with nicely, I check for all in first, then check if stack=0.

	5) I have not factored in 'Raise', which is also orange; same as 'Bet'.
	"""
	player_position_to_action = {}
	for pos in position_of_player_to_position_of_image_path:
		im = Image.open(position_of_player_to_position_of_image_path[pos])
		pixels = list(im.getdata())
		total_pixels = len(pixels)
		num_of_green_pixel = 0
		num_of_blue_pixel = 0
		num_of_pink_pixel = 0
		num_of_orange_pixels = 0
		num_of_grey_pixels = 0
		num_of_white_pixels = 0  # to distinguish fold vs. not acted yet - FOLD has white pixels
		for pixel in pixels:
			R,G,B,C = pixel

			if B > 100 and G > 100 and R > 100:
				num_of_white_pixels += 1

			if B > G > R:
				num_of_blue_pixel += 1

			if abs(G-R) >= 40 and abs(G-B) >= 40:
				num_of_green_pixel += 1

			if R > 120 and G < 120 and B > 120:
				num_of_pink_pixel += 1

			if R > 100 and G > 100 and B < 100:
				num_of_orange_pixels += 1

			if abs(R-G) <= 10 and abs(G-B) <= 10 and abs(R-B) <= 10:
				num_of_grey_pixels += 1

		# DO NOT change order of the below - it matters for pink pixel detection only
		if num_of_pink_pixel >= 0.35*total_pixels:
			player_position_to_action[pos] = 'all in'
		if stack_tracker[pos] == 0:
			player_position_to_action[pos] = 'fold'
		elif num_of_green_pixel >= 0.5*total_pixels and num_of_green_pixel > num_of_blue_pixel and num_of_orange_pixels <= 950:
			player_position_to_action[pos] = 'call'
		elif num_of_blue_pixel >= 0.9*total_pixels:
			player_position_to_action[pos] = 'check'
		elif num_of_orange_pixels >= 0.3*total_pixels:
			player_position_to_action[pos] = 'bet'
		elif num_of_grey_pixels >= 0.8*total_pixels:
			if num_of_white_pixels >= 0.25*total_pixels and num_of_white_pixels < 1100:
				player_position_to_action[pos] = 'fold'
			else:
				player_position_to_action[pos] = None
		else:
			# if none of the above detected, it means player has not acted yet - i.e. no billboard on their head
			player_position_to_action[pos] = None

	return player_position_to_action


class PotSizeAndActionBehindMe:

	def __init__(self, my_position, fold_tracker, stack_tracker, pre_flop=False):
		#  CALL THE BELOW DIRECTLY RATHER THAN THROUGH THIS CLASS!!!! - because you do not want to use an old value!
		self.my_position = my_position
		self.stack_tracker = stack_tracker
		self.fold_tracker = fold_tracker

		self.scan_action_of_the_table_f = self.scan_action_of_the_table()

		"""
		The below are the 'real' functions, all other functions are used to support these:
		self.scan_action_of_the_table
		self.pot_size
		self.scan_call_button_to_see_bet_amount
		self.how_much_can_i_raise_to
		self.calculate_SPR
		self.positions_of_players_to_act_ahead_of_me
		"""

	def read_check_bet_fold_sign_on_billboard(self, images):
		"""
		In the images: images = [image1, image2, image3, image4, image5, image6]
		N.B.
		THIS IS ALWAYS TRUE: image1 is me, image2 is guy to my left, image3 guy two to my self, etc. going round.
		"""
		position_of_player_to_position_of_image_path = {}
		curr_position = self.my_position
		for i in range(6):
			position_of_player_to_position_of_image_path[curr_position] = images[i]
			curr_position += 1
			if curr_position == 7:
				curr_position = 1

		# this returns a dictionary of player position and their action on their billboard, in a dictionary.
		return read_colour_of_billboard_to_determine_action_of_each_player(position_of_player_to_position_of_image_path, self.stack_tracker)

	def scan_action_of_the_table(self):
		'''
		This scans the billboard thing above a players' head when they have acted - it is to check if someone
		has Checked, Bet, Raised, etc.

		crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).
		'''

		# VIDEO COORDIANTES
		# My position
		image1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image1.png", region=(880, 1274, 83, 28))
		# Guy to my left
		image2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image2.png", region=(644, 956, 83, 25))
		# Guy two to left
		image3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image3.png", region=(693, 550, 83, 22))
		# Guy top of screen
		image4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image4.png", region=(885, 312, 81, 22))
		# Guy top + 1
		image5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image5.png", region=(1134, 550, 81, 22))
		# Guy top + 2
		image6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image6.png", region=(1182, 957, 81, 22))
		# image1 will always be my stack, then we go clockwise round

		# image1.show()
		# image2.show()
		# image3.show()
		# image4.show()
		# image5.show()
		# image6.show()

		# REAL APP COORDINATES
		# image1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image1.png", region=(880, 1274, 83, 30))
		# # Guy to my left
		# image2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image2.png", region=(644, 956, 83, 27))
		# # Guy two to left
		# image3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image3.png", region=(693, 550, 83, 24))
		# # Guy top of screen
		# image4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image4.png", region=(885, 312, 81, 24))
		# # Guy top + 1
		# image5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image5.png", region=(1134, 550, 81, 24))
		# # Guy top + 2
		# image6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/image6.png", region=(1182, 957, 81, 24))
		# # image1 will always be my stack, then we go clockwise round
		# images = [image1, image2, image3, image4, image5, image6]

		# image paths
		image1 = f"{sys.path[0]}/photo_dump/image1.png"
		image2 = f"{sys.path[0]}/photo_dump/image2.png"
		image3 = f"{sys.path[0]}/photo_dump/image3.png"
		image4 = f"{sys.path[0]}/photo_dump/image4.png"
		image5 = f"{sys.path[0]}/photo_dump/image5.png"
		image6 = f"{sys.path[0]}/photo_dump/image6.png"
		images = [image1, image2, image3, image4, image5, image6]

		return self.read_check_bet_fold_sign_on_billboard(images)

	@staticmethod
	def pot_size(pre_flop=False):
		"""
		This function simply returns the size of the pot; post flop it takes a ss of the pot.

		Pre_flop it will simply sum the action_so_far dictionary values.

		I need to calculate it pre-flop because of the SPR tracker, which uses the pot size to calculate SPR.

		crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).
		"""

		if pre_flop:
			# For pre_flop we don't need pot size; stack_tracker, fold_trackerthe way we calculate whether it's been bet, 3-bet or more
			# is to compare the amount on our button to the blinds.
			return False

		else:
			# VIDEO COORDINATES
			image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pot_size.png", region=(917, 655, 70, 28))
			# image.show()

			# REAL APP COORDINATES
			# image = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pot_size.png", region=(917, 625, 70, 30))
			# image.show()

			im = Image.open(f"{sys.path[0]}/photo_dump/pot_size.png")

			# The printscreen number is small so we enlarge it so number reader can detect num correctly
			new_im = im.resize((109, 45))
			# new_im.show()
			pot_size = pytesseract.image_to_string(new_im, config='--psm 6')

			final_pot_size = ''

			for char in pot_size:
				if char.isdigit() or char == '.':
					final_pot_size += char
			try:
				return float(final_pot_size)

			except:
				print('something went wrong with pot size string to float conversion; check if youre running pre flop there is no pot!')
				breakpoint()

	def scan_call_button_to_see_bet_amount(self):
		"""
		This function simply scans my 'call' button at the bottom of the screen, which shows the
		largest bet amount that I need to call to continue the hand.

		(R)!!! Two things to note:
		1) The detector cannot detect 'checks', because of the blur background of the button.
		so when it is my turn and I want to see if it has been 'checked' - do two things 1) the detector is ''
		and 2) scan a bit of the background of the button and check that it is blue.

		2) Otherwise if there is an amount to call the background of the button is green and it detects fine.
		"""
		# bet size on my button - VIDEO COORDINATES
		ss = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/largest_bet_size_my_button.png", region=(889, 1607, 149, 41))
		# ss.show()

		# bet size on my button - APP COORDINATES
		# ss = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/largest_bet_size_my_button.png", region=(889, 1607, 149, 43))
		# ss.show()

		image_path = f"{sys.path[0]}/photo_dump/largest_bet_size_my_button.png"
		final_bet_amount = read_white_text_on_image_my_button_bet_size(image_path, ss, self.stack_tracker, self.fold_tracker)

		return final_bet_amount

	def total_bet_amount_under_pot(self):
		"""
		This function will scan the number below the pot number, and return it.
		"""
		# VIDEO COORDINATES
		total_bet_amount_under_pot = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pot_size.png", region=(917, 683, 70, 32))
		# total_bet_amount_under_pot.show()
		# real app coordinates
		# total_bet_amount_under_pot = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pot_size.png", region=(917, 683, 70, 34))

		im = Image.open(f"{sys.path[0]}/photo_dump/pot_size.png")
		new_im = im.resize((109, 45))
		# new_im.show()
		total_bet_amount_under_pot = pytesseract.image_to_string(new_im, config='--psm 6')

		# SOMETIMES THE FULL STOP ISN'T DETECTED IN THE AMOUNT, SO DO A CHECK IF AMOUNT LOOKS SENSIBLE
		# Determine if we need to add a decimal point
		bet_larger_than_stack = 0
		for stack in self.stack_tracker:
			if self.stack_tracker[stack]:  # if empty seat or folded stack_tracker has value 0 for that seat
				if total_bet_amount_under_pot == '':
					continue
				if self.stack_tracker[stack] < float(total_bet_amount_under_pot):
					bet_larger_than_stack += 1
		number_of_players_in_pot = sum(1 for folded in self.fold_tracker.values() if not folded)

		if bet_larger_than_stack >= number_of_players_in_pot:
			# If the current bet amount is larger than most players' stack, need to add decimal point

			# Adding decimal point to third position from the right
			total_bet_amount_under_pot = total_bet_amount_under_pot[:len(total_bet_amount_under_pot)-2] + '.' + total_bet_amount_under_pot[len(total_bet_amount_under_pot)-2:]
			try:
				final_bet_amount = float(total_bet_amount_under_pot)
				return final_bet_amount
			except:
				print(f'bet amount looks like {total_bet_amount_under_pot}')
				breakpoint()

		return total_bet_amount_under_pot

	def how_much_can_i_raise_to(self):
		"""
		This function scans the number below the pot amount - and this number represents what the total pot is at
		the moment - including all of the bets before me. Whereas the top number represents the pot before any
		betting in the current round.

		This function will scan this bottom number and see what it is.
		It then determines what amount I can raise to if I wanted to raise, by doing the following calculation:

		1) amount_i_can_raise_to = Amount on my button x 3 + (the total pot amount including current bets - amount on my button button) ;

		2) if Amount on my button = 'Check', then I can just bet the pot of course.

		crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).
		"""
		total_bet_amount = self.total_bet_amount_under_pot()

		# it has been checked to me


	def calculate_SPR(self, how_much_can_i_bet_or_raise_to):
		"""
		In this function I simply take how much I can bet/raise to, and compare it to opponents' stack.

		So it's not really calculating SPR, but I get a good idea of what needs to be bet to get the money in,
		and on which street and whether I can/need to raise to achieve this.

		I will always compare it to the biggest stack - this makes the most sense, since we can be multi-way a lot of the times.

		FOR EXAMPLE:
		we are on the flop, it is my turn and I can raise to 300, and opponent with biggest stack has stack of 1700, then
		the SPR is 6ish; keep in mind the rule:
		(R)!!!!!!!
		**************************************
		- if SPR is 12 on the flop, you can get it in by the river by betting turn and river full pot.
		- if SPR is 27 on the flop you need to be able to raise to get in the money by the river by potting turn and river
		**************************************
		So with an SPR of 6ish, most of the money will go in on the turn if I pot it.

		FOR EXAMPLE:
		biggest stack 1200, I can bet 100 on flop and it is my turn to act, making an SPR of 12.
		flop: 300 in the middle if they call, they have 1100
		turn: pot 300, they call, pot is now 900 and they have 800 in stack.
		river: pot is 900 they have 800 in stack.
		"""
		spr_tracker = {}

		# N.B. regardless of whether it was bet ahead of me or checked, how_much_can_i_bet_or_raise_to will
		# hold the amount that can be bet/raised, so the SPR is just the opponent's stack divided by that. Simple.
		# N.B. stack_tracker will hold 0 for those who have folded.
		for opp in self.stack_tracker:
			spr_tracker[opp] = self.stack_tracker[opp] / how_much_can_i_bet_or_raise_to

		return spr_tracker

	def are_there_players_to_act_ahead_of_me(self, how_much_can_i_raise_to):
		"""
		This function will return True or False, indicating if there is a player(s) to act ahead of me.
		If I find later on I need to know how many, then I can add to this, but for now I don't think I need to know.

		Two possibilities:
		1) if it has been checked behind me, need to check if anyone still in pot that has not checked.
		2) if it has been bet behind me, then need to check if anyone still in pot that hasn't bet/called that amount
		There is a 'Call' button just like 'Check' and 'Bet', so use that.
		"""
		players_to_act_ahead_of_me = False
		curr_pos = self.my_position + 1

		# if it has been bet before me
		if how_much_can_i_raise_to > 0:
			while curr_pos != self.my_position:
				if curr_pos == 7:
					curr_pos = 1
				if self.scan_action_of_the_table_f[curr_pos] == 'check':
					players_to_act_ahead_of_me = True
					break
				curr_pos += 1

		# if it was checked before me
		else:
			while curr_pos != self.my_position:
				if curr_pos == 7:
					curr_pos = 1
				if not self.scan_action_of_the_table_f[curr_pos]:
					players_to_act_ahead_of_me = True
					break
				curr_pos += 1

		return players_to_act_ahead_of_me


def read_white_text_on_image_my_button_bet_size(image_path, ss, stack_tracker, fold_tracker):
	# Grayscale, Gaussian blur, Otsu's threshold
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (3,3), 0)
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	# Morph open to remove noise and invert image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
	invert = 255 - opening

	# Perform text extraction
	image_string_detected = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

	if not image_string_detected:
		# verify it was Checked by scanning the button; if it is a blue background it means it is a check.

		# crop the right side of the image so none of the white 'check' is in the picture, then detect blue colour
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
		# Determine if we need to add a decimal point
		bet_larger_than_stack = 0
		for stack in stack_tracker:
			if bet_amount == '':   # for testing - this occurs when it is not your turn and you run this function; your call button shows nothing
				continue
			if stack_tracker[stack] < float(bet_amount):
				bet_larger_than_stack += 1
		number_of_players_in_pot = sum(1 for folded in fold_tracker.values() if not folded)
		# breakpoint()
		if bet_larger_than_stack >= number_of_players_in_pot:
			# If the current bet amount is larger than most players' stack, need to add decimal point

			# Adding decimal point to third position from the right
			bet_amount = bet_amount[:len(bet_amount)-2] + '.' + bet_amount[len(bet_amount)-2:]
			try:
				final_bet_amount = float(bet_amount)
				return final_bet_amount
			except:
				print(f'bet amount looks like {bet_amount}')
				breakpoint()
		if not bet_amount:  # for testing, bet_amount will = ''
			return 0
		return float(bet_amount)


stack_tracker = {1: 633.46, 2: 58.19, 3: 271.84, 4: 311.57, 5: 342.21, 6: 382.34}
fold_tracker = {1: False, 2: True, 3: False, 4: False, 5: False, 6: False}
x = PotSizeAndActionBehindMe(4, fold_tracker, stack_tracker)
# print(f'total bet amount under the pot is: {x.how_much_can_i_raise_to()}')

# print(f'amount on my button is:{x.scan_call_button_to_see_bet_amount()}')

# REMINDER!: if you get an unexpected 'Fold' in scanning the billboard below, check what you have set the
# stack_tracker of that position, because if you set the stack to 0, then 'Fold' is correct!
# print(f'billboard action above each players head: {x.scan_action_of_the_table()}')

# print(f'the pot size is: {x.pot_size()}')

# For the below two functions, 'how_much_I_can_raise_to' are the arguments being passed into the function
# print(f'SPR of the table: {x.calculate_SPR(0)}')
# print(f'are there players to act ahead of me: {x.are_there_players_to_act_ahead_of_me(0)}')


