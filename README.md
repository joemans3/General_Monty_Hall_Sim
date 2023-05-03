This is a general case for the Monty Hall Problem.

Need:  (will update as a package later)
python3.+
numpy (v.)
matplotlib (v.)

It allows the number of doors, prizes and the number of door removing rounds to be changed.

Running the script as main will do a simple run of the simulation with the option of switching the door choice after removing a goat.
It will repeat this for a range of door values and plot the results of the win rate as a function of the door number.

The class can be used to do other things. Here is the general flow to use this class in another file. 

from PATH_TO_MAIN.PY import General_MontyHall_Simulator

repeats = 1000
game = General_MontyHall_Simulator(num_doors=3, num_prizes=1, num_remove_rounds=1, stratergy="switch")
win_rate = game(repeats)


Note the win rate is a float from 0 to 1.