"""
EXTRA NOTES:
- Note the 'raise'/'bet' button always says 'bet' after the flop and 'raise' before the flop; but they represent the same thing.

"""
from collections import defaultdict
from all_the_steps_with_coordinates.step_7_detect_whos_turn_to_act.whos_turn_to_act import IsItMyTurnToAct
import cv2
import sys
import pyautogui
from PIL import Image
import pytesseract


class PreFlopHandCombinations:
    """
    This class defined all the general functions that helps to build up the type of hand;
    e.g. singleSuitedAce, TwoPairedHighCard, etc.
    """

    def __init__(self, my_position, num_list, suit_list):
        self.my_position = my_position
        self.num_list = num_list
        self.suit_list = suit_list

        # high card
        self.at_least_four_high_cards = self.count_high_cards()
        # suited
        self.single_suited_ace_f = self.single_suited_ace()
        self.single_suited_king_f = self.single_suited_king()
        self.double_suited_aces_f = self.double_suited_ace()
        self.double_suited_f = self.double_suited()
        # pair
        self.high_pair_in_my_hand_f = self.high_pairs_in_my_hand()  # returns an integer
        # running
        self.check_for_wrap_and_wrap_plus_pair_generator = self.check_for_wrap_and_wrap_plus_pair()
        self.wrap_no_pair = self.check_for_wrap_and_wrap_plus_pair_generator[0]
        self.wrap_plus_pair = self.check_for_wrap_and_wrap_plus_pair_generator[1]

    def count_high_cards(self):
        """
        Return true if:
        1) 4 high cards >= 10
        2) 5 high cards >= 9
        The above is with making a wrap in mind!
        """
        num_high_cards_greater_than_10 = 0
        num_high_cards_greater_than_9 = 0
        for card in self.num_list:
            if card >= 10:
                num_high_cards_greater_than_10 += 1
            if card >= 9:
                num_high_cards_greater_than_9 += 1
        return num_high_cards_greater_than_10 >= 4 or num_high_cards_greater_than_9 >= 5

    def single_suited_ace(self):
        if self.num_list[0] == 14:
            first_ace_suit = self.suit_list[0]
            if any(suit == first_ace_suit for suit in self.suit_list[1:]):
                return True

        if self.num_list[1] == 14:
            second_ace_suit = self.suit_list[1]
            if any(suit == second_ace_suit for suit in self.suit_list[2:]):
                return True

        if self.num_list[2] == 14:
            second_ace_suit = self.suit_list[2]
            if any(suit == second_ace_suit for suit in self.suit_list[3:]):
                return True
        return False

    def single_suited_king(self):
        if self.num_list[0] == 13:
            first_ace_suit = self.suit_list[0]
            if any(suit == first_ace_suit for suit in self.suit_list[1:]):
                return True
        if self.num_list[1] == 13:
            second_ace_suit = self.suit_list[1]
            if any(suit == second_ace_suit for suit in self.suit_list[2:]):
                return True
        if self.num_list[2] == 13:
            second_ace_suit = self.suit_list[2]
            if any(suit == second_ace_suit for suit in self.suit_list[3:]):
                return True
        if self.num_list[3] == 13:
            second_ace_suit = self.suit_list[3]
            if any(suit == second_ace_suit for suit in self.suit_list[4:]):
                return True

        return False

    def double_suited_ace(self):
        number_of_suited_aces = 0
        if self.num_list[0] == 14:
            first_ace_suit = self.suit_list[0]
            if any(suit == first_ace_suit for suit in self.suit_list[1:]):
                number_of_suited_aces += 1
        if self.num_list[1] == 14:
            second_ace_suit = self.suit_list[1]
            if any(suit == second_ace_suit for suit in self.suit_list[2:]):
                number_of_suited_aces += 1
        if self.num_list[2] == 14:
            third_ace_suit = self.suit_list[2]
            if any(suit == third_ace_suit for suit in self.suit_list[3:]):
                number_of_suited_aces += 1

        return True if number_of_suited_aces >= 2 else False

    def double_suited(self):
        count_of_suits = defaultdict(int)
        for i in self.suit_list:
            count_of_suits[i] += 1
        double_suited_count = 0
        for suit_count in count_of_suits.values():
            if suit_count > 1:
                double_suited_count += 1
        if double_suited_count > 1:
            return True
        return False

    def high_pairs_in_my_hand(self):
        """
        I consider a high pair to be a pair that is 10 or above.
        """
        count_of_num = defaultdict(int)
        for i in self.num_list:
            count_of_num[i] += 1  # {'A': 2, 10: 1, 5: 1, 2: 2}
        number_of_high_pairs = 0
        for num in count_of_num:
            if int(num) >= 10 and count_of_num[num] > 1:
                number_of_high_pairs += 1
        if number_of_high_pairs >= 1:
            return True
        else:
            return False

    def check_for_wrap_and_wrap_plus_pair(self):
        """
        This function will return two things:
        1) if I have a 4 card wrap
        2) if I have a 4 card wrap + pair

        nums_list = [13,12,12,7,5,3]

        (R)!!! WITH EPIPHANY AROUND WRAPS
        I won't play 3 cards wraps; they are weak.
        Only 4 or 5 cards wraps are strong enough.

        The only wraps I consider playing: [9, 8, 7], [9, 8, 6], [9, 7, 6], [9, 8, 5], [9, 6, 5]

        Comparing 3 card wrap to 4 or 5 card wraps:
        9 8 7; 9 8 7
        9 8 7 6 ; 9 8 7, 9 8 6, 9,7,6, 8, 7, 6
        9 8 7 6 5; 9 8 7, 9 8 6, 9 8 5, 9 7 6, 8 7 6, etc.

        The reason A K J 10 is stronger than any other one gapper 4 running cards is because:
        9 8 6 5; 9 8 6, 9 8 5
        9 8 5 although is a wrap (on a 7 6 board), it is dominated by 10 9 8.
        But with A K J 10, there is no higher wrap!!!!

        (Note that I didn't put a condition for the 'A' to be in there as a must, but I think I might need to, because
        otherwise my wrap can be dominated- I think!) - leave this note here until I run and see.

        Will only consider wraps higher than 5.

        One caveat, if there is a pair inbetween, we want to filter it out first at the start.
        e.g. 10 9 9 8 4 3 -> 10 9 8 4 3
        """
        # remove all pairs from num_list before checking for wraps
        filtered_num_list_take_out_pairs = [self.num_list[0]]
        for i in range(1, 5):
            if self.num_list[i] == self.num_list[i-1] or self.num_list[i] == self.num_list[i+1]:
                if self.num_list[i] not in filtered_num_list_take_out_pairs:
                    filtered_num_list_take_out_pairs.append(self.num_list[i])
            else:
                filtered_num_list_take_out_pairs.append(self.num_list[i])
        if self.num_list[-1] != filtered_num_list_take_out_pairs[-1]:
            filtered_num_list_take_out_pairs.append(self.num_list[-1])
        if len(filtered_num_list_take_out_pairs) < 4:
            return False
        # split num_list into combo of 4 cards
        all_combo_of_four = []
        for i in range(len(filtered_num_list_take_out_pairs)):
            all_combo_of_four.append(filtered_num_list_take_out_pairs[i:i+4])
            if len(filtered_num_list_take_out_pairs) - i == 4:
                break

        # look if I have wrap and/or wrap plus pair in my hand
        any_wrap_in_my_hand = False
        is_wrap_plus_pair_in_my_hand = False
        for combo in all_combo_of_four:
            is_wrap_in_my_hand = False
            difference_first_two_cards = combo[0] - combo[1]
            difference_second_two_cards = combo[1] - combo[2]
            difference_third_two_cards = combo[2] - combo[3]
            total_difference = difference_first_two_cards + difference_second_two_cards + difference_third_two_cards
            # 9 8 7 - no gap wrap
            if difference_first_two_cards == 1 and difference_second_two_cards == 1 and difference_third_two_cards == 1:
                is_wrap_in_my_hand = True
            # 9 7 6 5 - one gap wraps
            elif difference_first_two_cards == 2 and difference_second_two_cards == 1 and difference_third_two_cards == 1:
                is_wrap_in_my_hand = True
            # 9 8 7 5
            elif difference_first_two_cards == 1 and difference_second_two_cards == 1 and difference_third_two_cards == 2:
                is_wrap_in_my_hand = True
            # 9 8 6 5
            elif difference_first_two_cards == 1 and difference_second_two_cards == 2 and difference_third_two_cards == 2:
                is_wrap_in_my_hand = True
            # A K 10 9 - two gap wraps; will play only for high cards.
            if combo[3] >= 9 and total_difference <= 5:
                is_wrap_in_my_hand = True

            if is_wrap_in_my_hand:
                any_wrap_in_my_hand = True
                for num in combo:
                    if self.num_list.count(num) >= 2:
                        is_wrap_plus_pair_in_my_hand = True

        return any_wrap_in_my_hand, is_wrap_plus_pair_in_my_hand


