my_stack.py 

This script takes an image of all of the 6 stack sizes on screen. 

It then resizes the image to simply make it a bit bigger, because the screenshots of the stack sizes 
are quite small and when you run the number reader against it, it reads some of them incorrectly. 
But after resizing them to make them slightly bigger it reads all of them correctly.

The script fills a dictionary called ''stack_tracker'', which is dictionary and will hold the 
stacks of all 6 players, including my own. 
Its keys are the position of the player and the values are the stacks of the players.

It starts with my stack, which is always at the bottom of the screen and will be stack1. 
Then the player directly to my left will have stack2, and so on. 



TO DO: 
1. The cooredinates of the 6 stack sizes need to be changed, becuase I didn't do it while screen mirroring. 

2. I'll also need to passs in my position into the function, and replace some fixed number that I used to 
represent my position for the puspose of making the script work. 