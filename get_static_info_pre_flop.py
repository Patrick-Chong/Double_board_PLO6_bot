"""
THE BELOW IS TO BE RUN ONCE PRE-FLOP.
Because this information doesn't change while we are in the same hand.

"""
from all_the_steps_with_coordinates.step_6_number_of_players_in_pot.num_of_players_in_pot import DetectEmptySeat
from all_the_steps_with_coordinates.step_9_blinds_of_the_table.blinds_of_table import table_blinds
from all_the_steps_with_coordinates.step_2_my_hand.generate_num_and_suit_list import generate_num_list_from_my_hand
import pyautogui
import sys
from PIL import ImageChops, Image


class MyPositionClass:
    """
    All this class does is identify my position.
    """

    @staticmethod
    def determine_white_pixels(pos):
        image = Image.open(pos)
        pixels = list(image.getdata())
        white_pix_count = 0

        for pixel in pixels:
            # if more than 2 of RGB are greater than 245, then it is a white pix
            individual_white_pix_count = 0
            for individual_pixel in pixel:
                if individual_pixel >= 245:
                    individual_white_pix_count += 1
            if individual_white_pix_count >= 3:
                white_pix_count += 1
            if white_pix_count >= 100:
                # this is the button image, we have found the button
                return True
        return False

    @staticmethod
    def take_SS_and_determine_position():
        """
        This function takes a screenshot of the 6 different places the button can be,
        and determines what position we are in, relative to the button
        """
        # REAL APP coordinates
        # my position
        pos1 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos1.png", region=(844, 1336, 37, 37))
        pos1_path = f"{sys.path[0]}/photo_dump/pos1.png"
        # guy one to my left
        pos2 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos2.png", region=(722, 1165, 37, 37))
        pos2_path = f"{sys.path[0]}/photo_dump/pos2.png"
        # guy two to my left
        pos3 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos3.png", region=(765, 745, 37, 37))
        pos3_path = f"{sys.path[0]}/photo_dump/pos3.png"
        # guy top of screen
        pos4 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos4.png", region=(878, 499, 37, 37))
        pos4_path = f"{sys.path[0]}/photo_dump/pos4.png"
        # guy top of screen + 1
        pos5 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos5.png", region=(1129, 745, 37, 37))
        pos5_path = f"{sys.path[0]}/photo_dump/pos5.png"
        # guy top of screen + 2
        pos6 = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/pos6.png", region=(1175, 1167, 37, 37))
        pos6_path = f"{sys.path[0]}/photo_dump/pos6.png"
        pos_path = [pos1_path, pos2_path, pos3_path, pos4_path, pos5_path, pos6_path]

        # pos1.show()
        # pos2.show()
        # pos3.show()
        # pos4.show()
        # pos5.show()
        # pos6.show()
        button_with = None
        for pos in pos_path:
            if MyPositionClass.determine_white_pixels(pos):
                button_with = pos
        if not button_with:
            print('No button found, check screen position')
            breakpoint()
        if button_with == pos1_path:
            return 6
        elif button_with == pos2_path:
            return 5
        elif button_with == pos3_path:
            return 4
        elif button_with == pos4_path:
            return 3
        elif button_with == pos5_path:
            return 2
        elif button_with == pos6_path:
            return 1


class RunFirstOneTime(MyPositionClass):

    @staticmethod
    def determine_table_blinds():
        blinds_of_table = table_blinds()
        possible_table_blinds = ('0.20/0.40', '0.30/0.60', '0.5/1', '1/2', '2/4')
        possible_big_blinds = {'0.20/0.40': '0.4', '0.30/0.60': '0.6', '0.5/1': '1', '1/2': '2', '2/4': '4'}
        for tb in possible_table_blinds:
            if tb in blinds_of_table:
                return float(possible_big_blinds[tb])
        else:
            print('Could not determine table blinds')
            breakpoint()

    @staticmethod
    def run_num_list_suit_list():
        num_list, suit_list = generate_num_list_from_my_hand()

        # num list are all integers, and suit list are all strings
        return num_list, suit_list


# MPC = MyPositionClass()
# print(MPC.take_SS_and_determine_position())
