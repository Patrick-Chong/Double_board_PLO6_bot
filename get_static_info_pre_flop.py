"""
THE BELOW IS TO BE RUN ONCE PRE-FLOP. 
After the flop the cards in the middle get in the way of the screenshots.

(R)!!! 
I FINALLY UNDERSTAND WHY CLASSES ARE USED. This is a perfect example of why they can be so useful, if I dump all of the functions 
in the different scripts into a class, then just import that class here, I can call on each of the functions easily! 
Otherwise I would have to manually import each function from each script!!! 

Another thing to note is that when I import classes and run this script, ''sys.path[0]'' doesn't point where you think it points; 
it starts from the directory that this script is in! 
SO I had to create a 'photo_dump' directory in this working directory that will hold all the screenshots as we go along.
Then change the path of all of the screenshots and anything with sys.path[0] to point to the photo_dump.

Need to add certain folders into photo dump! e.g. six_individ_cards_for_num and six_individ_cards_for_suit.

Note that I cannot just run the scipts directly, becuase it is tough to get the output of the scripts! 
So I'll import the classes and function into a script that will run everything and get the output that way.





(R)!!! V IMP 
The first few steps below are built for just one table, since I am taking a screenshot of just the one table, but if I play multiple tables 
I need to adjust the code such that I am detecting the yellow strip on the top of the screem, i.e. only when it is my turn to act. 
This should be fine, because I have 15-18 seconds to act, which should be enough time to run the script and make a decision.

"""
from all_the_steps_with_coordinates.step_2_my_hand.app import run_num_list_suit_list
from all_the_steps_with_coordinates.step_6_number_of_players_in_pot.num_of_players_in_pot import DetectEmptySeat
from all_the_steps_with_coordinates.step_9_blinds_of_the_table.blinds_of_table import table_blinds
import pyautogui
import sys
from PIL import ImageChops, Image


class MyPositionClass:

    @staticmethod
    def determine_white_pixels(pos):
        """
        The button has been a pain to deal with up until now.
        Best logical way is to detect the amount of white on the image because only the button will
        have lots of white pixels.

        white pixels have RGB of 255, while black have RGB of 0.
        """
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

    def __init__(self):
        self.my_position = MyPositionClass.take_SS_and_determine_position()
        self.num_list = run_num_list_suit_list()[0]  # [14, 14, 10, 6, 5, 2]
        self.suit_list = run_num_list_suit_list()[1]  # ['C', 'D', 'S', 'H', 'H', 'S']
        self.empty_seat_tracker_f = RunFirstOneTime.get_empty_seat_tracker(self.my_position)
        self.big_blind = RunFirstOneTime.determine_table_blinds()

    @staticmethod
    def get_empty_seat_tracker(my_position):
        DES = DetectEmptySeat()
        empty_seat_tracker = DES.detect_empty_seat(my_position)
        # Determine how many players are on table by counting non-empty seats
        no_players_on_table = 0
        for seat in empty_seat_tracker:
            if not empty_seat_tracker[seat]:
                no_players_on_table += 1
        return empty_seat_tracker

    @staticmethod
    def determine_table_blinds():
        blinds_of_table = table_blinds()
        possible_table_blinds = ('0.20/0.40', '0.30/0.60', '0.5/1', '1/2', '2/4')
        possible_big_blinds = {'0.20/0.40': '0.4', '0.30/0.60': '0.6', '0.5/1': '1', '1/2': '2', '2/4': '4'}
        return 0.4
        # for tb in possible_table_blinds:
        #     if tb in blinds_of_table:
        #         return float(possible_big_blinds[tb])
        # else:
        #     print('Could not determine table blinds')
        #     breakpoint()


MPC = MyPositionClass()
print(MPC.take_SS_and_determine_position())
