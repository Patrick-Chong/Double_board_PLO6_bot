from flop_turn_river_cards import TheFlop

TF = TheFlop()


class FlopHelper:
    # Note this class can and should be used on the turn and river too!
    def __init__(self, my_position, num_list, suit_list):

        self.num_list = num_list
        self.suit_list = suit_list
        self.my_position = my_position

        self.flop1, self.flop2 = self.organise_flop()
        # self.flop1 = [[14, 'S'], [6, 'S'], [5, 'C']]


        # ANYTHING COMPLETED ON FLOP (board_pair, flush, or straight?)
        # Is the board paired on either flops
        self.is_any_board_paired_on_flop_generator = self.is_any_board_paired_on_flop(self.flop1)
        self.is_board2_paired_on_flop1 = self.is_any_board_paired_on_flop_generator[0]
        self.high_or_low_paired_board_flop1 = self.is_any_board_paired_on_flop_generator[1]
        self.is_any_board_paired_on_flop_generator = self.is_any_board_paired_on_flop(self.flop2)
        self.is_board_paired_on_flop2 = self.is_any_board_paired_on_flop_generator[0]
        self.high_or_low_paired_board_flop2 = self.is_any_board_paired_on_flop_generator[1]
        # Is there a made flush on either flops
        self.made_flush_on_flop_generator = self.made_flush_on_flop(self.flop1)
        self.is_flush_completed_on_flop1 = self.made_flush_on_flop_generator[0]
        self.nut_flush_nums_flop1 = self.made_flush_on_flop_generator[1]
        self.nut_flush_suit_flop1 = self.made_flush_on_flop_generator[2]
        self.made_flush_on_flop_generator = self.made_flush_on_flop(self.flop2)
        self.is_flush_completed_on_flop2 = self.made_flush_on_flop_generator[0]
        self.nut_flush_nums_flop2 = self.made_flush_on_flop_generator[1]
        self.nut_flush_suit_flop2 = self.made_flush_on_flop_generator[2]
        # Is there a made straight on either flops
        self.made_straight_on_flop_generator = self.made_straight_on_flop(self.flop1)
        self.is_straight_completed_on_flop1 = self.made_straight_on_flop_generator[0]
        self.two_card_combis_that_complete_the_straight_on_flop1 = self.made_straight_on_flop_generator[1]
        self.open_or_closed_straight_flop1 = self.made_straight_on_flop_generator[2]  # open: 2,5,6  ; closed: 2 3 6
        self.made_straight_on_flop_generator = self.made_straight_on_flop(self.flop2)
        self.is_straight_completed_on_flop2 = self.made_straight_on_flop_generator[0]
        self.two_card_combis_that_complete_the_straight_on_flop2 = self.made_straight_on_flop_generator[1]
        self.open_or_closed_straight_flop2 = self.made_straight_on_flop_generator[2]  # open: 2,5,6  ; closed: 2 3 6


        # DRAWS ON FLOP (flush, wrap, straight?)
        # Is there a flush draw on flop
        self.flush_draw_on_flop_generator = self.flush_draw_on_flop(self.flop1)
        self.is_flush_draw_on_flop1 = self.flush_draw_on_flop_generator[0]
        self.nut_flush_draw_nums_on_flop1 = self.flush_draw_on_flop_generator[1]
        self.nut_flush_draw_suit_on_flop1 = self.flush_draw_on_flop_generator[2]
        self.flush_draw_on_flop_generator = self.flush_draw_on_flop(self.flop2)
        self.is_flush_draw_on_flop2 = self.flush_draw_on_flop_generator[0]
        self.nut_flush_draw_nums_on_flop2 = self.flush_draw_on_flop_generator[1]
        self.nut_flush_draw_suit_on_flop2 = self.flush_draw_on_flop_generator[2]
        # Is there a wrap draw on either flops
        self.wrap_draw_on_flop_generator = self.wrap_draw_on_flop(self.flop1)
        self.is_wrap_draw_on_flop1 = self.wrap_draw_on_flop_generator[0]
        self.is_wrap_closed_on_flop1 = self.wrap_draw_on_flop_generator[1]
        self.three_card_wrap_combis_on_flop1 = self.wrap_draw_on_flop_generator[2]
        self.wrap_draw_on_flop_generator = self.wrap_draw_on_flop(self.flop2)
        self.is_wrap_draw_on_flop2 = self.wrap_draw_on_flop_generator[0]
        self.is_wrap_closed_on_flop2 = self.wrap_draw_on_flop_generator[1]
        self.three_card_wrap_combis_on_flop2 = self.wrap_draw_on_flop_generator[2]
        # Is there a straight draw on either flops
        self.straight_draw_on_flop_generator = self.straight_draw_on_flop(self.flop1)
        self.is_straight_draw_on_flop1 = self.straight_draw_on_flop_generator[0]
        self.two_card_straight_draw_combis_on_flop1 = self.straight_draw_on_flop_generator[1]
        self.straight_draw_on_flop_generator = self.straight_draw_on_flop(self.flop2)
        self.is_straight_draw_on_flop2 = self.straight_draw_on_flop_generator[0]
        self.two_card_straight_draw_combis_on_flop2 = self.straight_draw_on_flop_generator[1]

    def organise_flop(self):
        """
        Note that when I sort the num of suit, the way I wrote it, the corresponding suits get moved together,
        which is extremely important!

        flop_nums = [[13, 2, 6], [14, 12, 8]]
        flop_suits = [['H', 'H', 'C'], ['D', 'D', 'C']]

        we are returning:
        flop1 = [[13, 'H'], [6, 'C'], [2, 'H']]
        flop2 = [[14, 'D'], [12, 'D'], [8, 'C']]
        """

        final_flop1 = list()
        final_flop2 = list()

        flop1, flop2 = TF.detect_flop_nums_and_suit()
        flop1_num, flop1_suit = flop1[0], flop1[1]
        final_flop1.append([flop1_num[0], flop1_suit[0]])
        final_flop1.append([flop1_num[1], flop1_suit[1]])
        final_flop1.append([flop1_num[2], flop1_suit[2]])

        flop2_num, flop2_suit = flop2[0], flop2[1]
        final_flop2.append([flop2_num[0], flop2_suit[0]])
        final_flop2.append([flop2_num[1], flop2_suit[1]])
        final_flop2.append([flop2_num[2], flop2_suit[2]])

        flop1 = sorted(final_flop1, key=lambda x: x[0], reverse=True)  # Sorting from largest to smallest, hence reverse=True
        flop2 = sorted(final_flop2, key=lambda x: x[0], reverse=True)  # Sorting from largest to smallest, hence reverse=True

        return flop1, flop2

    def is_any_board_paired_on_flop(self, flop):
        """
        This function will return:
         1) if the given flop is paired,
         2) if it is an 'lowpaired' or 'highpaied'.  lowpaired 10 3 3 board, and highpaied 10 10 3 board
        """
        # self.flop1 = [[14, 'S'], [6, 'S'], [5, 'C']]
        flop_nums = [card[0] for card in flop]
        is_flop_paired = True if len(set(flop_nums)) < 3 else False
        if is_flop_paired:
            high_or_low_paired_board = 'high' if flop_nums[0] == flop_nums[1] else 'low'
        else:
            high_or_low_paired_board = None

        return is_flop_paired, high_or_low_paired_board

    def made_flush_on_flop(self, flop):
        """
        This function will return:
        1) if there is a flush on board - doesn't mean I have the flush.
        2) the nut flush nums
        3) the nut flush suit

        (R)!!! - note that the nut flush nums is NOT the highest num on the board that has that suit.
        It is the highest number that is NOT on the flop.
        For example, [14, 13, 12] and they are all 'hearts' or whatever suit, then the nut flush nums is 11.
        """
        flop_suit = [card[1] for card in flop]
        if flop_suit[0] == flop_suit[1] and flop_suit[1] == flop_suit[2]:
            # if the first card is not an ace, then ace high flush is the highest flush
            if not flop[0][0] == 14:
                return True, 14, flop_suit[0]
            elif not flop[1][0] == 13:
                return True, 13, flop_suit[0]
            elif not flop[2][0] == 12:
                return True, 12, flop_suit[0]
            else:
                return True, 11, flop_suit[0]
        else:
            return False, 'no_flush_on_flop', 'no_flush_on_flop'

    def made_straight_on_flop(self, flop):
        """
        This function returns 3 things:

        1) This function will determine if there is a straight on board - doesn't mean I have the straight.
        e.g. if the flops is 3,4,5 or 3,4,6 or 3,4,7 then this returns True.
        if flop is 2,4,8 then it returns False.

        2) It will also return all the two_card_combinations that complete the straight; not just the nut
        straight but any straight.
        It will store these two card straight making combis in order of nuttiness starting with the nut straight.

        3) It will also return 'O' or 'C' to indicate if the straight is Open or Closed;
        closed would be: 3,4,7 or 3,4,5, 3,5,7. And the open would be 3,6,7.
        - in coding terms as long both the straight completing cards are not lower than two of the three flop cards,
        then we have a closed straight, otherwise it is open.

        A closed straight will change much less often, whereas an open straight will change often, as there is
        a wrap potential going up, so you won't want to go too crazy unless you are nutted on other baord.
        """
        flop_nums = [card[0] for card in flop]  # flop looks like [[10, 'S'], [6, 'C'], [2, 'S']]
        all_two_card_straight_completing_combi_on_flop = []
        open_or_closed_straight = None

        # check if straight completed on flop
        total_distance_of_flop_cards = 0
        total_distance_of_flop_cards += flop_nums[0] - flop_nums[1]
        total_distance_of_flop_cards += flop_nums[1] - flop_nums[2]
        if not 4 >= total_distance_of_flop_cards > 1:
            return False, None, None  # there is no made straight on the flop

        # There is a made straight on flop, find the two card combinations that complete it, and determine if it's open or closed
        # case 1) one gap between each card, e.g. 9 7 5
        if flop_nums[0] - flop_nums[1] == 2 and flop_nums[1] - flop_nums[2] == 2:
            all_two_card_straight_completing_combi_on_flop.append([flop_nums[1]+1, flop_nums[2]+1])
            open_or_closed_straight = 'C'
        if flop_nums[0] == 14:  # edge case
            two_completing_straight_cards = []
            for i in reversed(range(10, 15)):
                if i not in flop_nums:
                    two_completing_straight_cards.append(i)
            if not all_two_card_straight_completing_combi_on_flop:
                all_two_card_straight_completing_combi_on_flop.append(two_completing_straight_cards)
                open_or_closed_straight = 'C'
        else:
            # case 2) no gaps between each card, e.g. 9 8 7
            if total_distance_of_flop_cards == 2:
                if flop_nums[0] == 13:  # edge case
                    all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]+1, flop_nums[2]-1])  # 14 10
                    all_two_card_straight_completing_combi_on_flop.append([flop_nums[2]-1, flop_nums[2]-2])  # 10 9
                    open_or_closed_straight = 'C'
                else:
                    all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]+2, flop_nums[0]+1])  # 11 10
                    all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]+1, flop_nums[2]-1])  # 10 6
                    all_two_card_straight_completing_combi_on_flop.append([flop_nums[2]-1, flop_nums[2]-2])  # 6 5
                    open_or_closed_straight = 'C'
            # case 3) two gaps closed, e.g. 10 7 6
            if flop_nums[0] - flop_nums[1] == 3 and flop_nums[1] - flop_nums[2] == 1:
                all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]-1, flop_nums[0]-2])  # 9 8
                open_or_closed_straight = 'C'
            # case 4) two gaps open, e.g. 10 9 6
            elif flop_nums[0] - flop_nums[1] == 1 and flop_nums[1] - flop_nums[2] == 3:
                all_two_card_straight_completing_combi_on_flop.append([flop_nums[1]-1, flop_nums[1]-2])  # 8 7
                open_or_closed_straight = 'O'
            # case 5) one total gap lower, e.g. 10 9 7
            elif flop_nums[0] - flop_nums[1] == 1 and flop_nums[1] - flop_nums[2] == 2:
                all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]+1, flop_nums[1]-1])  # 11 8
                all_two_card_straight_completing_combi_on_flop.append([flop_nums[1]-1, flop_nums[2]-1])  # 8 6
                open_or_closed_straight = 'C'
            # case 6) one total gap upper, e.g. 10 8 7
            elif flop_nums[0] - flop_nums[1] == 2 and flop_nums[1] - flop_nums[2] == 1:
                all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]+1, flop_nums[0]-1])  # 11 9
                all_two_card_straight_completing_combi_on_flop.append([flop_nums[0]-1, flop_nums[2]-1])  # 9 6
                open_or_closed_straight = 'C'

        return True, all_two_card_straight_completing_combi_on_flop, open_or_closed_straight

    # DRAWS
    def flush_draw_on_flop(self, flop):
        """
        This function will return:
        1) if there is a flush draw on the flop
        2) the highest num of the flush draw
        3) suit of the flush.

        At this point we should have checked that flush has not completed on flop, so we can ignore that
        while considering different cases of flush draws and the highest flush nums card.

         # self.flop1 = [[14, 'S'], [6, 'S'], [5, 'C']]
        """
        if not any([flop[0][1] == flop[1][1], flop[1][1] == flop[2][1], flop[0][1] == flop[2][1]]):
            # No flush draw on flop
            return False, None, None

        if flop[0][1] == flop[1][1]:  # compare first and second card suits
            two_flush_draw_making_cards_nums = (flop[0][0], flop[1][0])
            if 14 not in two_flush_draw_making_cards_nums:
                return True, 14, flop[0][1]
            elif 13 not in two_flush_draw_making_cards_nums:
                return True, 13, flop[0][1]
            else:
                return True, 12, flop[0][1]

        if flop[1][1] == flop[2][1]:  # compare first and second card suits
            two_flush_draw_making_cards_nums = (flop[1][0], flop[2][0])
            if 14 not in two_flush_draw_making_cards_nums:
                return True, 14, flop[1][1]
            elif 13 not in two_flush_draw_making_cards_nums:
                return True, 13, flop[1][1]
            else:
                return True, 12, flop[1][1]

        if flop[0][1] == flop[2][1]:  # compare first and third card suits
            two_flush_draw_making_cards_nums = (flop[0][0], flop[2][0])
            if 14 not in two_flush_draw_making_cards_nums:
                return True, 14, flop[0][1]
            elif 13 not in two_flush_draw_making_cards_nums:
                return True, 13, flop[0][1]
            elif 12 not in two_flush_draw_making_cards_nums:
                return True, 12, flop[0][1]
            else:
                return True, 11, flop[0][1]

        return False, None, None  # these need to be None for how_big_is_my_flush_draw to work

    def wrap_draw_on_flop(self, flop):
        """
        I will consider all wraps, even if there are two, I'll consider both.
        Like always, the wraps will go down in nuttiness if there are more than one available.

        This function will return
        1) True if I have a wrap in my hand.
        2) if the wrap is closed
        3) all three_card_wrap_combis_on_flop.
        For example, flop_nums= 12 6 5 then this returns [9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2].
        Like other things, it will be more nutted first and go down in nuttiness, if there are more than one wraps
        available on the board.

        There is only a wrap draw if there is a two gapper between two of the cards, and no gaps between the
        other two, e.g. 10 9 6. Otherwise, no wrap is possible.
        Or if there is a three gapper between two cards and no gap between other cards.
        I'll call the latter closed wrap, it is easier to deal with.
        """
        flop_nums = [card[0] for card in flop]
        closed_wrap = True
        three_card_wrap_combis_on_flop = []

        # HARD TO WRITE CONDITION TO CHECK IF THERE IS A WRAP; SO JUST WRITE OUT ALL SCENARIOS
        # JUST UNIT TEST IT THOROUGHLY

        # 14 13 9
        if flop_nums[0] - flop_nums[1] == 4:
            three_card_wrap_combis_on_flop.append([flop_nums[0]-1, flop_nums[0]-2, flop_nums[0]-3])
        if flop_nums[1] - flop_nums[2] == 4:
            three_card_wrap_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2, flop_nums[1]-3])

        if flop_nums[0] - flop_nums[1] == 3 and flop_nums[1] - flop_nums[2] == 1:  # 10 7 6
            if not flop_nums[0] == 14:
                three_card_wrap_combis_on_flop.append([flop_nums[0]+1, flop_nums[0]-1, flop_nums[0]-2])
                three_card_wrap_combis_on_flop.append([flop_nums[0]-1, flop_nums[0]-2, flop_nums[2]-1])
            else:
                # edge case, if first card on flop is 14, we can't wrap higher than it
                three_card_wrap_combis_on_flop.append([flop_nums[0]-1, flop_nums[0]-2, flop_nums[2]-1])

        elif flop_nums[0] - flop_nums[1] == 1 and flop_nums[1] - flop_nums[2] == 3:  # 10 9 6
            if not flop_nums[0] == 14:
                three_card_wrap_combis_on_flop.append([flop_nums[0]+3, flop_nums[0]+2, flop_nums[0]+1])
                three_card_wrap_combis_on_flop.append([flop_nums[0]+2, flop_nums[0]+1, flop_nums[1]+1])
                three_card_wrap_combis_on_flop.append([flop_nums[0]+1, flop_nums[1]-1, flop_nums[1]-2])
                three_card_wrap_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2, flop_nums[2]-1])
            else:
                three_card_wrap_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2, flop_nums[2]-1])
            closed_wrap = False

        if not three_card_wrap_combis_on_flop:
            return False, None, []

        return True, closed_wrap, three_card_wrap_combis_on_flop

    def straight_draw_on_flop(self, flop):
        """
        Just like wrap draw above this, I will consider all straights.

        This function will return:
        1) if there is a straight draw on the flop
        2) a list of all the straight draw cards, there could be a few, e.g. on flop 10 8 5; [[J,9], [9,7], [7,6]] would be returned

        The only possible way for there to be a straight draw is if the gap between two cards are 1, 2 or 3.
        i.e. 10 9   or  10 8  or  10 7
        [[12,11],[11,8],[8,7]]    [[J,9], [9,7]]    [[9,8]]

        As usual, the combinations will go down in nuttiness as we go down the list.
        At this point I'll assume that we have done a check that a MADE STRAIGHT is NOT on board already.

        TO DO: add inside straight draws, e.g. on 10 8, if you have 12,11 that is a straight draw as well;
        a bit much for now so I'll leave it out.
        """
        flop_nums = [card[0] for card in flop]
        two_card_straight_draw_combis_on_flop = []

        # First check that there is a straight possibility between the flop cards
        distance_btw_cards_for_straight_to_be_possible = (1, 2, 3)
        distance_first_two_cards = flop_nums[0] - flop_nums[1]
        distance_second_and_third_card = flop_nums[1] - flop_nums[2]

        if not distance_first_two_cards in distance_btw_cards_for_straight_to_be_possible and \
            not distance_second_and_third_card in distance_btw_cards_for_straight_to_be_possible:
            return False, []

        # If straight possible, retrieve all the two straight draw making combinations.
        # Get all combinations with first two flop cards
        if distance_first_two_cards == 3:  # 10 7
            two_card_straight_draw_combis_on_flop.append([flop_nums[0]-1, flop_nums[0]-2])
        elif distance_first_two_cards == 2:  # 10 8
            if flop_nums[0] != 14:
                two_card_straight_draw_combis_on_flop.append([flop_nums[0]+1, flop_nums[0]-1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]+1, flop_nums[1]-1])
            else:
                # edge case, can't have higher straight draw card higher than 14
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]+1, flop_nums[1]-1])
        elif distance_first_two_cards == 1:  # 10 9
            if flop_nums[0] < 13:
                two_card_straight_draw_combis_on_flop.append([flop_nums[0]+2, flop_nums[0]+1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[0]+1, flop_nums[1]-1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2])
            elif flop_nums[0] == 13:
                two_card_straight_draw_combis_on_flop.append([flop_nums[0]+1, flop_nums[1]-1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2])
            elif flop_nums[0] == 14:
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2])

        # Get all combinations with second two flop cards (N.B. if second card is 14 first card must be 14)
        if distance_second_and_third_card == 3:  # 10 7
            two_card_straight_draw_combis_on_flop.append([flop_nums[1]-1, flop_nums[1]-2])
        elif distance_second_and_third_card == 2:  # 10 8
            if flop_nums[1] != 14:
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]+1, flop_nums[1]-1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[2]+1, flop_nums[2]-1])
            else:
                two_card_straight_draw_combis_on_flop.append([flop_nums[2]+1, flop_nums[2]-1])
        elif distance_second_and_third_card == 1:  # 10 9
            if flop_nums[1] < 13:
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]+2, flop_nums[1]+1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]+1, flop_nums[2]-1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[2]-1, flop_nums[2]-2])
            elif flop_nums[1] == 13:
                two_card_straight_draw_combis_on_flop.append([flop_nums[1]+1, flop_nums[2]-1])
                two_card_straight_draw_combis_on_flop.append([flop_nums[2]-1, flop_nums[2]-2])

        if not two_card_straight_draw_combis_on_flop:
            print('something went wrong with generating two straight card combis, two_card_straight_draw_combis_on_flop '
                  'should not be empty')

        return True, two_card_straight_draw_combis_on_flop


