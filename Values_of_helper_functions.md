Values of each of the useful functions: 

1. @pot size - returned as a float 
2. @action_behind_me - will have values 'Fold', 'Empty', or the float of whatever opps bet
3. @SPR_tracker - 'False' if folded or empty seat otherwise holds float of whatever the SPR is of the player
4. @guy_to_right_bet_size - 0 if checked to me otherwise float of whatever the last guy bet 
5. @positions_of_players_to_act_ahead_of_me - list of positions of players yet to act ahead of me
6. @limped_or_3_bet_to_me - returns a float, either 'Check', 'bet', 'three_bet' or 'four_bet'
7. @fold_tracker - Boolean; checks if seat is empty too, if it is, then True is marked for that seat
8. @stack_tracker - float; dictionary of each position's stack
9. @limped_or_3_bet_to_me_pre_flop - 'limped', 'bet', 'three_bet', 'four_bet'
