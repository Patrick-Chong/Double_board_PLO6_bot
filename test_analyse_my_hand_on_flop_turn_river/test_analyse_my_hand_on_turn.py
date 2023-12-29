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

    @pytest.mark.parametrize('turn,flush_draw_on_board,nut_flush_num_and_suit', [
        ([[10, 'S'], [7, 'S'], [6, 'H'], [2, 'C']], True, [[14, 'S']]),
        ([[14, 'S'], [9, 'S'], [6, 'H'], [2, 'C']], True, [[13, 'S']]),
        ([[14, 'S'], [13, 'S'], [6, 'H'], [2, 'C']], True, [[12, 'S']]),
        ([[14, 'S'], [13, 'S'], [8, 'H'], [2, 'H']], True, [[12, 'S'], [14, 'H']]),
        ([[14, 'S'], [13, 'C'], [8, 'H'], [2, 'D']], False, []),
        ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.organise_flop', return_value=[[[14, 'S'], [6, 'S'], [6, 'C']], [[14, 'S'], [6, 'S'], [6, 'C']]])
    @mock.patch('flop_turn_river_cards.TheTurn.detect_turn_nums_and_suit', return_value=([8, 'C'], [2, 'S']))
    def test_any_wrap_draw_on_turn(self, mock_detect_turn_nums_and_suit, mock_organise_flop, turn, flush_draw_on_board, nut_flush_num_and_suit):
        amhot = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        expected_flush_draw_on_board = flush_draw_on_board
        expected_nut_flush_num_and_suit = nut_flush_num_and_suit
        actual = amhot.any_flush_draw_on_turn(turn)

        assert actual == (expected_flush_draw_on_board, expected_nut_flush_num_and_suit)


    @pytest.mark.parametrize('turns,num_list,did_board_pair_on_turn,my_hand_rating', [
        # top card paired
        (([[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']], [[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']]), [10, 7, 3, 3, 2, 2], True, 7),
        (([[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']], [[10, 'S'], [10, 'C'], [7, 'C'], [2, 'S']]), [10, 2, 3, 3, 2, 2], True, 5),
        (([[10, 'S'], [10, 'C'], [7, 'C'], [7, 'S']], [[10, 'S'], [10, 'C'], [7, 'C'], [7, 'S']]), [10, 7, 3, 3, 2, 2], True, 7),
        # middle card paired
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [10, 10, 3, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [7, 7, 3, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [10, 7, 3, 3, 2, 2], False, 5),
        (([[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [7, 'C'], [5, 'S']]), [9, 7, 5, 3, 2, 2], False, 5),
        # bottom card paired
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [9, 5, 5, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [10, 10, 5, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [7, 7, 5, 3, 2, 2], False, 7),
        (([[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']], [[10, 'S'], [7, 'C'], [5, 'C'], [5, 'S']]), [10, 7, 5, 3, 2, 2], False, 5),
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

