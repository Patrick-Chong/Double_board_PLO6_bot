1. pot_size() simply prints what is in the pot currenctly. 
(IMPORTANTLY this DOES NOT include what others have currently bet, I have a different function in this script that tells us the action so far)

2. action_behind_me() records what has been bet so far in the current street behind me.

Just like with the other scripts that rely on indexing, this dictionary will have keys that represent the relative position of each player. 
And the values are their bets in the current street. 