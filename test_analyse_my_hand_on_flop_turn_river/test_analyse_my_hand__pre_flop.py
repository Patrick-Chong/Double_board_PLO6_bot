from analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop import PreFlopHandCombinations, ShouldWePlayThisPreFlopHand

import pytest
import mock


stack_tracker = {1: 500, 2: 600, 3: 100, 4: 100, 5: 300, 6: 200}
SPR_tracker = {1: 5, 2: 6, 3: 1, 4: 1, 5: 3, 6: 2}
guy_to_right_bet_size = 100
positions_of_players_to_act_ahead_of_me = []
pot_size = 100
my_position = 5
num_list = [10, 7, 3, 3, 2, 2]
suit_list = ['S', 'S', 'S', 'S', 'S', 'S']
big_blind = 0.4


class TestPreFlopHandCombinations:

    @pytest.mark.parametrize('num_list,expected_res', [
        ([14, 14, 13, 9, 8, 4], False),  # no 4 high cards above 10 or 5 high cards above 9
        ([14, 14, 13, 13, 12, 4], True),  # 4 high cards above 10
        ([14, 14, 13, 9, 9, 4], True),  # 5 high cards above 9
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair')
    def test_count_high_cards(self, mock_check_for_wrap_and_wrap_plus_pair, num_list, expected_res):
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.num_list = num_list
        actual_res = pfhc.count_high_cards()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,expected_res', [
        ([14, 13, 13, 9, 8, 4], ['S', 'C', 'H', 'C', 'S', 'C'], True),  # single suited ace
        ([14, 14, 13, 13, 12, 4], ['S', 'C', 'H', 'C', 'S', 'C'], True),  # double suited ace - same result as single suited for this function
        ([13, 13, 13, 9, 9, 4], ['S', 'C', 'H', 'C', 'S', 'C'], False),  # suited but not ace suited
        ([14, 13, 13, 9, 9, 4], ['S', 'C', 'H', 'C', 'H', 'C'], False),  # Just ace suited but not other card
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair')
    def test_single_suited_ace(self, mock_check_for_wrap_and_wrap_plus_pair, num_list, suit_list, expected_res):
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.num_list = num_list
        pfhc.suit_list = suit_list
        actual_res = pfhc.single_suited_ace()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,expected_res', [
        ([14, 14, 10, 9, 8, 4], ['S', 'C', 'H', 'C', 'S', 'C'], False),  # not king in hand
        ([14, 14, 13, 13, 12, 4], ['S', 'C', 'H', 'C', 'S', 'C'], True),  # suited king
        ([13, 13, 13, 9, 9, 4], ['S', 'C', 'H', 'C', 'H', 'C'], True),  # double suited kings; should be same result as single suited for this function
        ([14, 13, 13, 9, 9, 4], ['S', 'C', 'H', 'S', 'D', 'S'], False),  # Just King suited but not other card
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair')
    def test_single_suited_king(self, mock_check_for_wrap_and_wrap_plus_pair, num_list, suit_list, expected_res):
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.num_list = num_list
        pfhc.suit_list = suit_list
        actual_res = pfhc.single_suited_king()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,expected_res', [
        ([14, 13, 13, 9, 8, 4], ['S', 'C', 'H', 'C', 'S', 'C'], False),  # single suited ace
        ([14, 14, 13, 13, 12, 4], ['S', 'C', 'H', 'C', 'S', 'C'], True),  # double suited ace
        ([13, 13, 13, 9, 9, 4], ['S', 'C', 'H', 'C', 'S', 'C'], False),  # No ace in hand
        ([14, 14, 13, 9, 9, 4], ['S', 'C', 'H', 'H', 'H', 'D'], False),  # Two aces but both not suited
        ([14, 14, 13, 9, 9, 4], ['S', 'C', 'H', 'S', 'H', 'D'], False),  # Single suited ace
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair')
    def test_double_suited_ace(self, mock_check_for_wrap_and_wrap_plus_pair, num_list, suit_list, expected_res):
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.num_list = num_list
        pfhc.suit_list = suit_list
        actual_res = pfhc.double_suited_ace()
        assert actual_res == expected_res

    @pytest.mark.parametrize('suit_list,expected_res', [
        (['S', 'C', 'H', 'C', 'S', 'C'], True),  # double suited anything
        (['S', 'C', 'H', 'S', 'S', 'D'], False),  # single suited anything
        (['S', 'C', 'H', 'S', 'C', 'H'], True),  # triple suited suited anything
        (['S', 'C', 'C', 'C', 'C', 'C'], False),  # single suited
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair')
    def test_double_suited(self, mock_check_for_wrap_and_wrap_plus_pair, suit_list, expected_res):
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.suit_list = suit_list
        actual_res = pfhc.double_suited()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,expected_res', [
        ([14, 14, 13, 9, 8, 4], True),  # high pair in my hand
        ([14, 10, 10, 9, 8, 4], True),  # high pair in my hand
        ([14, 14, 10, 10, 8, 4], True),  # two high pair in my hand
        ([14, 10, 9, 9, 8, 4], False),  # no high pair in my hand
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair')
    def test_high_pairs_in_my_hand(self, mock_check_for_wrap_and_wrap_plus_pair, num_list, expected_res):
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.num_list = num_list
        actual_res = pfhc.high_pairs_in_my_hand()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,expected_res', [
        ([10, 9, 8, 7, 3, 2], (True, False)),  # 4 card wrap in my hand
        ([10, 9, 8, 7, 7, 2], (True, True)),  # 4 card wrap + pair in my hand
        ([10, 9, 8, 3, 3, 2], (False, False)),  # 3 card wrap - which is not considered a wrap by this function
        ([10, 10, 9, 9, 8, 7], (True, True)),  # 4 card wrap + two pairs
        ([10, 9, 8, 7, 6, 6], (True, True)),
    ])
    def test_check_for_wrap_and_wrap_plus_pair(self, num_list, expected_res):
        """
        As a gentle reminder, I will only consider 4 card wraps as wraps- after the epiphany that I encountered
        3 card wraps are far inferior to 4 card wraps.
        """
        pfhc = PreFlopHandCombinations(my_position, num_list, suit_list)
        pfhc.num_list = num_list
        actual_res = pfhc.check_for_wrap_and_wrap_plus_pair()
        assert actual_res == expected_res


class TestShouldWePlayThisPreFlopHand:

    @pytest.mark.parametrize('at_least_four_high_cards,single_suited_ace_f,single_suited_king_f,wrap_no_pair,wrap_plus_pair,high_pairs_in_my_hand,count_high_cards,expected_res', [
        (True, True, True, True, True, True, True, True),  # all pillars marked as True
        (False, False, False, True, True, True, False, False),  # marking both wrap and wrap plus pair as True + 1 other, but this is only 2 pillar so should fail
        (False, False, True, True, True, False, True, True),  # same as above but marking one more True to make it 3 pillar True in total
        (False, True, True, False, False, True, False, False),  # marking both suited king and ace as True + 1 other ; so only 2 pillars in total met
        (False, True, True, True, False, True, False, True),  # Same as above but marking on more True
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.double_suited_ace')
    def test_does_my_hand_meet_at_least_three_pillars(self, mock_double_suited_ace, at_least_four_high_cards, single_suited_ace_f,
                                                      single_suited_king_f, wrap_no_pair, wrap_plus_pair, high_pairs_in_my_hand, count_high_cards, expected_res):
        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.single_suited_king', return_value=single_suited_king_f):
            with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.single_suited_ace', return_value=single_suited_ace_f):
                with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.check_for_wrap_and_wrap_plus_pair', return_value=(wrap_no_pair, wrap_plus_pair)):
                    with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.high_pairs_in_my_hand', return_value=high_pairs_in_my_hand):
                        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand__pre_flop.PreFlopHandCombinations.count_high_cards', return_value=count_high_cards):
                            swptpfh = ShouldWePlayThisPreFlopHand(my_position, num_list, suit_list)
                            actual_res = swptpfh.does_my_hand_meet_at_least_three_pillars()
                            assert actual_res == expected_res
