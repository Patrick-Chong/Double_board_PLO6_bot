import pyautogui
import time



# print(pyautogui.position()) # tells you the position of where your mouse currently is on screen.

# pyautogui.moveTo(536, 869) # used to move the mouse to this point, the third arg is the number of second to get to that position, 
#                            # nothing is passed, the mouse moves there instantaneously.

# pyautogui.dragTo(100, 200, button='left') # drag mouse to X of 100, Y of 200 while holding down left mouse button

# pyautogui.click() # click the mouse


def click_fold_call_bet(action): 
	"""
	'action' argument will be one of three input strings: 'CALL', "FOLD", 'BET'.

	Note that Call/check and bet/raise are the same button, so just use the same name. 

	This function will click on whatever 'action' tells us to click on.

	"""

	# Bet button position: (x=536, y=869)
	# Call button position: (x=379, y=868)
	# Fold button position: (x=213, y=866)

	if action == 'FOLD': 
		pyautogui.moveTo(320, 815)
		pyautogui.click(x=320, y=815, clicks=2, interval=1)

	elif action == 'CALL': 
		pyautogui.moveTo(495, 815)
		pyautogui.click(x=495, y=815, clicks=2, interval=1)

	elif action == 'BET': 
		pyautogui.moveTo(635, 815)
		time.sleep(0.01)
		pyautogui.click(x=635, y=815, clicks=2, interval=1)
		pyautogui.moveTo(535, 815)  # move to the POT button
		time.sleep(0.01)
		pyautogui.click(x=535, y=815, clicks=2, interval=1)
		pyautogui.moveTo(635, 815)
		time.sleep(0.01)
		pyautogui.click(x=635, y=815, clicks=2, interval=1)

	else: 
		print(f'the action is {action}; BET, CALL or FOLD was not detected for some reason')
		breakpoint()


# print(click_fold_call_bet('CALL'))
