"""
Information I need to make best river decision possible:
1. Do I have the nuts on either/both board (absolute coconuts vs. nuts)?
Two people can have nut straight but two people cannot have nut flush; the latter is absolute coconuts.
2. Was I last aggressor on turn?
3. Did nuts change on either board with the river card?
4. Any draws (especially flush draws) on the turn that missed?/ got there
5. What is the SPR of those still in pot?
6. Anyone ahead of me to act / are we heads up?

Coding steps to gather above information:
- organise river cards into the turn
1. Check if I have absolute coconuts on either board or nut nut on either board; if so easy bet
To do this, just like on turn I'll need to code out, board pair, flush completed, straight completed. No need to check for draws thankfully.
2. My action on turn should be passed on in action_on_turn
3. Create function to check if nuts changes on either boards; particularly if flushes got there
This is important because if opp bet on turn and river changed and he check and we are heads up, I'll bet regardless.
This is a huge exploit that is easy to code.
4. Another function to check if many draws on turn and if they missed or got there
5/6 information we already have available, just think how to use it in decision making.
"""
from collections import defaultdict

from .analyse_my_hand_on_turn import AnalyseMyHandOnTurn
from flop_turn_river_cards import TheRiver
TR = TheRiver()


class AnalyseMyHandOnRiver(AnalyseMyHandOnTurn):
    def __init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                 positions_of_players_to_act_ahead_of_me,
                 pot_size, my_position, num_list, suit_list, big_blind):
        # As a learning point, the order of the below matters, so if you initialize self.special_hand1 before self.flop - you will get an error
        # since self.special_hand1 uses self.flop in it's function - makes perfect sense.
        AnalyseMyHandOnTurn.__init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)

        self.organise_river_f = self.organise_river()
        self.river = self.organise_river_f[0]
        self.river_num = self.organise_river_f[1]
        self.river_suit = self.organise_river_f[2]
        self.positions_of_players_to_act_ahead_of_me_f = positions_of_players_to_act_ahead_of_me

        # self.river = [[10, 'S'], [8, 'C'], [8, 'H'], [6, 'S'], [2, 'C']]
        # self.river_num = 10
        # self.river_suit = 'S'

        # check if there are any completed straights on the river - simple check
        self.any_straight_completed_on_river_f = self.any_straight_completed_on_river()
        self.did_any_straight_complete_on_river = self.any_straight_completed_on_river_f[0]
        self.three_cards_combis_that_make_straight_on_river = self.any_straight_completed_on_river_f[1]

        # Considers if straight is made on turn if river changes nuts or if no straight on turn if river completed any straights
        # and it returns all the 2 card combinations that complete those straights.
        self.all_two_card_combis_completing_straights_on_river = self.did_river_complete_any_straights_or_change_nuts_of_completed_straights()

        # check if flush completed on river, and the suit of the flush if so
        self.flush_complete_on_river = self.flush_completed_on_river()
        self.did_flush_complete_on_river = self.flush_complete_on_river[0]
        self.nut_flush_nums_river = self.flush_complete_on_river[1]  # N.B. This is not the largest nums of the flush on the board; e.g. [14, 13, 10, 2] all hearts; then this would be 12 of hearts.
        self.suit_of_flush_river = self.flush_complete_on_river[2]

        # check if I hit a flush on river; if I did, return the number of the highest flush card otherwise return False if I do not have the flush
        self.my_highest_num_of_the_completed_flush_on_river = self.did_I_hit_flush_on_river(self.river_suit)

        # check if I hit the nut straight or any straight on river
        self.did_I_hit_straight_on_river_f = self.did_I_hit_straight_on_river()

        # check if the board paired on the river - this will simply return True or False
        self.did_board_pair_on_river_f = self.did_board_pair_on_river()

    def any_straight_completed_on_river(self):
        """
        Analyse the river nums and check if any possible straight is present on the turn.

        Do this by checking 3 cards at a time, and since it is sorted we need to check 3 lots of 3.

        There is only a straight when the gap between the 3 cards is no more than 4.
        e.g. 10, 7, 6 or 10, 8, 6

        self.turn looks like [[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]
        """
        river_nums = [num[0] for num in self.river]
        three_card_combis_that_complete_straight_on_river = []
        if (river_nums[0] - river_nums[1]) + (river_nums[1] - river_nums[2]) <= 4:
            if river_nums[0] != river_nums[1] and river_nums[1] != river_nums[2]:
                three_card_combis_that_complete_straight_on_river.append(river_nums[:3])
        if (river_nums[1] - river_nums[2]) + (river_nums[2] - river_nums[3]) <= 4:
            if river_nums[1] != river_nums[2] and river_nums[2] != river_nums[3]:
                three_card_combis_that_complete_straight_on_river.append(river_nums[1:4])
        if (river_nums[2] - river_nums[3]) + (river_nums[3] - river_nums[4]) <= 4:
            if river_nums[2] != river_nums[3] and river_nums[3] != river_nums[4]:
                three_card_combis_that_complete_straight_on_river.append(river_nums[2:5])
        if three_card_combis_that_complete_straight_on_river:
            return True, three_card_combis_that_complete_straight_on_river
        return False, []

    def did_river_complete_any_straights_or_change_nuts_of_completed_straights(self):
        """
        ***The first half of the function builds on the scenario where there is already a straight on the turn.
        The second half considers the scenario when there is a straight draw on the flop and the turn comes in,
        and it checks if any straights are completed.

        N.B. To check if the river changed the nuts of the straight that is completed on the turn, you first need to
        grab the three straight making cards from the turn.
        It will either be the first three cards or the second/third/fourth card,
        e.g. for 9 8 7 6 ; 9 8 7 and 8 7 6
             for 10 5 4 3 ; 5 4 3
             for 10 9 8 2 ; 10 9 8

        Cases to cover:
        1) There was a made straight on the turn (doesn't matter to us if the straight was completed on the flop or turn)
                - check if river changed the nuts
                - check if river did not change the nuts
        2) No straight on turn but straight made with the river card.

        - (One edge case to consider, if we have something like 10 9 5 4 ; and the 7 hits on the river;
        this is not the case often but often enough to consider, as it completes the top and bottom straight).
        So it makes sense to always return the nut straight then consider lower straights- both are useful info to have.

        Definitely worth looking at the obvious straight draws on turn if there are any.
        This will determine a lot of thing for me.
        (TO DO FOR LATER - MAYBE NOT FOR MVP - CONSIDERATION IS QUITE DEEP)
        For MVP I'll just consider the above two main cases.
        """
        pass

    def did_I_hit_straight_on_river(self):
        """
        This function looks at all of the potential straights on the river, and by calling on
        self.did_river_complete_any_straights_or_change_nuts_of_completed_straights; it returns all
        two card combinations that complete the straights; it is in nutted order, so the first item in the
        list will be the nut straight.
        """
        all_two_card_straight_completing_combinations = []

        all_two_card_straight_completing_combinations = self.did_river_complete_any_straights_or_change_nuts_of_completed_straights()
        if all_two_card_straight_completing_combinations:
            nut_straight_two_cards = all_two_card_straight_completing_combinations[0]
            for two_cards in all_two_card_straight_completing_combinations:
                if all(card in self.num_list for card in two_cards):
                    # check if I have any straight or nut straight
                    if two_cards == nut_straight_two_cards:
                        return 'I_have_nut_straight'
                    else:
                        return 'I_have_non_nut_straight'

        return 'I_dont_have_straight'

    def did_board_pair_on_river(self):
        """
        This function will return True if the river card paired the board.
        """
        turn_nums = [card[0] for card in self.turn]
        if self.river_num in turn_nums:
            return True
        return False

    def organise_river(self):
        """
        turn will look like: [[13, 'S'], [10, 'C'], [9, 'S'], [8, 'C']] ; after we sort it.
        """
        river_generator = TR.add_river_card_num_and_suit_to_turn(self.turn)  # all we need to do here is to sort by number as we want the turn nums to still be in descending order
        river = river_generator[0]
        river_num = river_generator[1]
        river_suit = river_generator[2]

        return river, river_num, river_suit

    def analyse_final_check_on_river(self, flopped, card_helper):
        """
        This final check will as usual check the 3 main things that all main hands will check;
        1) did the board pair on river
        2) did a flush draw complete on the river
        3) did a straight complete and do I have the nut straight
        ** TO DO: when I write more main hands - consider just doing a function where the above 3 are checked
        rather than writing it out at the start of every hand.
        For MVP never mind, stick with this.

        Then it will continue all the hand from final_check on the turn.
        """
        pass




    def flush_completed_on_turn_play_river_exploit(self, flopped, card_helper):
        """EXPLOIT"""
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            # add randomiser, but I think lean towards folding as most would call river if they call turn with flush unless
            # they are pulling for house, so in any case, only worth betting 3/4
            if lowest_spr >= 2:
                return 'BET', 'betting river after flush completed on turn', 'bet river'




    def analyse_my_hand_against_river(self, action_on_turn, extra_information=None):
        """
        (R)!!!!!
        At the start of every main hand you MUST check
        1) did the board pair
        2) did a flush complete
        3) did a straight complete, and do I have the nut straight
        if 1) or 2) is True then coded a separate function to guide the play strategy.
        For 3), just check if straight got there and if so, to bet if I have the nut straight. Otherwise, other
        straight scenarios will be covered in the main hand.

        Doing the above check at the start will make your life 100% easier as you code out the possibilities of each hand.

        To make my life easier, it's also worth checking if I have the nut straight draw on the river and the board isn't paired and no flush
        because then I can comfortably get it all in. I might miss this in the main hand sometimes, because of all the complicated scenario -
        having this check makes it that much easier to play.

        N.B. if I do the above, I do not need to code as many scenarios over and over again,
        e.g. if I am drawing to the nut flush; then I won't need to repeatedly code the scenario if the flush got there on the
        river as it is taken care of at the start of the function.
        -------------------------------------------------------------

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
        """

        if self.guy_to_right_bet_size <=7:
            return 'call'
        if self.guy_to_right_bet_size == 0:
            return 'check'
        return 'fold'
