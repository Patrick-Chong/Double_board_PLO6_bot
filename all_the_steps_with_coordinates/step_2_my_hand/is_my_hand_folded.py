import numpy as np
import pyautogui
import sys
from PIL import ImageChops, Image

def calcdiff(im1_path, im2_path):
    im1 = Image.open(im1_path)
    im2 = Image.open(im2_path)
    dif = ImageChops.difference(im1, im2)

    return np.mean(np.array(dif))

    # comparing blacked out and non-blacked out, difference = 78ish
    # comparing blacked out and blacked out, difference = 2ish

    # times when no cards in front of me, difference is 23ish


def check_if_my_cards_are_live():
    """
    This function is simply to check whether my current hand is live - it will do
    this by looking at whether my cards are greyed out or not.
    It will return True if my hand is alive.

    To do this, take a pic of the non-blacked out hand and one of the blacked-out hand
    and do comparisons, just like with the button, can set a degree of accuracy.
    """
    # coordinates work for both video and app
    screenshot = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/ss_of_my_hand.png", region=(1060, 1390, 220, 58))
    ss_of_my_hand = f"{sys.path[0]}/photo_dump/ss_of_my_hand.png"
    my_hand_blacked_out = f"{sys.path[0]}/photo_dump/my_hand_blacked_out.png"
    # screenshot.show()

    if calcdiff(ss_of_my_hand, my_hand_blacked_out) >= 50: 
        return True
    else: 
        return False

print(check_if_my_cards_are_live())
