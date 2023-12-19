"""
Note from suit_list generation.

The way to build this is to detect either RED, BLUE, GREEN OR BLACK on screen.

(R)!!! V IMP
In the previous script, we cropped the image of the six cards in my hand into six
individual cards.
For each card I did something like crop_rectange = (10, 7, 50, 100)
Where the tupe represents the PIXELS!!!! of the dimensions of the image I am cropping.
The tuple represents the (LEFT, UPPER, RIGHT, LOWER) of the image.
So for the above example I we have a 40x93 pixel image!
Can calculate this by doing LEFT - RIGHT and UPPER - LOWER

image.shape ; gives you the pixel dimensions of the image
image = cv2.imread(f"{sys.path[0]}/six_individ_cards_in_my_hand/wi_40x93.png")
40x93 image


list(image.getdata()) returns ALL of the pixels of the image; going row by row
so if you apply to the above image, you will get a total of 40 x 93 =3720 pixels
"""

import sys
from PIL import Image
import pytesseract
import pyautogui


def convert_J_Q_K_A(num_list):
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

def collect_card_suit():
	suit_list = []
	for i in range(1, 7):
		suit_list.append(determine_black_SPADES(i))
	return suit_list

def determine_black_SPADES(card_number):
	"""
	The way to differentiate a black suit from the other colours (red, green, blue) is to take the
	difference between R,G,B of each pixel.
	The difference in general is far greater for non-black cards.
	So I will use a count for the number of dispersions higher than a certain number to determine
	if we have a black card.
	"""
	image = Image.open(f"{sys.path[0]}/photo_dump/six_individ_cards_for_num/card{card_number}.png", "r")
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
		return determine_suit_Clubs_Hearts_Diamonds(card_number)

	else:
		return 'S'

def determine_suit_Clubs_Hearts_Diamonds(card_number):
	"""
	THE WAY TO DETERMINE RED, BLUE OR GREEN IS AS FOLLOWS:

	1. GET ALL OF THE PIXELS WHOSE FIRST 3 VALUES ARE LESS THAN 180
	2. GET THE HIGHEST NUMBERS OF EACH OF THE 3
	3. IF THE HIGHEST NUMBER IS IN THE FIRST SLOT, IT IS A RED CARD
	IF HIGHEST NUMBER IS IN SECOND SLOT THEN IT'S A GREEN CARD
	IF HIGHEST NUMBER IS IN THIRD SLOT THEN IT'S A BLUE CARD
	(The reason for this is that each slot represents (R,G,B) colour breakdown of the pixel)

	WE NEED STEP 1 TO FILTER OUT ALL OF THE WHITE PIXELS.

	I take the aaverage of the 3 slots to ensure I eliminate outliers.

	I also first check that I am not dealing with a black spade by checking the difference
	in each pixel's R,G,B value; if it is black or white the difference is very small, but
	if it is one of red, blue or green the difference is quite large.
	"""

	image = Image.open(f"{sys.path[0]}/photo_dump/six_individ_cards_for_num/card{card_number}.png", "r")
	pixels = list(image.getdata())

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


def generate_suit_list_from_my_hand():
	# crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).

	im = Image.open(f"{sys.path[0]}/photo_dump/my_hand.png")
	rectangle_dimensions_of_six_cards_higher_up = [(2, 0, 23, 80), (28, 0, 52, 80), (54, 0, 79, 80),
													(79, 0, 104, 80), (106, 0, 130, 80), (133, 0, 156, 80)]

	for i in range(6):
		crop_rectangle = rectangle_dimensions_of_six_cards_higher_up[i]
		cropped_im = im.crop(crop_rectangle)

		# if i == 5:
		# 	cropped_im.show()
		# 	breakpoint()
		cropped_im.save(f"{sys.path[0]}/photo_dump/six_individ_cards_for_num/card{i+1}.png")
		cropped_im = Image.open(f"{sys.path[0]}/photo_dump/six_individ_cards_for_num/card{i+1}.png")
		resized_im = cropped_im.resize((65, 60))

	return collect_card_suit()

