import sys
from PIL import Image
import pytesseract
import pyautogui


def get_stack_sizes(my_position, fold_tracker):
	"""
	This function will take a screenshot of all 6 stack sizes, including my own, and
	will add it to a list and return it.

	(R)!! V IMP 
	The list will hold the stack sizes according to positions starting with position 1, 
	i.e. the UTG player! 

	I think it makes the most sense doing it this way, because when I write code for my actual play 
	this is how I would consider it. 

	In the screenshot that I am writing this code for, I am in position 6, i.e. on the button.

	crop_rectangle tuple represents (LEFT, UPPER, RIGHT, LOWER).
	"""

	stack_tracker = dict()

	# my stack - video coordinates
	stack1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack1.png", region=(909, 1475, 94, 28))

	# guy to my left
	stack2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack2.png", region=(605, 1145, 94, 28))

	# guy two to my left
	stack3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack3.png", region=(654, 725, 94, 28))

	# guy top of screen
	stack4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack4.png", region=(909, 480, 94, 28))

	# top of screen + 1
	stack5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack5.png", region=(1162, 727, 94, 26))

	# top of screen + 2
	stack6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack6.png", region=(1210, 1145, 94, 28))


	# my stack - real app coordinates
	# my stack - video coordinates
	# stack1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack1.png", region=(909, 1475, 94, 30))
	#
	# # guy to my left
	# stack2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack2.png", region=(605, 1145, 94, 30))
	#
	# # guy two to my left
	# stack3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack3.png", region=(654, 725, 94, 30))
	#
	# # guy top of screen
	# stack4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack4.png", region=(909, 480, 94, 30))
	#
	# # top of screen + 1
	# stack5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack5.png", region=(1162, 727, 94, 30))
	#
	# # top of screen + 2
	# stack6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack6.png", region=(1210, 1145, 94, 30))

	# stack1.show()
	# stack2.show()
	# stack3.show()
	# stack4.show()
	# stack5.show()
	# stack6.show()

	# Assuming that I am in position 5; but in reality my position will be passed into this function as an argument.
	current_position = my_position
	for i in range(1, 7):
		# stack1 will always be my stack.
		im = Image.open(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/stack{i}.png")

		new_im = im.resize((100, 45))

		new_im.show()

		current_stack = pytesseract.image_to_string(new_im, config='--psm 6')
		stack_tracker[current_position] = current_stack
		current_position = (current_position + 1) % 7

		# To adjust for the fact that modulo has 0 but my positions start from 1
		if current_position == 0: 
			current_position = 1

	# Cleaning up the stack sizes, they will be floats after the clean
	for key in stack_tracker:
		if fold_tracker[key]:  # they have folded or seat is empty
			stack_tracker[key] = 0
			continue

		stack = stack_tracker.get(key)
		hand = ''

		for num in stack:
			try:
				int_num = int(num)
				hand = hand + num
			except:
				pass
		hand = hand[:len(hand)-2] + '.' + hand[len(hand)-2:]
		try:
			stack_tracker[key] = float(hand)
		except:
			print(f'something went wrong converting a stack: {hand} to float')
			breakpoint()

	print(f'stack tracker: {stack_tracker}')
	return stack_tracker


print(get_stack_sizes(1, {1: False, 2: False, 3: True, 4: False, 5: False, 6: False}))
# print(all_in_checker({1: 'Fold', 2: 8.26, 3: 'Fold', 4: 'Fold', 5: '/(', 6: 60.30}, 6, 5))