class ShouldWePlayThisPreFlopHand(PreFlopHandCombinations):
    """
    This class will define all the types of hands I will play pre_flop_play.

    It will use functions from the above PreFlopHandCombinations, which is a helper functions
    where the functions define useful things about my hand construct like two paired high cards,
    or ace high flush, so that in this class I can refer to it without needing to write code to
    check if I have it.
    """

    def __init__(self, my_position, num_list, suit_list):
        PreFlopHandCombinations.__init__(self, my_position, num_list, suit_list)

    """
    Keep in mind I will play 99% of hands from positions 5 and 6.
    I think the most important thing is that the hand uses all 6 cards! - this constructs a high hand
    when we flop something. Of course a strong hand can miss the board completely too, but 
    when it hits you want ALL or most of the cards to play a part in the hand.
    
    Also remember I read that in Omaha, hands are made on the straight - so running cards are quite important - VERY! 
    
    I write these with DOMINATION in mind. 
    Having redraws to the nuts, and set over set, etc. 
    
    (R)!!! 
    Keep in mind what I read about being in position and playing less nutted hand because 
    you have the benefit of position, whereas if you play any hands OOP, you'll want to be nutted. 
    i.e. drawing to nut flush draw, as you don't have benefit of position and don't know as well 
    where you are vs. your opponent.
    
    IF I play hands in position 5 or 6 ALWAYS raise (it if hasn't been raised behind you).
    IF I play hands OOP ALWAYS call. 
    (unless SPR is low and you have double suited aces - so some caveats but not many)
    
    (R)!!!! 
    Position should play a part in determining if a hand is premium, so A 8 7 6 5 4 would be 
    premium hand if you are in position 6 but in position 1 it is a call hand.  
    (That's because IP you can bluff a lot more! - but OOP you need to play more straight forward, since 
    you lack opponent information).
    """

    def my_turn_to_act(self):
        is_it_my_turn_to_act = IsItMyTurnToAct()
        return is_it_my_turn_to_act.is_it_my_turn_to_act()

    def does_my_hand_meet_at_least_three_pillars(self):
        """
        STRATEGY:

        I will only play a hand if it meets the following criteria:
        1) at least 5 of the 6 cards are connected
        2) By connected I mean connect in some ways according to the 4 pillars: high, paired, suited, running
        - At least 3 of the pillars must be met for me to play the hand.
        So for example if he had three high paired in my hand but they're not suited or running then I won't play.

        (On second thought as long as 3/4 pillars are met I'll play the hand;
        because if you think about it as long as 3/4 pillars are met, can you think of a weak hand
        that meets 3/4 pillars, if so then change the strategy but if not, which I think not, then
        keep it like this)

        I think it's worth making a distinction between a very strong and a strong hand.
        Because I can think of hands where I would want to 3-bet that meet 3 pillars but others that I would not.
        For now leave it, to play safer even super storng hands don't three bet pre_flop, just go nuts when
        you hit something strong on flop. SOMETHING TO CONSIDER LATER ONCE THINGS ARE RUNNING.

        # high card
        self.at_least_four_high_cards = self.count_high_cards()  # True or False
        # suited
        self.single_suited_ace_f = self.single_suited_ace()
        self.single_suited_king_f = self.single_suited_king()
        self.double_suited_aces_f = self.double_suited_ace()
        self.double_suited_f = self.double_suited()
        # pair
        self.how_many_high_pair_in_my_hand_f = self.how_many_high_pairs_in_my_hand()  # returns an integer
        # running
        self.check_for_wrap_and_wrap_plus_pair_generator = self.check_for_wrap_and_wrap_plus_pair()
        self.wrap_no_pair = self.check_for_wrap_and_wrap_plus_pair_generator[0]
        self.wrap_plus_pair = self.check_for_wrap_and_wrap_plus_pair_generator[1]

        Initially I thought it might be worth keeping track of the pillars that I have, but I don't think it's
        necessary, just return 'bet' or 'fold' or 'call'.
        Look at notepad and see what the considerations are to decide, call, bet or fold.
        On the flop I check what I have already so no point doing the work here too.
        """
        pillars_of_a_strong_starting_hand = dict()
        pillars_of_a_strong_starting_hand['high_cards'] = self.at_least_four_high_cards
        pillars_of_a_strong_starting_hand['suited'] = [self.single_suited_ace_f or self.single_suited_king_f]
        pillars_of_a_strong_starting_hand['pair'] = self.high_pair_in_my_hand_f
        pillars_of_a_strong_starting_hand['running'] = [self.wrap_no_pair or self.wrap_plus_pair]
        number_of_pillars_met = 0
        for pillar in pillars_of_a_strong_starting_hand.values():
            if isinstance(pillar, list):
                if any(pillar):
                    number_of_pillars_met += 1
            else:
                if pillar:
                    number_of_pillars_met += 1
        if number_of_pillars_met < 3:
            return False
        return True

    def double_suited_aces(self):
        """
        Double suited aces is still a flip against most hands.
        Unless it's double suited aces with other cards running, then it's worth going all in with pre_flop.
        Anything short of that just call or raise if it hasn't been raised.
        """
        pass

    def all_six_cards_connected(self):
        """
        This is where we have running + paired + suited.

        Not as important if the cards or suits are high, because this is powerful if you hit the right flop.
        i.e. you can be flopping the opp dead.
        """
        pass


