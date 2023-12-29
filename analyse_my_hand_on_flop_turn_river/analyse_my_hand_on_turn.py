"""
What I will consider in this package:
1) Organise both turn cards by adding them to the flop
2) Consider what is possible on the turn (ot neccesarily I have it but what is possible) -
paired board, made flush, wrap draw, etc.
3) Using 2, look at what I have in my hand; fill in my_hand_rating dictionary
4) Decision to check, bet, fold, call, etc. based on:
- SPR (I don't consider SPR now, consider it later)
- Anyone ahead of me to act
- My hand rating on turn

Consider exploit later.
"""


from collections import Counter
from .analyse_my_hand_on_flop import AnalyseMyHandOnFlop

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

        # my hand ratings on turn dictionary
        self.hand_ratings_turn1 = dict()
        self.hand_ratings_turn2 = dict()

    def organise_turn(self):
        """
        self.flop looks like: [[13, 'S'], [10, 'C'], [9, 'S']]
        turn will look like: [[13, 'S'], [10, 'C'], [9, 'S'], [8, 'C']] ; after we sort it.
        """
        turn1_card, turn2_card = TT.detect_turn_nums_and_suit()
        # TO DO: add a breakpoint here when running integration test and check if self.flop is correct, prviously
        # it got messed up and it took the value of the turn and I couldn't figure out why.
        # Add both turn cards to the flops

        turn1 = self.flop1 + [turn1_card]
        turn2 = self.flop2 + [turn2_card]

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
        return False, False

    @staticmethod
    def flush_completed_on_turn(turn):
        """
        This function will return:
        1) if there is a flush completed on turn
        2) What the nut flush nums card is
        3) What the nut flush suit card is
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
        two_card_completing_straights = []
        turn_numbers = [card[0] for card in turn]
        num1 = turn_numbers[0]
        num2 = turn_numbers[1]
        num3 = turn_numbers[2]
        num4 = turn_numbers[3]
        for i in range(2):
            if i == 1:
                # checking if there is straight btw second, third and fourth card
                num1, num2, num3 = num2, num3, num4
            if (num1 - num2) + (num2 - num3) <= 4:
                # edge case - if 14 is ever part of straight, only one straight combi possible
                if num1 == 14:
                    two_card_completing_straights += [[num for num in reversed(range(10, 15)) if num not in turn_numbers]]
                # 10 7 6 or 10 9 6
                elif (num1 - num2) == 3 or (num2 - num3) == 3:
                    two_card_completing_straights += [[num for num in reversed(range(num3, num1)) if num not in turn_numbers]]
                # 10 8 6
                elif (num1 - num2) == 2 and (num2 - num3) == 2:
                    two_card_completing_straights += [[num1-1, num2-1]]
                # 10 9 7
                elif (num1 - num2) == 1 and (num2 - num3) == 2:
                    two_card_completing_straights += [[num1+1, num2-1], [num2-1, num3-1]]
                # 10 8 7
                elif (num1 - num2) == 2 and (num2 - num3) == 1:
                    two_card_completing_straights += [[num1+1, num1-1], [num1-1, num3-1]]
                # 10 9 8
                elif (num1 - num2) == 1 and (num2 - num3) == 1:
                    # edge case if highest card is 14 or 13
                    if num1 == 14:
                        two_card_completing_straights += [[num3-1, num3-2]]
                    elif num1 == 13:
                        two_card_completing_straights += [[num1+1, num3-1], [num3-1, num3-2]]
                    else:
                        two_card_completing_straights += [[num1+2, num1+1], [num1+1, num3-1], [num3-1, num3-2]]
        if two_card_completing_straights:
            return True, two_card_completing_straights
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


    #---------------------------------------------------------------------------------------
    """
    Above outlines everything that is possible on the turn. 
    Below, I will compare my hand to what is possible and rate how nutted my hand is on the turn.
    """

    def is_board_paired_on_turn(self):
        """
        This function will:
        1) see if board is paired on turn
        2) if so, if I have any of it and add it to the rating.

        As with all other ratings, I'll keep it as 7 and 5's.
        Where 7 is the coconuts, and 5 can vary but it is a hand with equity, BUT CAN BE DOMINATED.
        """
        turn1_nums = [card[0] for card in self.turn1]
        turn2_nums = [card[0] for card in self.turn2]

        did_board_pair_on_turns = [self.did_board_pair_on_turn1, self.did_board_pair_on_turn2]
        board_pair_top_card_turns = [self.board_pair_top_card_turn1, self.board_pair_top_card_turn2]
        turn_nums = [turn1_nums, turn2_nums]
        hand_ratings_turns = [self.hand_ratings_turn1, self.hand_ratings_turn2]
        for one_of_two_turns in range(2):
            # Analyse whether each turn is paired and if we have anything
            if did_board_pair_on_turns[one_of_two_turns]:
                if board_pair_top_card_turns[one_of_two_turns]:
                    # top card paired 10 10 7 5
                    if turn_nums[one_of_two_turns][1] in self.num_list and turn_nums[one_of_two_turns][2] in self.num_list:
                        hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # nut house, 10 7
                    elif turn_nums[one_of_two_turns][1] in self.num_list and turn_nums[one_of_two_turns][3] in self.num_list:
                        if turn_nums[one_of_two_turns][2] != turn_nums[one_of_two_turns][3]:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 5  # second nut house, 10 5
                        else:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # nut house, 10 7 (board is 10 10 7 7 in this case)
                else:
                    # middle card paired  10 7 7 5
                    if turn_nums[one_of_two_turns][1] == turn_nums[one_of_two_turns][2]:
                        if self.num_list.count(turn_nums[one_of_two_turns][0]) >= 2:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # overhouse, 10 10
                        elif self.num_list.count(turn_nums[one_of_two_turns][1]) == 2:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # quads, 7 7
                        elif turn_nums[one_of_two_turns][0] in self.num_list and turn_nums[one_of_two_turns][1] in self.num_list:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 6   # 'nutish' house as overhouse is available, 10 7
                        elif turn_nums[one_of_two_turns][1] in self.num_list and turn_nums[one_of_two_turns][2] in self.num_list:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 5  # lower house, 7 5
                    # bottom card paired  10 7 5 5
                    elif turn_nums[one_of_two_turns][2] == turn_nums[one_of_two_turns][3]:
                        if self.num_list.count(turn_nums[one_of_two_turns][2]) == 2:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # quads, 5 5
                        elif self.num_list.count(turn_nums[one_of_two_turns][0]) >= 2:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # overhouse, 10 10
                        elif self.num_list.count(turn_nums[one_of_two_turns][1]) >= 2:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 7  # overhouse, 7 7
                        elif turn_nums[one_of_two_turns][0] in self.num_list and turn_nums[one_of_two_turns][2] in self.num_list:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 6  # 'nutish' house as overhouse is available, 10 7
                        elif turn_nums[one_of_two_turns][1] in self.num_list and turn_nums[one_of_two_turns][2] in self.num_list:
                            hand_ratings_turns[one_of_two_turns]['board_paired'] = 5  # lower house, 7 5

    def is_flush_completed_on_turn(self):
        """
        This function will:
        1) see if either board has a completed flush
        2) if so, if I have any of it and add it to the rating.

        Nut flush will rate it a 7 of course, ever other flush will be rated 5.
        Might be worth making a list of higher flushes and rate them 6, but not sure as I only want to
        play nuts, esp with flush.
        """
        my_hand = [(card_num, card_suit) for card_num in self.num_list for card_suit in self.suit_list]
        if self.did_flush_completed_on_turn1:
            if [self.nut_flush_nums_turn1, self.suit_of_flush_turn1] in my_hand:
                self.hand_ratings_turn1['made_flush'] = 7
            elif self.suit_list.count(self.suit_of_flush_turn1) >= 2:
                self.hand_ratings_turn1['made_flush'] = 5
        if self.did_flush_completed_on_turn2:
            if [self.nut_flush_nums_turn2, self.suit_of_flush_turn2] in my_hand:
                self.hand_ratings_turn2['made_flush'] = 7
            elif self.suit_list.count(self.suit_of_flush_turn2) >= 2:
                self.hand_ratings_turn2['made_flush'] = 5

        # if board is paired, rate flush as None
        if self.did_board_pair_on_turn1:
            self.hand_ratings_turn1['made_flush'] = None
        if self.did_board_pair_on_turn2:
            self.hand_ratings_turn2['made_flush'] = None

    def is_straight_completed_on_turn(self):
        """
        This function will:
        1) see if either board has a completed straight
        2) if so, if I have any of it and add it to the rating.

        Just like with flush I think rate 7 to the nut straight and any other straight that
        I have will be rated as 5.
        Can consider making finer distinction about second nut straight later on, just like with flush above.
        """
        if self.did_straight_complete_on_turn1:
            if self.two_card_combi_completing_straight_on_turn1 and all(card in self.num_list for card in self.two_card_combi_completing_straight_on_turn1[0]):
                self.hand_ratings_turn1['made_straight'] = 7
            else:
                for two_card_combi in self.two_card_combi_completing_straight_on_turn1:
                    if all(card in self.num_list for card in two_card_combi):
                        self.hand_ratings_turn1['made_straight'] = 5

        if self.did_straight_complete_on_turn2:
            if self.two_card_combi_completing_straight_on_turn2 and all(card in self.num_list for card in self.two_card_combi_completing_straight_on_turn2[0]):
                self.hand_ratings_turn2['made_straight'] = 7
            else:
                for two_card_combi in self.two_card_combi_completing_straight_on_turn2:
                    if all(card in self.num_list for card in two_card_combi):
                        self.hand_ratings_turn2['made_straight'] = 5
        # check if board paired or flush completed , if so rate made straight as None
        if self.did_board_pair_on_turn1 or self.did_flush_completed_on_turn1:
            self.hand_ratings_turn1['made_straight'] = None
        if self.did_board_pair_on_turn2 or self.did_flush_completed_on_turn2:
            self.hand_ratings_turn2['made_straight'] = None

    def set_on_turn(self):
        """
        This function will return:
        1) if I have a set and what set it is (this will be used for combo draw function below)
        returns 'top_set' or 'middle_set' or 'bottom_set' or None.

        It will also fill in my hand rating dictionary with the strength of my set relative to the board,
        if I have a set of course.
        It will only consider cases where the board is not completed. For completed boards I will
        consider it in the combo function below.
        """
        which_set_in_my_hand_turn1 = None
        which_set_in_my_hand_turn2 = None
        turn1_nums = [card[0] for card in self.turn1]
        turn2_nums = [card[0] for card in self.turn2]
        # turn1
        if self.num_list.count(turn1_nums[0]) >= 2:
            which_set_in_my_hand_turn1 = 'top'
        elif self.num_list.count(turn1_nums[1]) >= 2:
            which_set_in_my_hand_turn1 = 'middle'
        elif self.num_list.count(turn1_nums[2]) >= 2 or self.num_list.count(turn1_nums[3]) >= 2:
            which_set_in_my_hand_turn1 = 'bottom'
        # turn 2
        if self.num_list.count(turn2_nums[0]) >= 2:
            which_set_in_my_hand_turn2 = 'top'
        elif self.num_list.count(turn2_nums[1]) >= 2:
            which_set_in_my_hand_turn2 = 'middle'
        elif self.num_list.count(turn2_nums[2]) >= 2 or self.num_list.count(turn1_nums[3]) >= 2:
            which_set_in_my_hand_turn2 = 'bottom'

        # check if there is made straight for flush
        if not self.did_flush_completed_on_turn1 and self.did_straight_complete_on_turn1:
            if which_set_in_my_hand_turn1 == 'top':
                self.hand_ratings_turn1['set_with_nothing_completed'] = 6
            elif which_set_in_my_hand_turn1 == 'middle':
                self.hand_ratings_turn1['set_with_nothing_completed'] = 6
            elif which_set_in_my_hand_turn1 == 'bottom':
                self.hand_ratings_turn1['set_with_nothing_completed'] = 5
        if not self.did_flush_completed_on_turn2 and self.did_straight_complete_on_turn2:
            if which_set_in_my_hand_turn2 == 'top':
                self.hand_ratings_turn2['set_with_nothing_completed'] = 6
            elif which_set_in_my_hand_turn2 == 'middle':
                self.hand_ratings_turn2['set_with_nothing_completed'] = 6
            elif which_set_in_my_hand_turn2 == 'bottom':
                self.hand_ratings_turn2['set_with_nothing_completed'] = 5

        return which_set_in_my_hand_turn1, which_set_in_my_hand_turn2

    def is_flush_draw_on_turn(self):
        """
        This function will return:
        1) If there is a flush draw on turn
        2) If I have any flush draw; if I have 'nut' or 'some' flush draw
        """
        flush_draw_on_turn1 = None
        flush_draw_on_turn2 = None
        my_hand = [(card_num, card_suit) for card_num in self.num_list for card_suit in self.suit_list]
        if self.is_flush_draw_on_turn1:
            flush_draw_suit = [fd_suit for fd_suit in self.list_of_nut_flush_draw_num_suit_on_turn1[1]]
            if any(flush_draw in my_hand for flush_draw in self.list_of_nut_flush_draw_num_suit_on_turn1):
                flush_draw_on_turn1 = 'nut'
            elif self.suit_list.count(flush_draw_suit[0]) >= 2:
                flush_draw_on_turn1 = 'some'
            elif len(flush_draw_suit) > 1 and not self.hand_ratings_turn1.get('flush_draw'):
                if self.suit_list.count(flush_draw_suit[1]) >= 2:
                    flush_draw_on_turn1 = 'some'
        if self.is_flush_draw_on_turn2:
            flush_draw_suit = [fd_suit for fd_suit in self.list_of_nut_flush_draw_num_suit_on_turn2[1]]
            if any(flush_draw in my_hand for flush_draw in self.list_of_nut_flush_draw_num_suit_on_turn2):
                flush_draw_on_turn2 = 'nut'
            elif self.suit_list.count(flush_draw_suit[0]) >= 2:
                flush_draw_on_turn2 = 'some'
            elif len(flush_draw_suit) > 1 and not self.hand_ratings_turn2.get('flush_draw'):
                if self.suit_list.count(flush_draw_suit[1]) >= 2:
                    flush_draw_on_turn2 = 'some'

        # check if board paired, if so rate flush draw as None
        flush_draw_on_turn1 = None if self.did_board_pair_on_turn1 else flush_draw_on_turn1
        flush_draw_on_turn2 = None if self.did_board_pair_on_turn2 else flush_draw_on_turn2
        return flush_draw_on_turn1, flush_draw_on_turn2

    def is_wrap_draw_on_turn(self):
        """
        This function will return:
        1) If there is a wrap draw on turn
        2) If I have any wrap draw, if I have 'nut' or 'some' wrap
        """
        wrap_on_turn1 = None
        wrap_on_turn2 = None
        if self.is_wrap_draw_on_turn1:
            if all(card in self.num_list for card in self.list_of_all_three_card_wrap_combi_turn1[0]):
                wrap_on_turn1 = 'nut'
            else:
                for two_card_combi in self.list_of_all_three_card_wrap_combi_turn1:
                    if all(card in self.num_list for card in two_card_combi):
                        wrap_on_turn1 = 'some'
        if self.is_wrap_draw_on_turn2:
            if all(card in self.num_list for card in self.list_of_all_three_card_wrap_combi_turn2[0]):
                wrap_on_turn2 = 'nut'
            else:
                for two_card_combi in self.list_of_all_three_card_wrap_combi_turn2:
                    if all(card in self.num_list for card in two_card_combi):
                        wrap_on_turn2 = 'some'
        # check if board paired or flush completed, if so rate wrap draw as None
        wrap_on_turn1 = None if (self.did_board_pair_on_turn1 or self.did_flush_completed_on_turn1) else wrap_on_turn1
        wrap_on_turn2 = None if (self.did_board_pair_on_turn2 or self.did_flush_completed_on_turn2) else wrap_on_turn2
        return wrap_on_turn1, wrap_on_turn2

    def combo_draw(self):
        """
        This function will consider the combination of hands with flush and wrap draws.

        By itself, highest I will rate any draw is 6, because it still can BRICK! - and with just one card to come,
        need to be conservative.
        Also, because I will always bet 7's so it's not right to rate draw a 7 as I generally don't want to bet with it.
        """
        wrap_draw_on_turn1, wrap_draw_on_turn2 = self.is_wrap_draw_on_turn()
        flush_draw_on_turn1, flush_draw_on_turn2 = self.is_flush_draw_on_turn()
        set_on_turn1, set_on_turn2 = self.set_on_turn()
        # Wrap + flush combi draw
        if wrap_draw_on_turn1 == 'nut' and flush_draw_on_turn1 == 'nut':
            self.hand_ratings_turn1['combo_draw'] = 6
        elif wrap_draw_on_turn1 and flush_draw_on_turn1:
            self.hand_ratings_turn1['combo_draw'] = 5
        # Set + flush combi draw
        elif set_on_turn1 == 'nut' and flush_draw_on_turn1 == 'nut':
            self.hand_ratings_turn1['combo_draw'] = 6
        elif set_on_turn1 and flush_draw_on_turn1:
            self.hand_ratings_turn1['combo_draw'] = 5

    def analyse_my_hand_against_turn(self, action_on_flop, extra_information):
        """
        action_on_flop will be 'BET' or 'CALL' - tells us what we did on the flop;
        importantly it tells us who the aggressor was on last street.

        It's quite important to know on the turn in general the SPR of the person who bet and anyone who called.
        Because if it is small, then a fold should be a call many times.

        (R)!!!
        If the board is not paired or there is no flush on turn, I will fill the dictionary value with 'None'.
        Importantly distinction is that if board id paired and I have nothing, I will rate it a 1.
        (not a 0, because this can be confused with None depending on how you use it)

        Another thing to consider is that if board is paired, there's no need to run through
        straight or flush or draws functions, as they will be void.
        With this in mind it makes sense to pass it in a certain order and if something like a paired
        board is detected, stop passing and can return there.
        Order to check things on turn:
        1) did board pair -       self.hand_ratings_turn1['board_paired']
        2) did flush complete -   self.hand_ratings_turn1['made_flush']
        3) did straight complete- self.hand_ratings_turn1['made_straight']
        4) Combo draws -          self.hand_ratings_turn1['combo_draw']

        (R)!!!!!!
        Note that if say turn1 is paired, then you should have automatic 1 for all other ratings in hand.
        Because on a paired board other stuff is futile, or even if you have hit something, it is not
        worth considering continuing on that basis.
        We need to add that logic to this function.

        Ratings and what they mean:
        7 : the absolute coconuts - e.g. quads
        6:  very close to the coconuts - e.g. house with overhouse available, or middle set.
        5:  strong but non-nut - e.g. top house but overhouse available
        """

        # Fill out my hand ratings based on what is on board and what I have
        self.is_board_paired_on_turn()
        # Need to waterfall this so that if anything above is filled, no need to fill the below, I think?
        # OR if anything above filled, anything below can be marked as 1 in terms of rating and no need to
        # run the function.
        self.is_flush_completed_on_turn()
        self.is_straight_completed_on_turn()
        self.combo_draw()

        # Add logic here to check both my hand ratings and then return 'bet', 'call', 'check' or 'fold'.
        hand_rating_on_turn1 = max(self.hand_ratings_turn1.values())
        hand_rating_on_turn2 = max(self.hand_ratings_turn1.values())

        # STRATEGY FOR MY PLAY:
        # For now I'll ignore SPR for check raising- can introduce it later, just bet when I have it and check when I don't
        # I'm confident doing this alone will print money.
        action_behind_me = self.check_bet_three_bet()  # 'check', 'bet', 'three_bet'
        if hand_rating_on_turn1 == 7 or hand_rating_on_turn2 == 7:
            return 'BET'
        if hand_rating_on_turn1 == 6 and hand_rating_on_turn2 == 6:
            if action_on_flop == 'BET':  # means I was aggressor on flop
                return 'BET'
            elif not self.guy_to_right_bet_size:
                return 'BET'
            else:
                return 'CALL'
        if hand_rating_on_turn1 == 5 and hand_rating_on_turn2 == 6 \
            or hand_rating_on_turn1 == 6 and hand_rating_on_turn2 == 5:
            if action_behind_me == 'bet' and not self.positions_of_players_to_act_ahead_of_me:
                return 'CALL'

        if action_behind_me == 'check':
            return 'CALL'
        else:
            return 'FOLD'

        # For testing the flow of code vs. real app, comment out all of the above, and comment in all of below:
        # if self.guy_to_right_bet_size <= 3:
        #     return 'call'
        # if self.guy_to_right_bet_size == 0:
        #     return 'check'
        # return 'fold'
