import pytest
import mock
from analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn import AnalyseMyHandOnTurn


stack_tracker = {1:500, 2:600, 3:100, 4:100, 5:300, 6:200}
SPR_tracker = {1:5, 2:6, 3:1, 4:1, 5:3, 6:2}
guy_to_right_bet_size = 100
positions_of_players_to_act_ahead_of_me = []
pot_size = 100
my_position = 5
num_list = [10, 7, 3, 3, 2, 2]
suit_list = ['S', 'S', 'S', 'S', 'S', 'S']
big_blind = 0.4


class TestAnalyseMyHandOnTurn:

    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_organise_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        actual = amhot.organise_turn()
        expected = [[14, 'S'], [8, 'C'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C'], [2, 'S']]
        assert actual == expected

    @pytest.mark.parametrize('turn,did_board_pair,did_board_pair_highest_card', [
        ([[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']], True, True),  # board paired, paired highest card
        ([[10, 'S'], [7, 'C'], [2, 'C'], [2, 'S']], True, False),  # board paired, paired not highest card
        ([[10, 'S'], [9, 'C'], [7, 'C'], [2, 'S']], False, False),  # board did not pair
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_did_board_pair_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, turn, did_board_pair, did_board_pair_highest_card):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        expected_did_board_pair = did_board_pair
        expected_did_board_pair_highest_card = did_board_pair_highest_card

        actual = amhot.did_board_pair_on_turn(turn)
        assert actual == (expected_did_board_pair, expected_did_board_pair_highest_card)

    @pytest.mark.parametrize('turn,flush_completed,nut_flush_num,nut_flush_suit', [
        ([[10, 'S'], [10, 'S'], [7, 'S'], [2, 'C']], True, 14, 'S'),
        ([[14, 'S'], [14, 'C'], [2, 'C'], [2, 'C']], True, 13, 'C'),
        ([[14, 'S'], [14, 'C'], [13, 'C'], [6, 'C']], True, 12, 'C'),
        ([[14, 'S'], [14, 'C'], [13, 'C'], [12, 'C']], True, 11, 'C'),
        ([[14, 'C'], [13, 'C'], [12, 'C'], [11, 'C']], True, 10, 'C'),
        ([[10, 'S'], [9, 'C'], [7, 'C'], [2, 'S']], False, False, False),
        ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_flush_completed_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, turn, flush_completed, nut_flush_num, nut_flush_suit):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        expected_flush_completed = flush_completed
        expected_nut_flush_num = nut_flush_num
        expected_nut_flush_suit = nut_flush_suit
        actual = amhot.flush_completed_on_turn(turn)

        assert actual == (expected_flush_completed, expected_nut_flush_num, expected_nut_flush_suit)

    @pytest.mark.parametrize('turn,straight_completed,list_of_two_card_straight_completing_combi', [
        # checking for straight btw first 3 cards
        ([[10, 'S'], [7, 'S'], [6, 'S'], [2, 'C']], True, [[9, 8]]),
        ([[10, 'S'], [9, 'S'], [6, 'S'], [2, 'C']], True, [[8, 7]]),
        ([[10, 'S'], [8, 'S'], [6, 'S'], [2, 'C']], True, [[9, 7]]),
        ([[10, 'S'], [9, 'S'], [8, 'S'], [2, 'C']], True, [[12, 11], [11, 7], [7, 6]]),
        ([[14, 'S'], [13, 'S'], [12, 'S'], [2, 'C']], True, [[11, 10]]),
        ([[14, 'S'], [12, 'C'], [11, 'C'], [2, 'C']], True, [[13, 10]]),
        ([[14, 'S'], [11, 'C'], [10, 'C'], [6, 'C']], True, [[13, 12]]),
        ([[13, 'S'], [12, 'C'], [10, 'C'], [6, 'C']], True, [[14, 11], [11, 9]]),
        ([[13, 'S'], [12, 'C'], [11, 'C'], [6, 'C']], True, [[14, 10], [10, 9]]),
        ([[12, 'S'], [11, 'C'], [9, 'C'], [6, 'C']], True, [[13, 10], [10, 8]]),
        ([[10, 'S'], [9, 'C'], [3, 'C'], [2, 'S']], False, None),
        # checking for straight btw 2nd 3rd and 4th cards
        ([[14, 'S'], [7, 'S'], [4, 'S'], [3, 'C']], True, [[6, 5]]),
        ([[14, 'S'], [7, 'S'], [6, 'S'], [3, 'C']], True, [[5, 4]]),
        ([[14, 'S'], [7, 'S'], [5, 'S'], [3, 'C']], True, [[6, 4]]),
        ([[14, 'S'], [7, 'S'], [6, 'S'], [5, 'C']], True, [[9, 8], [8, 4], [4, 3]]),
        ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_any_straight_completed_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, turn, straight_completed, list_of_two_card_straight_completing_combi):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        expected_straight_completed = straight_completed
        expected_list_of_two_card_straight_completing_combi = list_of_two_card_straight_completing_combi
        actual = amhot.any_straight_completed_on_turn(turn)

        assert actual == (expected_straight_completed, expected_list_of_two_card_straight_completing_combi)

    @pytest.mark.parametrize('turn,flush_draw_on_board,nut_flush_num_and_suit', [
        ([[10, 'S'], [7, 'S'], [6, 'H'], [2, 'C']], True, [[14, 'S']]),
        ([[14, 'S'], [9, 'S'], [6, 'H'], [2, 'C']], True, [[13, 'S']]),
        ([[14, 'S'], [13, 'S'], [6, 'H'], [2, 'C']], True, [[12, 'S']]),
        ([[14, 'S'], [13, 'S'], [8, 'H'], [2, 'H']], True, [[12, 'S'], [14, 'H']]),
        ([[14, 'S'], [13, 'C'], [8, 'H'], [2, 'D']], False, []),
        ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_any_flush_draw_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, turn, flush_draw_on_board, nut_flush_num_and_suit):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        expected_flush_draw_on_board = flush_draw_on_board
        expected_nut_flush_num_and_suit = nut_flush_num_and_suit
        actual = amhot.any_flush_draw_on_turn(turn)

        assert actual == (expected_flush_draw_on_board, expected_nut_flush_num_and_suit)

    @pytest.mark.parametrize('turn,is_wrap_on_board,list_of_wraps', [
        # ignore the PAIRED cards below; this gets dealt with later - I used it just for testing the other cards create the correct wrap!
        ([[12, 'S'], [8, 'S'], [2, 'H'], [2, 'C']], True, [[11, 10, 9]]),
        ([[14, 'S'], [10, 'S'], [6, 'H'], [2, 'C']], True, [[13, 12, 11], [9, 8, 7], [5, 4, 3]]),
        ([[10, 'S'], [7, 'S'], [2, 'H'], [2, 'C']], True, [[11, 9, 8], [9, 8, 6]]),
        ([[10, 'S'], [7, 'S'], [6, 'H'], [6, 'H']], False, []),  # this should return False as there is made straight
        ([[13, 'S'], [8, 'C'], [5, 'H'], [2, 'D']], True, [[9, 7, 6], [7, 6, 4], [6, 4, 3], [4, 3, 1]]),
        ([[14, 'S'], [13, 'C'], [7, 'H'], [4, 'D']], True, [[12, 11, 10], [8, 6, 5], [6, 5, 3]]),
        ([[13, 'S'], [12, 'C'], [7, 'H'], [2, 'D']], True, [[14, 11, 10], [11, 10, 9]]),
        ([[8, 'S'], [7, 'C'], [2, 'H'], [2, 'D']], True, [[11, 10, 9], [10, 9, 6], [9, 6, 5], [6, 5, 4]]),
        ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_any_wrap_draw_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, turn, is_wrap_on_board, list_of_wraps):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        expected_is_wrap_on_board = is_wrap_on_board
        expected_list_of_wraps = list_of_wraps
        actual_wrap_generator = amhot.any_wrap_draw_on_turn(turn)
        actual_wrap_on_board = actual_wrap_generator[0]
        actual_list_of_wraps = actual_wrap_generator[1]

        assert actual_wrap_on_board == expected_is_wrap_on_board
        assert all(wraps in expected_list_of_wraps for wraps in actual_list_of_wraps)


    # ------------------------------------------- below are testing my_hand_ratings being filled correctly

    @pytest.mark.parametrize('turns,num_list,did_board_pair_on_turn,my_hand_rating', [
        # top card paired
        (([[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']], [[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']]), [10, 7, 3, 3, 2, 2], True, 7),
        (([[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']], [[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']]), [10, 2, 3, 3, 2, 2], True, 5),
        (([[10, 'S'], [10, 'C'], [7, 'C'], [7, 'S']], [[10, 'S'], [10, 'C'], [7, 'C'], [7, 'S']]), [10, 7, 3, 3, 2, 2], True, 7),
        # middle card paired
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [10, 10, 3, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [7, 7, 3, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [10, 7, 3, 3, 2, 2], False, 6.5),
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [9, 7, 5, 3, 2, 2], False, 5),
        # bottom card paired
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [9, 5, 5, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [10, 10, 5, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [7, 7, 5, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [10, 7, 5, 3, 2, 2], False, 6.5),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [8, 7, 5, 3, 2, 2], False, 5),
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnFlop')
    def test_is_board_paired_on_turn(self, mock_AnalyseMyHandOnFlop, mockFlopHelper, turns, num_list, did_board_pair_on_turn, my_hand_rating):
        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.organise_turn', return_value=turns):
            amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)
            amhot.did_board_pair_on_turn1 = True
            amhot.did_board_pair_on_turn2 = True
            amhot.board_pair_top_card_turn1 = did_board_pair_on_turn
            amhot.board_pair_top_card_turn2 = did_board_pair_on_turn
            amhot.num_list = num_list
            amhot.is_board_paired_on_turn()
        assert amhot.hand_ratings_turn1.get('board_paired') == my_hand_rating
        assert amhot.hand_ratings_turn2.get('board_paired') == my_hand_rating

    @pytest.mark.parametrize('num_list,suit_list,did_flush_complete_on_turn,did_board_pair,nut_flush_nums,nut_flush_suit,my_hand_rating', [
        ([14, 13, 12, 12, 10, 9], ['S', 'S', 'S', 'C', 'C', 'S'], True, False, 14, 'S', 7),  # nut flush in my hand
        ([13, 13, 12, 12, 10, 9], ['S', 'S', 'S', 'C', 'C', 'S'], True, False, 14, 'S', 5),  # non nut flush in my hand
        ([13, 13, 12, 12, 10, 9], ['C', 'C', 'C', 'C', 'C', 'C'], True, False, 14, 'S', None),  # no flush in my hand
        ([14, 13, 12, 12, 10, 9], ['S', 'S', 'S', 'C', 'C', 'S'], True, True, 14, 'S', None),  # board paired
        ([14, 13, 12, 12, 10, 9], ['S', 'S', 'S', 'C', 'C', 'S'], False, False, 14, 'S', None),  # no flush on board
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_is_flush_completed_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, num_list, suit_list,
                                        did_flush_complete_on_turn, did_board_pair, nut_flush_nums, nut_flush_suit, my_hand_rating):

        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)
        amhot.num_list = num_list
        amhot.suit_list = suit_list
        amhot.did_board_pair_on_turn1 = did_board_pair
        amhot.did_flush_completed_on_turn1 = did_flush_complete_on_turn
        amhot.nut_flush_nums_turn1 = nut_flush_nums
        amhot.nut_flush_suit_turn1 = nut_flush_suit
        amhot.is_flush_completed_on_turn()
        assert amhot.hand_ratings_turn1.get('made_flush') == my_hand_rating

    @pytest.mark.parametrize('num_list,suit_list,did_straight_complete_on_turn1,two_card_combi_completing_straight_on_turn1,is_did_board_paired,did_flush_complete,my_hand_rating', [
        ([14, 13, 12, 12, 8, 6], ['S', 'S', 'S', 'C', 'C', 'S'], True, [[8, 6]], False, False, 6.5),  # nut straight in my hand
        ([14, 13, 12, 12, 6, 4], ['S', 'S', 'S', 'C', 'C', 'S'], True, [[8, 6], [6, 4]], False, False, 5),  # non nut straight in my hand
        ([14, 13, 12, 12, 8, 6], ['S', 'S', 'S', 'C', 'C', 'S'], True, [[8, 6], [6, 4]], True, False, None),  # I have straight but flush completed
        ([14, 13, 12, 12, 8, 6], ['S', 'S', 'S', 'C', 'C', 'S'], True, [[8, 6], [6, 4]], False, True, None),  # I have straight but board paired
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_is_straight_completed_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, num_list, suit_list,
                                        did_straight_complete_on_turn1, two_card_combi_completing_straight_on_turn1, is_did_board_paired, did_flush_complete, my_hand_rating):

        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)
        amhot.num_list = num_list
        amhot.suit_list = suit_list
        amhot.did_board_pair_on_turn1 = is_did_board_paired
        amhot.did_straight_complete_on_turn1 = did_straight_complete_on_turn1
        amhot.two_card_combi_completing_straight_on_turn1 = two_card_combi_completing_straight_on_turn1
        amhot.did_flush_completed_on_turn1 = did_flush_complete
        amhot.is_straight_completed_on_turn()
        assert amhot.hand_ratings_turn1.get('made_straight') == my_hand_rating

    @pytest.mark.parametrize('num_list,suit_list,turns,did_straight_complete_on_turn1,did_flush_completed_on_turn1,did_board_pair_on_turn1,my_hand_rating, actual_res', [
        ([14, 14, 12, 12, 8, 6], ['S', 'C', 'S', 'C', 'C', 'S'], [[[14, 'S'], [12, 'C'], [8, 'S'], [2, 'C']], [[14, 'S'], [12, 'C'], [8, 'S'], [2, 'C']]], False, False, False, 6.5, ('top', 'top')),  # top set
        ([13, 13, 12, 12, 8, 6], ['S', 'C', 'S', 'C', 'C', 'S'], [[[14, 'S'], [12, 'C'], [8, 'S'], [2, 'C']], [[14, 'S'], [12, 'C'], [8, 'S'], [2, 'C']]], False, False, False, 6.5, ('middle', 'middle')),  # mid set
        ([13, 13, 12, 11, 2, 2], ['S', 'C', 'S', 'C', 'C', 'S'], [[[14, 'S'], [12, 'C'], [8, 'S'], [2, 'C']], [[14, 'S'], [12, 'C'], [8, 'S'], [2, 'C']]], False, False, False, 5.5, ('bottom', 'bottom')),  # bottom set
        ([13, 13, 12, 11, 2, 2], ['S', 'C', 'S', 'C', 'C', 'S'], [[[14, 'S'], [13, 'C'], [12, 'S'], [2, 'C']], [[14, 'S'], [13, 'C'], [12, 'S'], [2, 'C']]], True, False, False, 5.5, ('middle', 'middle')),  # set on made turn
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnFlop')
    def test_set_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, num_list, suit_list, turns,
                         did_straight_complete_on_turn1, did_flush_completed_on_turn1, did_board_pair_on_turn1, my_hand_rating, actual_res):
        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.organise_turn', return_value=turns):
            amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                            positions_of_players_to_act_ahead_of_me,
                                            pot_size, my_position, num_list, suit_list, big_blind)
            amhot.num_list = num_list
            amhot.suit_list = suit_list
            amhot.did_board_pair_on_turn1 = did_board_pair_on_turn1
            amhot.did_straight_complete_on_turn1 = did_straight_complete_on_turn1
            amhot.did_flush_completed_on_turn1 = did_flush_completed_on_turn1
            res = amhot.set_on_turn()
            assert amhot.hand_ratings_turn1.get('set_with_nothing_completed') == my_hand_rating
            assert res == actual_res

    @pytest.mark.parametrize('num_list,suit_list,did_board_pair_turn,flush_completed_turn,expected_res', [
        ([14, 13, 12, 12, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], False, False, ('nut', 'nut')),  # nut flush draw
        ([13, 12, 11, 12, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], False, False, ('some', 'some')),  # some flush draw
        ([13, 12, 11, 12, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], True, False, (None, None)),  # some flush draw but board paired
        ([13, 12, 11, 12, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], False, True, (None, None)),  # some flush draw but flush completed
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'C']))
    def test_is_flush_draw_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, num_list, suit_list,
                                        did_board_pair_turn, flush_completed_turn, expected_res):

        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)
        amhot.num_list = num_list
        amhot.suit_list = suit_list
        amhot.did_board_pair_on_turn1 = did_board_pair_turn
        amhot.did_board_pair_on_turn2 = did_board_pair_turn
        amhot.did_flush_completed_on_turn1 = flush_completed_turn
        amhot.did_flush_completed_on_turn2 = flush_completed_turn
        actual_res = amhot.is_flush_draw_on_turn()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,turns,is_wrap_draw_on_turn,board_paired_turn,flush_completed_turn,straight_completed_turn,list_of_wrap_combi_turn,expected_res', [
        ([11, 10, 10, 9, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], ([[14, 'S'], [13, 'C'], [8, 'C'], [2, 'S']], [[14, 'S'], [13, 'C'], [8, 'C'], [2, 'S']]), True, False, False, False, [[11, 10, 9]], ('nut', 'nut')),  # nut wrap draw
        ([13, 10, 10, 9, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], ([[14, 'S'], [13, 'C'], [8, 'C'], [7, 'S']], [[14, 'S'], [13, 'C'], [7, 'C'], [6, 'S']]), True, False, False, False, [[11, 10, 9], [10, 9, 8], [9, 8, 5], [8, 5, 4], [5, 4, 3]], ('some', 'some')),  # some wrap
        ([13, 10, 10, 9, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], ([[14, 'S'], [13, 'C'], [8, 'C'], [7, 'S']], [[14, 'S'], [13, 'C'], [7, 'C'], [6, 'S']]), True, True, False, False, [[11, 10, 9], [10, 9, 8], [9, 8, 5], [8, 5, 4], [5, 4, 3]], (None, None)),  # some wrap but board pair
        ([13, 10, 10, 9, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], ([[14, 'S'], [13, 'C'], [8, 'C'], [7, 'S']], [[14, 'S'], [13, 'C'], [7, 'C'], [6, 'S']]), True, False, True, False, [[11, 10, 9], [10, 9, 8], [9, 8, 5], [8, 5, 4], [5, 4, 3]], (None, None)),  # some wrap but flush complete
        ([13, 10, 10, 9, 8, 6], ['C', 'S', 'S', 'C', 'C', 'S'], ([[14, 'S'], [13, 'C'], [8, 'C'], [7, 'S']], [[14, 'S'], [13, 'C'], [7, 'C'], [6, 'S']]), True, False, False, True, [[11, 10, 9], [10, 9, 8], [9, 8, 5], [8, 5, 4], [5, 4, 3]], (None, None)),  # some wrap but straight complete
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnFlop')
    def test_is_wrap_draw_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, num_list, suit_list,
                                        turns, is_wrap_draw_on_turn, board_paired_turn, flush_completed_turn, straight_completed_turn, list_of_wrap_combi_turn, expected_res):
        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.organise_turn', return_value=turns):
            amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                            positions_of_players_to_act_ahead_of_me,
                                            pot_size, my_position, num_list, suit_list, big_blind)
            amhot.num_list = num_list
            amhot.suit_list = suit_list
            amhot.is_wrap_draw_on_turn1 = is_wrap_draw_on_turn
            amhot.is_wrap_draw_on_turn2 = is_wrap_draw_on_turn
            amhot.did_flush_completed_on_turn1 = flush_completed_turn
            amhot.did_flush_completed_on_turn2 = flush_completed_turn
            amhot.did_straight_complete_on_turn1 = straight_completed_turn
            amhot.did_straight_complete_on_turn2 = straight_completed_turn
            amhot.list_of_all_three_card_wrap_combi_turn1 = list_of_wrap_combi_turn
            amhot.list_of_all_three_card_wrap_combi_turn2 = list_of_wrap_combi_turn
            amhot.did_board_pair_on_turn1 = board_paired_turn
            amhot.did_board_pair_on_turn2 = board_paired_turn
            actual_res = amhot.is_wrap_draw_on_turn()
            assert actual_res == expected_res

    @pytest.mark.parametrize('is_wrap_draw_on_turn_res,is_flush_draw_on_turn_res,set_on_turn_res,hand_rating', [
        (['nut', 'nut'], ['nut', 'nut'], [None, None], 6.5),  # nut wrap nut flush
        (['some', 'some'], ['some', 'some'], [None, None], 5.5),  # some wrap some flush
        ([None, None], ['nut', 'nut'], ['top', 'top'], 6.5),  # top set nut flush
        ([None, None], ['some', 'some'], ['top', 'top'], 6.5),  # top set some flush
        ([None, None], ['some', 'some'], ['some', 'some'], 5.5),  # some set some flush
        (['nut', 'nut'], ['nut', 'nut'], ['some', 'some'], 6.5),  # nut wrap nut flush some set

        # ([None, None], ['some', 'some'], ['some', 'some'], 5.5),  # some set some flush

    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_combo_draw(self, mock_detect_turn_nums_and_suit, mock_organise_flop,
                                  is_wrap_draw_on_turn_res, is_flush_draw_on_turn_res, set_on_turn_res, hand_rating):
        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_wrap_draw_on_turn', return_value=is_wrap_draw_on_turn_res):
            with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_flush_draw_on_turn', return_value=is_flush_draw_on_turn_res):
                with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.set_on_turn', return_value=set_on_turn_res):
                    amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                                    positions_of_players_to_act_ahead_of_me,
                                                    pot_size, my_position, num_list, suit_list, big_blind)
                    amhot.combo_draw()
                    assert amhot.hand_ratings_turn1.get('combo_draw') == hand_rating

    @pytest.mark.parametrize('is_wrap_draw_on_turn_res,is_flush_draw_on_turn_res,set_on_turn_res,hand_rating', [
        ([None, None], ['some', 'some'], [None, None], 6.75),  # made straight with flush redraw
        ([None, None], [None, None], ['some', 'some'], 6.75),  # made straight with set redraw
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_combo_draw_made_straight(self, mock_detect_turn_nums_and_suit, mock_organise_flop,
                                  is_wrap_draw_on_turn_res, is_flush_draw_on_turn_res, set_on_turn_res, hand_rating):
        with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_wrap_draw_on_turn', return_value=is_wrap_draw_on_turn_res):
            with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_flush_draw_on_turn', return_value=is_flush_draw_on_turn_res):
                with mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.set_on_turn', return_value=set_on_turn_res):
                    amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                                    positions_of_players_to_act_ahead_of_me,
                                                    pot_size, my_position, num_list, suit_list, big_blind)
                    amhot.hand_ratings_turn1['made_straight'] = 6.5
                    amhot.combo_draw()
                    assert amhot.hand_ratings_turn1.get('made_straight') == hand_rating

    @pytest.mark.parametrize('hand_rating_turn1,hand_rating_turn2,guy_to_right_bet_size,pos_players_ahead_of_me,expected_action', [
        ({'made_flush': 7, 'combo_draw': 6, 'made_straight': 5.5}, {'made_flush': 6, 'combo_draw': 6, 'made_straight': 6}, 0, [], 'BET'),  # 7 7 rating
        ({'made_flush': 6.75, 'combo_draw': 5.5, 'made_straight': 5.5}, {'made_flush': 6.75, 'combo_draw': 5.5, 'made_straight': 5.5}, 0, [], 'BET'),  # 6.75 5.5 rating
        ({'made_flush': 6.5, 'combo_draw': 5.5, 'made_straight': 5.5}, {'made_flush': 6, 'combo_draw': 5.5, 'made_straight': 5.5}, 0, [], 'BET'),  # 6.5 6 rating
        ({'made_flush': 6.5, 'combo_draw': 5.5, 'made_straight': 5.5}, {'made_flush': 5.5, 'combo_draw': 5.5, 'made_straight': 5.5}, 0, [], 'BET'),  # 6.5 >6 rating, no one has bet
        ({'made_flush': 6.5, 'combo_draw': 5.5, 'made_straight': 5.5}, {'made_flush': 5.5, 'combo_draw': 5.5, 'made_straight': 5.5}, 10, [], 'CALL'),  # 6.5 >6 rating, someone has bet
        ({'made_flush': 5.5, 'combo_draw': 5.5, 'made_straight': 5.5}, {'made_flush': 5.5, 'combo_draw': 5.5, 'made_straight': 5.5}, 0, [], 'CALL'),  # hand not strong enough, no one bet
        ({'made_flush': 5.5, 'combo_draw': 5.5, 'made_straight': 5.5}, {'made_flush': 5.5, 'combo_draw': 5.5, 'made_straight': 5.5}, 10, [], 'FOLD'),  # hand not strong enough, someone bet
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.combo_draw')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_straight_completed_on_turn')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_flush_completed_on_turn')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.two_pair_no_flush_or_straight_completed')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn.AnalyseMyHandOnTurn.is_board_paired_on_turn')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_analyse_my_hand_against_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, mock_board_paired_on_turn, mock_two_pair_non_made_turn,
                                          mock_is_flush_completed_on_turn, mock_is_straight_completed_on_turn, mock_combo_draw, hand_rating_turn1,
                                          hand_rating_turn2, guy_to_right_bet_size, pos_players_ahead_of_me, expected_action):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                                    positions_of_players_to_act_ahead_of_me,
                                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhot.hand_ratings_turn1 = hand_rating_turn1
        amhot.hand_ratings_turn2 = hand_rating_turn2
        amhot.positions_of_players_to_act_ahead_of_me = positions_of_players_to_act_ahead_of_me
        amhot.guy_to_right_bet_size = guy_to_right_bet_size
        actual = amhot.analyse_my_hand_against_turn()
        assert actual == expected_action
