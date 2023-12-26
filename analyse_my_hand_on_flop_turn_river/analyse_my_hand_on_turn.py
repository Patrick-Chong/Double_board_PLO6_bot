"""
What I will consider in this package:
1) The turn card on both flops
2) Did the turn card change the nuts or complete anything? (with hand ratings 4 & 5 we care if nuts change or things completed)
3) My hand rating on turn (could be very different to hand rating on flop)
4) Do I check, bet, raise? To decide this, need to consider:
- SPR
- Anyone ahead of me to act
- My hand rating on turn

- For exploit look at things like if the nuts changed on the turn card
(for now just play straight forward- bet if you have it, check if you do not).
"""


from collections import Counter
from analyse_my_hand_on_flop import AnalyseMyHandOnFlop

from flop_turn_river_cards import TheTurn
TT = TheTurn()


class AnalyseMyHandOnTurn(AnalyseMyHandOnFlop):
    """
    Before I made a distinction between if flush or straight or board paired on the flop vs. on turn.
    After thinking about it, this distinction is not necessary.
    I'll just look at each street separately, no need to connect them!
    """

    def __init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                 positions_of_players_to_act_ahead_of_me,
                 pot_size, my_position, num_list, suit_list, big_blind):

        AnalyseMyHandOnFlop.__init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)

        # dynamic information
        self.positions_of_players_to_act_ahead_of_me = positions_of_players_to_act_ahead_of_me
        self.guy_to_right_bet_size = guy_to_right_bet_size  # it is a float, it is 0 if checked.
        self.SPR_tracker = SPR_tracker
        self.pot_size = pot_size
        self.stack_tracker = stack_tracker

        # adding the turn cards to the flop
        self.turn1, self.turn2 = self.organise_turn()

        # Check what is available to hit on the turn
        # Did board pair
        self.did_board_pair_on_turn_generator = AnalyseMyHandOnTurn.did_board_pair_on_turn(self.turn1)
        self.did_board_pair_on_turn1 = self.did_board_pair_on_turn_generator[0]
        self.board_pair_top_card_turn1 = self.did_board_pair_on_turn_generator[1]
        self.did_board_pair_on_turn_generator = AnalyseMyHandOnTurn.did_board_pair_on_turn(self.turn2)
        self.did_board_pair_on_turn2 = self.did_board_pair_on_turn_generator[0]
        self.board_pair_top_card_turn2 = self.did_board_pair_on_turn_generator[1]
        # Did flush complete
        self.flush_complete_on_turn = AnalyseMyHandOnTurn.flush_completed_on_turn(self.turn1)
        self.did_flush_completed_on_turn1 = self.flush_complete_on_turn[0]
        self.nut_flush_nums_turn1 = self.flush_complete_on_turn[1]
        self.suit_of_flush_turn1 = self.flush_complete_on_turn[2]
        self.flush_complete_on_turn = AnalyseMyHandOnTurn.flush_completed_on_turn(self.turn2)
        self.did_flush_completed_on_turn2 = self.flush_complete_on_turn[0]
        self.nut_flush_nums_turn2 = self.flush_complete_on_turn[1]
        self.suit_of_flush_turn2 = self.flush_complete_on_turn[2]
        # Did straight complete
        self.any_straight_completed_on_turn_generator = AnalyseMyHandOnTurn.any_straight_completed_on_turn(self.turn1)
        self.did_straight_complete_on_turn1 = self.any_straight_completed_on_turn_generator[0]
        self.two_card_combi_completing_straight_on_turn1 = self.any_straight_completed_on_turn_generator[1]
        self.any_straight_completed_on_turn_generator = AnalyseMyHandOnTurn.any_straight_completed_on_turn(self.turn2)
        self.did_straight_complete_on_turn2 = self.any_straight_completed_on_turn_generator[0]
        self.two_card_combi_completing_straight_on_turn2 = self.any_straight_completed_on_turn_generator[1]

        # Any flush draws on turn
        self.flush_draw_on_turn_generator = AnalyseMyHandOnTurn.any_flush_draw_on_turn(self.turn1)
        self.is_flush_draw_on_turn1 = self.flush_draw_on_turn_generator[0]
        self.list_of_nut_flush_draw_num_suit_on_turn1 = self.flush_draw_on_turn_generator[1]
        self.flush_draw_on_turn_generator = AnalyseMyHandOnTurn.any_flush_draw_on_turn(self.turn2)
        self.is_flush_draw_on_turn2 = self.flush_draw_on_turn_generator[0]
        self.list_of_nut_flush_draw_num_suit_on_turn2 = self.flush_draw_on_turn_generator[1]
        # Any wrap draws on turn
        self.wrap_draw_on_turn_generator = AnalyseMyHandOnTurn.any_wrap_draw_on_turn(self.turn1)
        self.is_wrap_draw_on_turn1 = self.wrap_draw_on_turn_generator[0]
        self.list_of_all_three_card_wrap_combi_turn1 = self.wrap_draw_on_turn_generator[1]
        self.wrap_draw_on_turn_generator = AnalyseMyHandOnTurn.any_wrap_draw_on_turn(self.turn2)
        self.is_wrap_draw_on_turn2 = self.wrap_draw_on_turn_generator[0]
        self.list_of_all_three_card_wrap_combi_turn2 = self.wrap_draw_on_turn_generator[1]

        # Check what I have hit on the turn
        """
        (R)!!!!! 
        Had an excellent idea on how to code what I have. 
        1) Check both turns and look at what nuts are available (by using the functions I have written above)
        2) Then simply check how 'nutty' my hand is based on 1), and do my hand rating 6 to 4.
        it is as simple as that. 
        """



    def organise_turn(self):
        """
        self.flop looks like: [[13, 'S'], [10, 'C'], [9, 'S']]
        turn will look like: [[13, 'S'], [10, 'C'], [9, 'S'], [8, 'C']] ; after we sort it.
        """
        turn1_card, turn2_card = TT.detect_turn_nums_and_suit()
        # TO DO: add a breakpoint here when running integration test and check if self.flop is correct, prviously
        # it got messed up and it took the value of the turn and I couldn't figure out why.

        # Add both turn cards to the flops
        turn1 = self.flop1.append(turn1_card)
        turn2 = self.flop2.append(turn2_card)

        # Sort the turn cards with flop so everything is in descending order
        turn1 = sorted(turn1, key=lambda x: x[0], reverse=True)  # Sorting from largest to smallest, hence reverse=True
        turn2 = sorted(turn2, key=lambda x: x[0], reverse=True)  # Sorting from largest to smallest, hence reverse=True

        return turn1, turn2

    @staticmethod
    def did_board_pair_on_turn(turn):
        """
        This function returns:
        1) If the board paired
        2) If the board paired the highest card.
        """
        turn_nums = [card[0] for card in turn]
        highest_num_on_turn = turn_nums[0]
        count_nums_on_turn = Counter(turn_nums)  # Counter(10: 2, 7: 1, 4: 1})

        if len(set(turn_nums)) < 4:
            return True, True if count_nums_on_turn[highest_num_on_turn] >= 2 else False

    @staticmethod
    def flush_completed_on_turn(turn):
        """
        This function will return:
        1) if there is a flush completed on turn
        2) What the nut flush nums card is
        3) What the nut flush suit card is
        (R)!!! - note that this is NOT the highest num on the board that has that suit.
        e.g. [14, 13, 12, 2] and they are all 'hearts', then this function will return 11 as the nut flush nums.
        """
        nut_flush_num = None
        turn_suits = [card[1] for card in turn]
        suit_counter = Counter(turn_suits)  # Counter({'C': 2, 'S': 1, 'H': 1})

        for suit_card in suit_counter:
            if suit_counter[suit_card] >= 3:
                # N.B. To find the nut nums of the flush, iterate from 14 down
                # and the first card that you do not find is the nut flush
                for num in reversed(range(15)):  # iterates from 14
                    if [num, suit_card] not in turn:
                        nut_flush_num = num
                        break
                return True, nut_flush_num, suit_card
        return False, False, False

    @staticmethod
    def any_straight_completed_on_turn(turn):
        """
        This function will return:
        1) If there is a made straight on the turn
        2) A list of two card combis that complete the straight

        Check if there's a straight by look at 3 cards at a time, and since it is sorted we need to check 2 lots of 3,
        as there are only 4 cards.
        There is a made straight only if the gap between the 3 cards is no more than 4.
        e.g. 10, 7, 6 or 10, 8, 6 or 10 9 8

        self.turn1 looks like [[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]
        """
        turn_numbers = [card[0] for card in turn]

        for num in range(2):
            if num == 0:
                num1 = turn_numbers[0]
                num2 = turn_numbers[1]
                num3 = turn_numbers[2]
            else:
                num1 = turn_numbers[1]
                num2 = turn_numbers[2]
                num3 = turn_numbers[3]
            if (turn_numbers[num1] - turn_numbers[num2]) + (turn_numbers[num2] - turn_numbers[num3]) <= 4:
                # 10 7 6 or 10 9 6
                if (turn_numbers[num1] - turn_numbers[num2]) == 3 or (turn_numbers[num2] - turn_numbers[num3]) == 3:
                    return True, [[num for num in reversed(range(turn_numbers[num1], turn_numbers[num3])) if num not in turn]]
                # 10 8 6
                elif (turn_numbers[num1] - turn_numbers[num2]) == 2 or (turn_numbers[num2] - turn_numbers[num3]) == 2:
                    return True, [[turn_numbers[0]-1, turn_numbers[1]-2]]
                # 10 9 8
                elif (turn_numbers[num1] - turn_numbers[num2]) == 1 or (turn_numbers[num2] - turn_numbers[num3]) == 1:
                    # edge case if highest card is 14 or 13
                    if turn_numbers[num1] == 14:
                        return True, [[turn_numbers[num3]-1, turn_numbers[num3]-2]]
                    elif turn_numbers[num1] == 13:
                        return True, [[turn_numbers[num1]+1, turn_numbers[num3]-1], [turn_numbers[num3]-1, turn_numbers[num3]-2]]
                    else:
                        return True, [[turn_numbers[num1]+2, turn_numbers[num1]+1], [turn_numbers[num1]+1, turn_numbers[num3]-1], [turn_numbers[num3]-1, turn_numbers[num3]-2]]
        return False, None

    @staticmethod
    def any_flush_draw_on_turn(turn):
        """
        This function will return:
        1) If there is a flush draw available on the turn
        2) [The nut flush draw num, The nut flush draw suit]
        N.B. 2) will be a list of nut flush num,suit ; because there could be up to two flush draws on the turn
        """
        nut_flush_num_and_suit_list = []
        turn_suits = [card[1] for card in turn]
        suit_counter = Counter(turn_suits)  # Counter({'C': 2, 'S': 1, 'H': 1})

        for suit_card in suit_counter:
            if suit_counter[suit_card] == 2:
                for num in reversed(range(15)):  # iterates from 14
                    if [num, suit_card] not in turn:
                        nut_flush_num_and_suit_list.append([num, suit_card])
                        break
        if nut_flush_num_and_suit_list:
            return True, nut_flush_num_and_suit_list
        else:
            return False, []

    @staticmethod
    def any_wrap_draw_on_turn(turn):
        """
        This function returns
        1) if there is a wrap draw possible on the turn
        2) A lit of all 3 card wrap combinations

        I thought about writing a function for straight draw, but not worth it - not enough equity to play it;
        even if you have a pure wrap draw on turn, you are only 25% at best to hit it on the river.

        Also, haven't considered lower wrap with ace! E.g. if 14 13 5 2 ; I consider 4,3,1 to be a wrap, but I need
        to map 1 to ACE! - something to do in future.
        """
        turn_nums = [card[0] for card in turn]
        three_card_wrap_combis_on_turn = []

        # 12 8 3 2 or 12 9 5 4 or 12 11 6 2
        if turn_nums[0] - turn_nums[1] == 4:
            three_card_wrap_combis_on_turn.append([turn_nums[0]-1, turn_nums[0]-2, turn_nums[0]-3])
        if turn_nums[1] - turn_nums[2] == 4:
            three_card_wrap_combis_on_turn.append([turn_nums[1]-1, turn_nums[1]-2, turn_nums[1]-3])
        if turn_nums[2] - turn_nums[3] == 4:
            three_card_wrap_combis_on_turn.append([turn_nums[2]-1, turn_nums[2]-2, turn_nums[2]-3])

        # 10 7 5 2 - the third card must be 5 or lower or a made straight is on board
        if turn_nums[0] - turn_nums[1] == 3 and turn_nums[1] - turn_nums[2] > 1:
            if not turn_nums[0] == 14:
                three_card_wrap_combis_on_turn.append([turn_nums[0]+1, turn_nums[0]-1, turn_nums[0]-2])
                three_card_wrap_combis_on_turn.append([turn_nums[0]-1, turn_nums[0]-2, turn_nums[1]-1])
            else:
                # edge case, if first card on flop is 14, we can't wrap higher than it
                three_card_wrap_combis_on_turn.append([turn_nums[0]-1, turn_nums[0]-2, turn_nums[2]-1])
        # 13 8 5 2 - first card must be larger than 9 and fourth card mus be smaller tha 4, otherwise made straight is on board
        if turn_nums[1] - turn_nums[2] == 3 and turn_nums[0] - turn_nums[1] > 1 and turn_nums[2] - turn_nums[3] > 1:
            # no edge case possible, turn_nums[0] cannot be 14 or 13 and for the above condition to be met
            three_card_wrap_combis_on_turn.append([turn_nums[1]+1, turn_nums[1]-1, turn_nums[1]-2])
            three_card_wrap_combis_on_turn.append([turn_nums[1]-1, turn_nums[1]-2, turn_nums[2]-1])
        # 14 13 7 4
        if turn_nums[2] - turn_nums[3] == 3 and turn_nums[1] - turn_nums[2] > 1:
            three_card_wrap_combis_on_turn.append([turn_nums[2]+1, turn_nums[2]-1, turn_nums[2]-2])
            three_card_wrap_combis_on_turn.append([turn_nums[2]-1, turn_nums[2]-2, turn_nums[3]-1])

        # 14 13 4 2 or 14 9 8 2 or 14 9 3 2
        if turn_nums[0] - turn_nums[1] == 1 and turn_nums[1] - turn_nums[2] > 3:
            # difference between second and third card must be more than 3, or a made straight is on board
            if turn_nums[0] == 14:
                three_card_wrap_combis_on_turn.append([turn_nums[1]-1, turn_nums[1]-2, turn_nums[1]-3])
            elif turn_nums[0] == 13:
                three_card_wrap_combis_on_turn.append([turn_nums[0]+1, turn_nums[1]-1, turn_nums[1]-2])
                three_card_wrap_combis_on_turn.append([turn_nums[1]-1, turn_nums[1]-2, turn_nums[1]-3])
            else:
                three_card_wrap_combis_on_turn.append([turn_nums[0]+3, turn_nums[0]+2, turn_nums[0]+1])
                three_card_wrap_combis_on_turn.append([turn_nums[0]+2, turn_nums[0]+1, turn_nums[1]-1])
                three_card_wrap_combis_on_turn.append([turn_nums[0]+1, turn_nums[1]-1, turn_nums[1]-2])
                three_card_wrap_combis_on_turn.append([turn_nums[1]-1, turn_nums[1]-2, turn_nums[1]-3])
        if turn_nums[1] - turn_nums[2] == 1 and turn_nums[0] - turn_nums[1] > 3 and turn_nums[2] - turn_nums[3] > 3:
            # no edge case where turn_nums[1] == 14 or 13 is possible and for the above condition to hold
            three_card_wrap_combis_on_turn.append([turn_nums[1]+3, turn_nums[1]+2, turn_nums[1]+1])
            three_card_wrap_combis_on_turn.append([turn_nums[1]+2, turn_nums[1]+1, turn_nums[2]-1])
            three_card_wrap_combis_on_turn.append([turn_nums[1]+1, turn_nums[2]-1, turn_nums[2]-2])
            three_card_wrap_combis_on_turn.append([turn_nums[2]-1, turn_nums[2]-2, turn_nums[2]-3])
        if turn_nums[2] - turn_nums[3] == 1 and turn_nums[1] - turn_nums[2] > 3:
            three_card_wrap_combis_on_turn.append([turn_nums[2]+3, turn_nums[2]+2, turn_nums[2]+1])
            three_card_wrap_combis_on_turn.append([turn_nums[2]+2, turn_nums[2]+1, turn_nums[3]-1])
            three_card_wrap_combis_on_turn.append([turn_nums[2]+1, turn_nums[3]-1, turn_nums[3]-2])
            three_card_wrap_combis_on_turn.append([turn_nums[3]-1, turn_nums[3]-2, turn_nums[3]-3])

        if not three_card_wrap_combis_on_turn:
            return False, []

        return True, three_card_wrap_combis_on_turn

    def analyse_my_hand_against_turn(self, action_on_flop, extra_information):
        """
        flop_action will be 'BET' or 'CALL' - tells us what we did on the flop

        card_helper is a dict() that holds what we flopped as the key, and helper cards as the values.
        e.g. ... card_helper('flopped_straight_draw': (9,7), 'flopped_wrap': (10,9,7), 'flopped_set': 'flopped_top_set', 'SPR_low': True)

        All possible keys for card_helper:
        1. flopped_straight_draw
        2. flopped_wrap
        3. flopped_set
        4. SPR_low
        5. flopped_nut_flush_draw
        6. flopped_nut_flush
        ---------------------------------------------------------

        It's quite important to know on the turn in general the SPR of the person who bet and anyone who called.
        Because if it is small, then a fold should be a call many times.

        Assumption: I'll buy in for the max (60) and I'll make decisions based on this.

        SPR = 1 : 30 in pot (30 in my stack)
        SPR = 2 : 20 in pot (40 in my stack)
        SPR = 3 : 15 in pot (45 in my stack)
        SPR = 4 : 12 in pot (48 in my stack)
        SPR = 5 : 10 in pot (50 in my stack)
        SPR = 7 : 7.5 in pot (52.5 in my stack)
        SPR = 9 : 6 in pot (54 in my stack)
        SPR = 11 : 5 in pot (55 in my stack)
        SPR = 19 : 3 in pot (57 in my stack)
        """

        # For MVP just get it to run through, so look at bet amount if it is small call or check, otherwise fold.
        if self.guy_to_right_bet_size <= 3:
            return 'call'
        if self.guy_to_right_bet_size == 0:
            return 'check'
        return 'fold'