class AnalyseMyHandOnFlop(FlopHelper):

    def __init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                 positions_of_players_to_act_ahead_of_me,
                 pot_size, my_position, num_list, suit_list, big_blind):
        # As a learning point, the order of the below matters; if you initialize self.special_hand1 before self.flop, you will get an error
        # since self.special_hand1 uses self.flop in it's function - makes perfect sense.
        FlopHelper.__init__(self, my_position, num_list, suit_list)

        self.guy_to_right_bet_size = guy_to_right_bet_size
        self.positions_of_players_to_act_ahead_of_me = positions_of_players_to_act_ahead_of_me

        self.stack_tracker = stack_tracker
        self.pot_size = pot_size
        self.SPR_tracker = SPR_tracker
        self.flop1_nums = [card[0] for card in self.flop1]
        self.flop2_nums = [card[0] for card in self.flop2]

        # Helpers; checks if I have: (nut flush draw, set, check_raise
        self.flopped_nut_flush_draw_generator = self.helper_flopped_nut_flush_draw()
        self.flopped_nut_flush_draw_flop1 = self.flopped_nut_flush_draw_generator[0]
        self.flopped_nut_flush_draw_flop2 = self.flopped_nut_flush_draw_generator[1]

        self.flopped_set_generator = self.helper_set_checker()
        self.flopped_set_flop1 = self.flopped_set_generator[0]
        self.flopped_set_flop2 = self.flopped_set_generator[1]

        self.check_raise_f = self.helper_check_raise()

        # WHAT DO I HAVE
        # Rated 6
        # 1) over-house  2) nut flush  3) quads
        self.overhouse_check_on_flop_generator = self.over_house_check()
        self.overhouse_on_flop1 = self.overhouse_check_on_flop_generator[0]
        self.overhouse_on_flop2 = self.overhouse_check_on_flop_generator[1]

        self.nut_flush_check_on_flop_generator = self.nut_flush_check()
        self.nut_flush_on_flop1 = self.nut_flush_check_on_flop_generator[0]
        self.nut_flush_on_flop2 = self.nut_flush_check_on_flop_generator[1]

        self.quads_check_generator = self.quads_checker()
        self.flopped_quads_flop1 = self.quads_check_generator[0]
        self.flopped_quads_flop2 = self.quads_check_generator[1]

        # Rated 5
        # 1) top set no made straight/flush  2) nut flush draw top wrap
        # 3) Flopped nut straight with flush/house redraw   4) nut full house
        self.top_set_no_made_flush_straight_generator = self.top_set_no_made_flush_straight_checker()
        self.flopped_top_set_no_made_flush_straight_flop1 = self.top_set_no_made_flush_straight_generator[0]
        self.flopped_top_set_no_made_flush_straight_flop2 = self.top_set_no_made_flush_straight_generator[1]

        self.nut_flush_draw_nut_wrap_generator = self.nut_flush_draw_nut_wrap()
        self.flopped_nut_flush_draw_nut_wrap_flop1 = self.nut_flush_draw_nut_wrap_generator[0]
        self.flopped_nut_flush_draw_nut_wrap_flop2 = self.nut_flush_draw_nut_wrap_generator[1]

        self.flopped_nut_straight_with_house_or_flush_redraw_generator = self.flopped_nut_straight_with_house_or_flush_redraw()
        self.flopped_nut_straight_with_house_or_flush_redraw_flop1 = self.flopped_nut_straight_with_house_or_flush_redraw_generator[0]
        self.flopped_nut_straight_with_house_or_flush_redraw_flop2 = self.flopped_nut_straight_with_house_or_flush_redraw_generator[1]

        self.nut_house_on_flop_generator = self.check_nut_house_on_flop()
        self.nut_house_on_flop1 = self.nut_house_on_flop_generator[0]
        self.nut_house_on_flop2 = self.nut_house_on_flop_generator[1]

        # Rated 4
        # 1) top set on made straight/flush  2) nut wrap with non nut flush draw  / or nut flush draw non nut wrap
        # 3) underhouse  4) any set 5) house with over house available   6) wrap on rainbow board
        self.top_set_on_made_flush_straight_board_generator = self.top_set_on_made_flush_straight_board()
        self.top_set_on_made_flush_straight_board_flop1 = self.top_set_on_made_flush_straight_board_generator[0]
        self.top_set_on_made_flush_straight_board_flop2 = self.top_set_on_made_flush_straight_board_generator[1]

        self.nut_wrap_non_nut_flush_draw_generator = self.nut_wrap_non_nut_flush_draw()
        self.nut_wrap_non_nut_flush_draw_flop1 = self.nut_wrap_non_nut_flush_draw_generator[0]
        self.nut_wrap_non_nut_flush_draw_flop2 = self.nut_wrap_non_nut_flush_draw_generator[1]

        self.non_nut_wrap_nut_flush_draw_generator = self.non_nut_wrap_nut_flush_draw()
        self.non_nut_wrap_nut_flush_draw_flop1 = self.non_nut_wrap_nut_flush_draw_generator[0]
        self.non_nut_wrap_nut_flush_draw_flop2 = self.non_nut_wrap_nut_flush_draw_generator[1]

        self.flopped_underhouse_generator = self.flopped_under_house()
        self.flopped_underhouse_flop1 = self.flopped_underhouse_generator[0]
        self.flopped_underhouse_flop2 = self.flopped_underhouse_generator[1]

        self.flopped_any_set_flop1 = self.flopped_set_flop1
        self.flopped_any_set_flop2 = self.flopped_set_flop2

        self.flopped_house_with_overhouse_avail_generator = self.flopped_house_with_overhouse_avail()
        self.flopped_house_with_overhouse_avail_flop1 = self.flopped_house_with_overhouse_avail_generator[0]
        self.flopped_house_with_overhouse_avail_flop2 = self.flopped_house_with_overhouse_avail_generator[1]

        self.any_wrap_on_rainbow_board_generator = self.any_wrap_on_rainbow_board()
        self.any_wrap_on_rainbow_board_flop1 = self.any_wrap_on_rainbow_board_generator[0]
        self.any_wrap_on_rainbow_board_flop2 = self.any_wrap_on_rainbow_board_generator[1]

        self.summary_of_hand_ratings_and_my_hand_on_flop1_generator = self.summary_of_hand_ratings_and_my_hand_on_flops()
        self.summary_of_hand_ratings_and_my_hand_on_flop1 = self.summary_of_hand_ratings_and_my_hand_on_flop1_generator[0]
        self.summary_of_hand_ratings_and_my_hand_on_flop2 = self.summary_of_hand_ratings_and_my_hand_on_flop1_generator[1]

    def analyse_my_hand_against_flop(self, action=None):
        """
        This function will consider my hand ratings on flop1 and flop2, and return the action corresponding
        to the strength of my hand.
        It will take into consideration the SPR, when deciding whether to bet or not.

        The initial aim will be to only play nutted hands, where my equity is high.
        So from an action perspective, I will want to get the money in as efficiently as possible.

        Strategy summary:
          --------------------------------
         |  flop1    flop2      action
         |    6       any   ->   bet
         |   any       6    ->   bet
         |
         |    5        5    ->   bet
         |    5        4    ->   bet
         |    4        5    ->   bet
         |    4        4    ->   check

        """
        # TO DO: add SPR consideration to the below; there is a check_raise flag that you can use.

        if any(self.summary_of_hand_ratings_and_my_hand_on_flop1[6]) or any(self.summary_of_hand_ratings_and_my_hand_on_flop2[6]):
            action = 'bet'
        elif any(self.summary_of_hand_ratings_and_my_hand_on_flop1[5]) and any(self.summary_of_hand_ratings_and_my_hand_on_flop2[5]):
            action = 'bet'
        elif any(self.summary_of_hand_ratings_and_my_hand_on_flop1[5]) and any(self.summary_of_hand_ratings_and_my_hand_on_flop2[4]):
            action = 'bet'
        elif any(self.summary_of_hand_ratings_and_my_hand_on_flop1[4]) and any(self.summary_of_hand_ratings_and_my_hand_on_flop2[5]):
            action = 'bet'
        elif any(self.summary_of_hand_ratings_and_my_hand_on_flop1[4]) and any(self.summary_of_hand_ratings_and_my_hand_on_flop2[4]):
            action = 'check'

        return action

    def summary_of_hand_ratings_and_my_hand_on_flops(self):
        """
        This function will hold a dictionary of hand rating to hands that are in that rating.
        hand_ratings_flop1 = dict(6:[('self.overhouse_on_flop1', self.overhouse_on_flop1), ('self.nut_flush_on_flop1', nut_flush_on_flop1),
                                     ('self.flopped_quads_flop1', self.flopped_quads_flop1)],
                                  5:[....]
                                  4:[....]}
        hand_ratings_flop2 = dict(6:[('self.overhouse_on_flop2', self.overhouse_on_flop2), ('self.nut_flush_on_flop2', nut_flush_on_flop2),
                                     ('self.flopped_quads_flop1', self.flopped_quads_flop1)],
                                  5:[...]
                                  4:[...]}

        Note that the dictionary consists of the rating as the key, and the values of each rating is a dictionary of tuples,
        where the first item in the tuple is a string representation of the hand in that rating and the second item
        will be True or False to indicate whether we have that in our hand.
        """
        hand_ratings_flop1 = dict()
        hand_ratings_flop2 = dict()
        hand_ratings_flop1[6] = [('self.overhouse_on_flop1', self.overhouse_on_flop1),
                                 ('self.nut_flush_on_flop1', self.nut_flush_on_flop1),
                                 ('self.flopped_quads_flop1', self.flopped_quads_flop1)
                                 ]
        hand_ratings_flop1[5] = [('self.flopped_top_set_no_made_flush_straight_flop1', self.flopped_top_set_no_made_flush_straight_flop1),
                                 ('self.flopped_nut_flush_draw_nut_wrap_flop1', self.flopped_nut_flush_draw_nut_wrap_flop1),
                                 ('self.flopped_nut_straight_with_house_or_flush_redraw_flop1', self.flopped_nut_straight_with_house_or_flush_redraw_flop1),
                                 ('self.nut_house_on_flop1', self.nut_house_on_flop1)
                                 ]
        hand_ratings_flop1[4] = [('self.top_set_on_made_flush_straight_board_flop1', self.top_set_on_made_flush_straight_board_flop1),
                                 ('self.nut_wrap_non_nut_flush_draw_flop1', self.nut_wrap_non_nut_flush_draw_flop1),
                                 ('self.non_nut_wrap_nut_flush_draw_flop1', self.non_nut_wrap_nut_flush_draw_flop1),
                                 ('self.flopped_underhouse_flop1', self.flopped_underhouse_flop1),
                                 ('self.flopped_any_set_flop1', self.flopped_any_set_flop1),
                                 ('self.flopped_house_with_overhouse_avail_flop1', self.flopped_house_with_overhouse_avail_flop1),
                                 ('self.any_wrap_on_rainbow_board_flop1', self.any_wrap_on_rainbow_board_flop1),
                                 ('self.summary_of_hand_ratings_and__my_hand_on_flop1', self.summary_of_hand_ratings_and_my_hand_on_flop1)
                                 ]
        hand_ratings_flop2[6] = [('self.overhouse_on_flop2', self.overhouse_on_flop2),
                                 ('self.nut_flush_on_flop2', self.nut_flush_on_flop2),
                                 ('self.flopped_quads_flop2', self.flopped_quads_flop2)
                                 ]
        hand_ratings_flop2[5] = [('self.flopped_top_set_no_made_flush_straight_flop2', self.flopped_top_set_no_made_flush_straight_flop2),
                                 ('self.flopped_nut_flush_draw_nut_wrap_flop2', self.flopped_nut_flush_draw_nut_wrap_flop2),
                                 ('self.flopped_nut_straight_with_house_or_flush_redraw_flop2', self.flopped_nut_straight_with_house_or_flush_redraw_flop2),
                                 ('self.nut_house_on_flop2', self.nut_house_on_flop2)
                                 ]
        hand_ratings_flop2[4] = [('self.top_set_on_made_flush_straight_board_flop2', self.top_set_on_made_flush_straight_board_flop2),
                                 ('self.nut_wrap_non_nut_flush_draw_flop2', self.nut_wrap_non_nut_flush_draw_flop2),
                                 ('self.non_nut_wrap_nut_flush_draw_flop2', self.non_nut_wrap_nut_flush_draw_flop2),
                                 ('self.flopped_underhouse_flop2', self.flopped_underhouse_flop2),
                                 ('self.flopped_any_set_flop2', self.flopped_any_set_flop2),
                                 ('self.flopped_house_with_overhouse_avail_flop2', self.flopped_house_with_overhouse_avail_flop2),
                                 ('self.any_wrap_on_rainbow_board_flop2', self.any_wrap_on_rainbow_board_flop2),
                                 ('self.summary_of_hand_ratings_and__my_hand_on_flop2', self.summary_of_hand_ratings_and_my_hand_on_flop2)
                                 ]
        return hand_ratings_flop1, hand_ratings_flop2

    def helper_check_raise(self):
        """
        This function will return True is the SPR is such that betting pot on every street will
        not get the money in by the river.
        It will return False, if betting the pot every street will result in all the money going in.

        Reminder:
        SPR CONSIDERATIONS
        1. An SPR of 12x the pot on the flop means if you bet pot on each street all the money can go in by the river.
        2. An SPR of 27x the pot on the flop, if I go for a check raise on the flop, and bet the pot on every subsequent
           street, I can get all the money in by the river.
           Anything inbetween also falls in category 2. of course; 2. is like the upper end, meaning anything
           above 27x won't go in by the river.
        """
        highest_spr_in_play = max(spr for spr in self.SPR_tracker.values())

        return False if highest_spr_in_play <= 15 else True

    def helper_flopped_nut_flush_draw(self):
        """
        This function will check if I have the nut flush draw on either flops.
        """
        flopped_nut_flush_draw_flop1 = False
        flopped_nut_flush_draw_flop2 = False

        # check if there is flush draw and I have nut flush draw
        flop1_nut_flush_draw_nums_index_tracker = []
        flop2_nut_flush_draw_nums_index_tracker = []
        if self.is_flush_draw_on_flop1:
            for card in self.num_list:
                if card == self.nut_flush_draw_nums_on_flop1:
                    flop1_nut_flush_draw_nums_index_tracker.append(self.num_list.index(card))
        for index in flop1_nut_flush_draw_nums_index_tracker:
            if self.suit_list[index] == self.nut_flush_draw_suit_on_flop1:
                flopped_nut_flush_draw_flop1 = True
        if self.is_flush_draw_on_flop2:
            for card in self.num_list:
                if card == self.nut_flush_draw_nums_on_flop2:
                    flop2_nut_flush_draw_nums_index_tracker.append(self.num_list.index(card))
        for index in flop2_nut_flush_draw_nums_index_tracker:
            if self.suit_list[index] == self.nut_flush_draw_suit_on_flop1:
                flopped_nut_flush_draw_flop2 = True

        return flopped_nut_flush_draw_flop1, flopped_nut_flush_draw_flop2

    def helper_set_checker(self):
        """
        This function will return what set we have on the flop: top, middle, bottom, None.
        It will do this for both flops.
        """
        flopped_set_flop1 = None
        flopped_set_flop2 = None
        if self.num_list.count(self.flop1_nums[0]) >= 2:
            flopped_set_flop1 = 'top'
        elif self.num_list.count(self.flop1_nums[1]) >= 2:
            flopped_set_flop1 = 'middle'
        elif self.num_list.count(self.flop1_nums[2]) >= 2:
            flopped_set_flop1 = 'bottom'
        if self.num_list.count(self.flop2_nums[0]) >= 2:
            flopped_set_flop2 = 'top'
        elif self.num_list.count(self.flop2_nums[1]) >= 2:
            flopped_set_flop2 = 'middle'
        elif self.num_list.count(self.flop2_nums[2]) >= 2:
            flopped_set_flop2 = 'bottom'

        return flopped_set_flop1, flopped_set_flop2

    def over_house_check(self):
        """
        e.g. I have 10 10 on a 10 4 4 board.
        """
        overhouse_flop1 = False
        overhouse_flop2 = False

        if self.high_or_low_paired_board_flop1 == 'low':
            if self.num_list.count(self.flop1_nums[0]) >= 2:
                overhouse_flop1 = True
        if self.high_or_low_paired_board_flop2 == 'low':
            if self.num_list.count(self.flop2_nums[0]) >= 2:
                overhouse_flop2 = True
        return overhouse_flop1, overhouse_flop2

    def nut_flush_check(self):
        """
        This function will check if I have the nut flush.
        A bit awkward to check if I have nut flush; the way I do it is to check if in my hand I have the particular
        number of the nut flush card, and keep track of all the INDEXES of the nums in my hand that matches this number.
        Then need to look in my hand and check if for those INDEXES, the suit is the same as the nut flush suit.
        """
        flop1_nut_flush = False
        flop2_nut_flush = False
        flop1_nut_flush_nums_index_tracker = []
        flop2_nut_flush_nums_index_tracker = []

        if self.is_flush_completed_on_flop1:
            for card in self.num_list:
                if card == self.nut_flush_nums_flop1:
                    flop1_nut_flush_nums_index_tracker.append(self.num_list.index(card))
        for index in flop1_nut_flush_nums_index_tracker:
            if self.suit_list[index] == self.nut_flush_suit_flop1:
                flop1_nut_flush = True

        if self.is_flush_completed_on_flop2:
            for card in self.num_list:
                if card == self.nut_flush_nums_flop2:
                    flop2_nut_flush_nums_index_tracker.append(self.num_list.index(card))
        for index in flop2_nut_flush_nums_index_tracker:
            if self.suit_list[index] == self.nut_flush_suit_flop2:
                flop2_nut_flush = True

        return flop1_nut_flush, flop2_nut_flush

    def quads_checker(self):
        flopped_quads_flop1 = False
        flopped_quads_flop2 = False
        if self.high_or_low_paired_board_flop1 == 'low':
            if self.num_list.count(self.flop1_nums[1]) >= 2:
                flopped_quads_flop1 = True
        elif self.high_or_low_paired_board_flop1 == 'high':
            if self.num_list.count(self.flop1_nums[1]) >= 2:
                flopped_quads_flop1 = True
        if self.high_or_low_paired_board_flop2 == 'low':
            if self.num_list.count(self.flop2_nums[1]) >= 2:
                flopped_quads_flop2 = True
        elif self.high_or_low_paired_board_flop2 == 'high':
            if self.num_list.count(self.flop2_nums[1]) >= 2:
                flopped_quads_flop2 = True
        return flopped_quads_flop1, flopped_quads_flop2

    def top_set_no_made_flush_straight_checker(self):
        """
        This function will return True if I have top set and there is no made flush or straight on the flop.
        """
        # check if we have top set
        top_set_no_made_flush_straight_flop1 = True if self.flopped_set_flop1 == 'top' else False
        top_set_no_made_flush_straight_flop2 = True if self.flopped_set_flop2 == 'top' else False

        # check if there are any made flush or straight completed on either flops
        if self.is_flush_completed_on_flop1 or self.is_straight_completed_on_flop1:
            top_set_no_made_flush_straight_flop1 = False
        if self.is_flush_completed_on_flop2 or self.is_straight_completed_on_flop2:
            top_set_no_made_flush_straight_flop2 = False

        return top_set_no_made_flush_straight_flop1, top_set_no_made_flush_straight_flop2

    def nut_flush_draw_nut_wrap(self):
        flopped_nut_flush_draw_nut_wrap_flop1 = False
        flopped_nut_flush_draw_nut_wrap_flop2 = False

        # check if there is a wrap and I have nut wrap
        if self.three_card_wrap_combis_on_flop1:
            if all(card in self.num_list for card in self.three_card_wrap_combis_on_flop1):
                flopped_nut_flush_draw_nut_wrap_flop1 = True
        if self.three_card_wrap_combis_on_flop2:
            if all(card in self.num_list for card in self.three_card_wrap_combis_on_flop2):
                flopped_nut_flush_draw_nut_wrap_flop2 = True

        # check if I have nut flush draw as well
        if flopped_nut_flush_draw_nut_wrap_flop1 and self.flopped_nut_flush_draw_flop1:
            flopped_nut_flush_draw_nut_wrap_flop1 = True
        if flopped_nut_flush_draw_nut_wrap_flop2 and self.flopped_nut_flush_draw_flop2:
            flopped_nut_flush_draw_nut_wrap_flop2 = True

        return flopped_nut_flush_draw_nut_wrap_flop1, flopped_nut_flush_draw_nut_wrap_flop2

    def flopped_nut_straight_with_house_or_flush_redraw(self):
        flopped_nut_straight_with_house_flush_redraw_flop1 = False
        flopped_nut_straight_with_house_flush_redraw_flop2 = False

        # check if I flopped any flush draw
        flopped_any_flush_draw_flop1 = True if self.is_flush_draw_on_flop1 and self.suit_list.count(self.nut_flush_draw_suit_on_flop1) >= 2 else False
        flopped_any_flush_draw_flop2 = True if self.is_flush_draw_on_flop2 and self.suit_list.count(self.nut_flush_draw_suit_on_flop2) >= 2 else False

        if self.two_card_combis_that_complete_the_straight_on_flop1:
            # check I have nut straight
            if all(card in self.num_list for card in self.two_card_combis_that_complete_the_straight_on_flop1[0]):
                # check if I have set or flush redraw
                if self.flopped_set_flop1 or flopped_any_flush_draw_flop1:
                    flopped_nut_straight_with_house_flush_redraw_flop1 = True

        if self.two_card_combis_that_complete_the_straight_on_flop2:
            if all(card in self.num_list for card in self.two_card_combis_that_complete_the_straight_on_flop2[0]):
                if self.flopped_set_flop2 or flopped_any_flush_draw_flop2:
                    flopped_nut_straight_with_house_flush_redraw_flop2 = True

        return flopped_nut_straight_with_house_flush_redraw_flop1, flopped_nut_straight_with_house_flush_redraw_flop2

    def check_nut_house_on_flop(self):
        """
        This function will return if we have the nut house.
        This is only possible if we have a 'high' paired board, e.g. 10 10 4
        """
        flopped_nut_house_on_flop1 = False
        flopped_nut_house_on_flop2 = False
        if self.high_or_low_paired_board_flop1 == 'high':
            if self.flop1_nums[1] in self.num_list and self.flop1_nums[2] in self.num_list:
                flopped_nut_house_on_flop1 = True
        if self.high_or_low_paired_board_flop2 == 'high':
            if self.flop2_nums[1] in self.num_list and self.flop2_nums[2] in self.num_list:
                flopped_nut_house_on_flop2 = True

        return flopped_nut_house_on_flop1, flopped_nut_house_on_flop2

    def top_set_on_made_flush_straight_board(self):
        """
        This function will return whether I have top set on a made flush or made straight flop.
        """
        top_set_on_made_flush_straight_flop1 = False
        top_set_on_made_flush_straight_flop2 = False

        if self.flopped_set_flop1 == 'high':
            if self.is_straight_completed_on_flop1 or self.is_flush_completed_on_flop1:
                top_set_on_made_flush_straight_flop1 = True
        if self.flopped_set_flop2 == 'high':
            if self.is_straight_completed_on_flop2 or self.is_flush_completed_on_flop2:
                top_set_on_made_flush_straight_flop2 = True

        return top_set_on_made_flush_straight_flop1, top_set_on_made_flush_straight_flop2

    def nut_wrap_non_nut_flush_draw(self):
        # check if there is a wrap and I have nut wrap
        flopped_nut_wrap_flop1 = True if self.three_card_wrap_combis_on_flop1 and \
            all(card in self.num_list for card in self.three_card_wrap_combis_on_flop1) else False
        flopped_nut_wrap_flop2 = True if self.three_card_wrap_combis_on_flop2 and \
            all(card in self.num_list for card in self.three_card_wrap_combis_on_flop2) else False

        # check if I flopped any flush draw
        flopped_nut_wrap_non_nut_flush_draw_flop1 = True if self.is_flush_draw_on_flop1 and \
            flopped_nut_wrap_flop1 and self.suit_list.count(self.nut_flush_draw_suit_on_flop1) >= 2 else False
        flopped_nut_wrap_non_nut_flush_draw_flop2 = True if self.is_flush_draw_on_flop2 and \
            flopped_nut_wrap_flop2 and self.suit_list.count(self.nut_flush_draw_suit_on_flop2) >= 2 else False

        return flopped_nut_wrap_non_nut_flush_draw_flop1, flopped_nut_wrap_non_nut_flush_draw_flop2

    def non_nut_wrap_nut_flush_draw(self):
        # check if there is a wrap possible on flop and if I have any wrap
        flopped_any_wrap_flop1 = True if self.three_card_wrap_combis_on_flop1 and \
            any(all(card in self.num_list for card in wrap) for wrap in self.three_card_wrap_combis_on_flop1) else False
        flopped_any_wrap_flop2 = True if self.three_card_wrap_combis_on_flop2 and \
            any(all(card in self.num_list for card in wrap) for wrap in self.three_card_wrap_combis_on_flop2) else False

        # check if I flopped nut flush draw
        flopped_non_nut_wrap_nut_flush_draw_flop1 = True if self.flopped_nut_flush_draw_flop1 and flopped_any_wrap_flop1 else False
        flopped_non_nut_wrap_nut_flush_draw_flop2 = True if self.flopped_nut_flush_draw_flop2 and flopped_any_wrap_flop2 else False
        return flopped_non_nut_wrap_nut_flush_draw_flop1, flopped_non_nut_wrap_nut_flush_draw_flop2

    def flopped_under_house(self):
        """
        This function will return if we flopped an underhouse on either flops.
        And underhouse is if board is 10 10 4 and I have 4 4 in my hand.
        """
        flopped_underhouse_flop1 = True if self.high_or_low_paired_board_flop1 == 'low' and \
            self.num_list.count(self.flop1_nums[2]) >= 2 else False
        flopped_underhouse_flop2 = True if self.high_or_low_paired_board_flop2 == 'low' and \
            self.num_list.count(self.flop2_nums[2]) >= 2 else False

        return flopped_underhouse_flop1, flopped_underhouse_flop2

    def flopped_house_with_overhouse_avail(self):
        """
        e.g. flop: 10 10 4 and I have a 10 and a 4 in my hand.
        """
        flopped_house_with_overhouse_avail_flop1 = True if self.high_or_low_paired_board_flop1 == 'high' and \
            all(card in self.num_list for card in (self.flop1_nums[1], self.flop1_nums[2])) else False
        flopped_house_with_overhouse_avail_flop2 = True if self.high_or_low_paired_board_flop2 == 'high' and \
            all(card in self.num_list for card in (self.flop2_nums[1], self.flop2_nums[2])) else False

        return flopped_house_with_overhouse_avail_flop1, flopped_house_with_overhouse_avail_flop2

    def any_wrap_on_rainbow_board(self):
        """rainbow board is one where there is no flush draw available and no completed flush"""
        # check if there is a wrap possible on flop and if I have any wrap
        flopped_any_wrap_flop1 = True if self.three_card_wrap_combis_on_flop1 and \
            any(all(card in self.num_list for card in wrap) for wrap in self.three_card_wrap_combis_on_flop1) else False
        flopped_any_wrap_flop2 = True if self.three_card_wrap_combis_on_flop2 and \
            any(all(card in self.num_list for card in wrap) for wrap in self.three_card_wrap_combis_on_flop2) else False

        # check no flush draw and no flush completed on either flops
        flopped_any_wrap_on_rainbow_board_flop1 = True if flopped_any_wrap_flop1 and not self.is_flush_draw_on_flop1 \
            and not self.is_flush_completed_on_flop1 else False
        flopped_any_wrap_on_rainbow_board_flop2 = True if flopped_any_wrap_flop2 and not self.is_flush_draw_on_flop2 \
            and not self.is_flush_completed_on_flop2 else False

        return flopped_any_wrap_on_rainbow_board_flop1, flopped_any_wrap_on_rainbow_board_flop2


# x = AnalyseMyHandOnFlop()
# AnalyseMyHandOnFlop.organise_flop('whatever')

x = FlopHelper(5, [10, 6, 5], ['S', 'S', 'S'])
