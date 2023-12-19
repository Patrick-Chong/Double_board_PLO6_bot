num_of_players_in_pot script takes a pic of all 6 positions of the players, including myself and sees if there is a 'Fold' sign. 

The dictionary entry will look something like: {1: True, 2: False, 3: True, 4: True, 5: True, 6: False}

Which indicates UTG player has folded, UTG + 1 has NOT folded, etc. 
(i.e. if it is True that means that player in that position HAS FOLDED!!)