def generate_num_list_from_my_hand(): 
	"""
	crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).

	Some rules for detecting hand:
	1) Sometimes a card is not detected at all, so my code adds a 10 in its place, which is obv not right.
	Added to the fact that 10's always have a letter or a '0'.
	So this rule is that if a '0' or a letter is not found and we are missing a card, then rescan my hand.


	"""
	# Common cards used to fill num list
	common_num_cards = {'A', 'K', 'Q', 'J', '9', '8', '7', '6', '5', '4', '3', '2'}

	num_list = []
	suit_list = []

	# Video coordinates
	pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(535, 126, 158, 37))
	pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(543, 127, 158, 37))
	pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(543, 126, 159, 37))
	ss_of_my_hand = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(529, 123, 158, 37))
	ss_of_my_hand.show()

	# THIS IS FOR num_list - real app coordinates
	# pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(535, 126, 158, 39))
	# pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(543, 127, 158, 39))
	# pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(543, 126, 159, 39))
	# ss_of_my_hand = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/my_hand.png", region=(529, 123, 158, 39))
	# ss_of_my_hand.show()

	current_num = pytesseract.image_to_string(ss_of_my_hand, config='--psm 6')
	# current_num looks like this here: 'KJ0632\n' ; there's always that escape thing at the end, so ignore it.
	current_num = current_num[:len(current_num)-1]
	# print(f'my hand_num is {current_num}')

	for num in current_num:
		if num in common_num_cards:
			num_list.append(num)

	number_of_10_to_add = 6 - len(num_list)

	if number_of_10_to_add > 0:
		for _ in range(number_of_10_to_add):
			num_list.append('10')

	# Examples of what current_num can be: 'KJ0632', 'Qau9985', 'K09944', '005542', 'Q0 7653', 'QN6432', 'Qann852', 'Ai7522'
	# It detects everything perfectly except for 10.
	# The above examples is actually 'KJ10632', 'Q109985', 'K109944', '10105542', 'Q107653', 'Q106432', 'Q1010852', 'A107522'

	# So I noticed when 10 is by itself it gets detected as a letter or a bunch of letters or a 0.
	# When two 10's are next to each other it's commonly three lower case letters.

	# I think the approach is to map the others then look at how many cards I am missing and fill it in from there.
	# EVERY SINGLE TIME I'VE RUN THE DETECTOR IT HAS DETECTED WITH 100% EVERYTHING EXCEPT FOR '10', #
	# SO THE APPORACH IS TO FILL IN ALL BUT 10, THEN JUST ADD THE NUMBER OF MISSING NUMS WITH 10.

	# before I didn't need to sort num_list but because of the 10 being added at the end of the list
	# now it needs to be sorted. But first we convert the face cards into numbers.
	num_list = convert_J_Q_K_A(num_list)
	num_list = sorted(num_list, key=int, reverse=True)

	# convert num list face cards to numbers
	num_list = get_num_list(num_list)

	# get the suit_list
	suit_list = generate_suit_list_from_my_hand()

	return num_list, suit_list


def ten_checker(final_num_list, pos_of_1):
    """
    Very often '10' is recognised as '1' in my hand.
    So I will map '1' -> '10', and while doing this there are checks to make sure that the '1' is indeed meant to be
    a '10' ; they are not 100% guarantees, but the check is pretty good; and that is to check that
    all cards to the right of
    """

    # i.e. 1 is the first card in my hand
    if pos_of_1 == 0:
        for num in range(1, len(final_num_list)):
            if final_num_list[num] > 10:
                return False

    # if 1 is the last card in my hand
    if pos_of_1 == 5:
        for num in range(5):
            if final_num_list[num] < 10:
                return False

    # if 1 is any card inbetween the first and last card in my hand
    for num in range(pos_of_1):
        if final_num_list[num] < 10:
            return False
    for num in range(pos_of_1, len(final_num_list)):
        if final_num_list[num] > 10:
            return False

    return True

def get_num_list(num_list_with_face_cards_to_be_converted_to_numbers):
	num_list_all_nums = []  # will hold the final num_list
	final_num_list = []
	convert_jack_queen_king_ace = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
	for pos, num in enumerate(num_list_with_face_cards_to_be_converted_to_numbers, 0):
		if num in convert_jack_queen_king_ace:
			num_list_all_nums.append(convert_jack_queen_king_ace.get(num))
		else:
			num_list_all_nums.append(num)
	try:
		final_num_list = [int(num) for num in num_list_all_nums]

	except:
		print(f'something wrong with num_list: {num_list_all_nums}')
		breakpoint()

	# Often the 10 in my hand gets read as a 1, so if a 1 is detected, check that all the numbers to its
	# right are smaller than a 10, if so then you can be quite confident that 1 was misread as 10.
	# Also check that all the cards to the left of it is larger than it!
	for pos, num in enumerate(final_num_list):
		if num == 1:
			if ten_checker(final_num_list, pos):
				final_num_list[pos] = 10

	# N.B. A good check to do is to check if the cards in my hands are sorted - they always should be,
	# because pokerbros sorts the nums from largest to smallest - ALWAYS
	# So if it is not in sorted order, likely the card reader has some issues, so break and find out
	for i in range(len(final_num_list)-1):
		if final_num_list[i] < final_num_list[i + 1]:
			print(f'num_list is not in sorted order - nums detection something wrong, num_list: {final_num_list}')
			breakpoint()

	return final_num_list  # e.g. [14, 10, 5, 4, 3, 2]

num_list, suit_list = generate_num_list_from_my_hand()
print(num_list, suit_list)