def read_white_text_on_image(image_path, ss):
    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    image_string_detected = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

    if not image_string_detected:
        # verify it was Checked by scanning the button; if it is a blue background it means it is a check.

        # crop the right side of the image so none of the white 'check' is in the picutre, then detect blue colour
        im = Image.open(image_path)
        cropped_image_for_blue = im.crop((120, 8, 200, 200))
        pixels = list(ss.getdata())
        total_pixels = len(pixels)
        num_of_blue_pixel = 0
        for pixel in pixels:
            r, g, b, c = pixel
            if b > 110:
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
        # add decimal point to three spaces from the right
        bet_amount = bet_amount[:len(bet_amount)-2] + '.' + bet_amount[len(bet_amount)-2:]
        try:
            final_bet_amount = float(bet_amount)
            return final_bet_amount
        except:
            print(f'bet amount looks like {bet_amount}')
            breakpoint()

def scan_call_button_to_see_bet_amount():
    """
    This function simply scans my 'call' button at the bottom of the screen, which shows the
    largest bet amount that I need to call to continue the hand.

    (R)!!! Two things to note:
    1) The detector cannot detect 'checks', because of the blur background of the button.
    so when it is my turn and I want to see if it has been 'checked' - do two things 1) the detector is ''
    and 2) scan a bit of the background of the button and check that it is blue.

    2) Otherwise if there is an amount to call the background of the button is green and it detects fine.
    """
    # bet size on my button
    ss = pyautogui.screenshot(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/largest_bet_size_my_button.png", region=(889, 1607, 149, 41))

    # image = Image.open(f"{sys.path[0]}/photo_dump/screenshots_of_stacks/largest_bet_size_my_button.png")
    # image.show()

    image_path = f"{sys.path[0]}/photo_dump/screenshots_of_stacks/largest_bet_size_my_button.png"
    final_bet_amount = read_white_text_on_image(image_path, ss)
    print(f'bet to call detected is:{final_bet_amount}')

    return float(final_bet_amount)


class RunPreFlop(ShouldWePlayThisPreFlopHand):

    def __init__(self, my_position, num_list, suit_list, big_blind, stack_tracker):
        ShouldWePlayThisPreFlopHand.__init__(self, my_position, num_list, suit_list)
        self.big_blind = big_blind
        self.stack_tracker = stack_tracker
        self.pre_flop_bet_amount = scan_call_button_to_see_bet_amount()

    def limped_or_3_bet_to_me_pre_flop(self):
        """
        This function tells us whether it has been limped to us or has been three_bet behind or more.

        The way to calculate is to scan my button and see what the amount is to call.

        Then there is a running 'pot' amount, and it includes the bet I am facing.
        So if you subtract the amount I need to call from the running bet, you get a good idea of whether it's been
        bet, 3-bet or more.

        Because before when I just
        """
        if self.pre_flop_bet_amount <= self.big_blind:
            return 'limped'
        elif self.big_blind < self.pre_flop_bet_amount <= 4 * self.big_blind:
            return 'bet'
        elif 4 * self.big_blind < self.pre_flop_bet_amount <= 10 * self.big_blind:
            return 'three_bet'
        else:
            print(f"Issue with limped bet or three bet detection, pre_flop bet size detected is {self.pre_flop_bet_amount}")
            breakpoint()

    def action_pre_flop(self, limped_or_3_bet_to_me_pre_flop):
        """
        To begin with, as less 'risky' approach is NOT to 3-bet pre_flop, though I'm quite sure this
        is profitable if done right, I still think the equity is too close to be doing this.
        Better to see a flop 'cheaply', then go ham if I connected hard with the flop.

        My play strategy with regards to position will be as follows, if I meet the 3 pillars:
        - If I am in position 5 or 6:
            - call a 3-bet (maybe I'll fold - play and see; what if it's 4-bet behind me?)
            The only way this is worth it is if I incorporate bluffs in, with position, I think.
            - raise if it has been limped
        - If I am in any other position:
            - Call any bets and limp if it has been limped.

        IN THIS FUNCTION I should consider all things I noted down on notepad to make the
        decision to 'bet', 'call' or 'fold' pre_flop:
        - SPR (only if SPR is now extremely low is this a consideration otherwise doesn't matter)
        - action behind me (particularly has it been 3-bet)
        - am I in position, play as per what it says above.
        - do I meet at least 3/4 pillars
        """
        if not self.does_my_hand_meet_at_least_three_pillars():
            return 'FOLD'
        premium_positions = (5, 6)
        if self.my_position in premium_positions:
            if limped_or_3_bet_to_me_pre_flop in ('three_bet', 'bet'):
                return 'CALL'
            if limped_or_3_bet_to_me_pre_flop == 'limped':
                return 'BET'
        else:
            if limped_or_3_bet_to_me_pre_flop in ('bet', 'limped'):
                return 'CALL'
        return 'FOLD'

    def pre_flop_action(self):
        extra_information = dict()  # store if someone 3-bet pre_flop
        limped_or_3_bet_to_me_pre_flop = self.limped_or_3_bet_to_me_pre_flop()
        action = self.action_pre_flop(limped_or_3_bet_to_me_pre_flop)
        extra_information['three_bet_pre_flop'] = True if limped_or_3_bet_to_me_pre_flop == 'three_bet' else False
        return action, extra_information

# x = RunPreFlop()
# print(scan_call_button_to_see_bet_amount())
# print(x.pre_flop_action())
