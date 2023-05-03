import numpy as np
from matplotlib import pyplot as plt

class General_MontyHall_Simulator:
    def __init__(self,
                num_doors: int = 3,
                num_prizes: int = 1,
                num_remove_rounds: int = 1,
                stratergy: str = "switch") -> None:
        
        #assertions so the game can be played properly
        assert num_doors > num_prizes + 1, "Number of doors must be greater than the number of prizes +1"
        assert num_remove_rounds < num_doors - num_prizes, "Number of remove rounds must be less than the number of doors - number of prizes"
        assert num_remove_rounds > 0, "Number of remove rounds must be greater than 0"
        assert stratergy == "switch" or stratergy == "keep", "Stratergy must be either 'switch' or 'keep'"

        self.num_doors = num_doors
        self.door_IDs = np.arange(0,num_doors)
        self.num_prizes = num_prizes
        self.stratergy = stratergy
        self.num_remove_rounds = num_remove_rounds

    #0 = goat, 1 = prize, removed = -1
    def _initalize_door_states(self,num_doors: int, num_prizes: int) -> np.ndarray:
        self.door_states = np.zeros(num_doors)
        #choose random door IDs to be prizes
        prize_door_IDs = np.random.choice(self.door_IDs,num_prizes,replace=False)
        self.prize_doors = prize_door_IDs
        #set door states to 1 if door ID is in prize_door_IDs
        self.door_states[prize_door_IDs] = 1
        return self.door_states
    
    def _remove_door(self,door_ID: int) -> None:
        self.door_states[door_ID] = -1
        return None
    
    def _play_rounds(self):
        #make a player choice
        player_door_ID = np.random.choice(self.door_IDs)
        self.player_door_ID = player_door_ID

        for i in range(self.num_remove_rounds):
            #choose a door to remove that is not the player door or a prize door or has already been removed
            remove_door_ID = np.random.choice(self.door_IDs[(self.door_states != 1) & (self.door_states != -1) & (self.door_IDs != player_door_ID)])
            self._remove_door(remove_door_ID)

            #based on the stratergy, choose a door to switch to or keep
            if self.stratergy == "switch":
                switch_door_ID = np.random.choice(self.door_IDs[(self.door_states != -1) & (self.door_IDs != player_door_ID)])
                self.player_door_ID = switch_door_ID
        #after all rounds have been played, check if the player won
        if self.door_states[self.player_door_ID] == 1:
            return 1
        else:
            return 0
    
    #every time the game is played, the door states are reset along with the player door ID and prize door IDs
    #the return is the win rate of the player
    def __call__(self, repeats: int = 100) -> float:
        win_count = 0
        for i in range(repeats):
            self._initalize_door_states(self.num_doors,self.num_prizes)
            win_count += self._play_rounds()
        return float(win_count/repeats)
    

    @property
    def door_states(self) -> np.ndarray:
        return self._door_states
    @door_states.setter
    def door_states(self,door_states: np.ndarray) -> None:
        self._door_states = door_states
    
    @property
    def prize_doors(self) -> np.ndarray:
        return self._prize_doors
    @prize_doors.setter
    def prize_doors(self,prize_doors: np.ndarray) -> None:
        self._prize_doors = prize_doors

    @property
    def player_door_ID(self) -> int:
        return self._player_door_ID
    @player_door_ID.setter
    def player_door_ID(self,player_door_ID: int) -> None:
        self._player_door_ID = player_door_ID
    

    
if __name__ == "__main__":
    #test what happens as the number of doors increases but the number of prizes stays the same and the number of remove rounds stays the same
    num_door_range = np.arange(3,10)
    num_prizes = 1
    num_remove_rounds = 1
    repeats = 1000
    win_rates_switch = []
    win_rates_keep = []
    for num_doors in num_door_range:
        game_switch = General_MontyHall_Simulator(num_doors,num_prizes,num_remove_rounds,"switch")
        game_keep = General_MontyHall_Simulator(num_doors,num_prizes,num_remove_rounds,"keep")
        win_rates_switch.append(game_switch(repeats=repeats))
        win_rates_keep.append(game_keep(repeats=repeats))

    
    #make a plot of the win rates
    fig, ax = plt.subplots()
    ax.plot(num_door_range,win_rates_switch,label="Choice = Switch")
    ax.plot(num_door_range,win_rates_keep,label="Choice = Keep")
    ax.set_xlabel("Number of Doors")
    ax.set_ylabel("Win Rate")
    ax.set_title("Win Rate vs Number of Doors in the Monty Hall Problem \n with 1 Prize and 1 Remove Round")
    ax.legend(loc="upper right")
    plt.show()


