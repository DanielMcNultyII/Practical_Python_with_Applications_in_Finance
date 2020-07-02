'''
Daniel McNulty II
Last Modified: 08/14/2018
This file contains the player classes for the Monty Hall Problem Simulation
'''


# Import randint from the random module
from random import randint


# Base class for Players
class Player(object):
    # Standard initialization object
    def __init__(self, player_name='Player', switch=None):
        # Initialize name, door, and switch object level variables for the player.
        #   - name holds the name of the player. Defaults to 'Player' if no name is input
        #   - door holds the door the player initially chooses as an integer between 1 and 3 inclusive. Uses randint to
        #     make the door decision "random"
        #   - switch will holds the player's strategy as to whether they will switch doors when given the opportunity in
        #     the Monty Hall problem (aka When the switch_door_decision() function below is called on the Player object)
        #       > If switch is True, then the player will switch doors.
        #       > If switch is False, then the player will not switch doors.
        self.name = player_name
        self.door = randint(1, 3)
        self.switch = switch

    # switch_door_decision function simulates the Player choosing whether to switch from their initial door decision or
    # not in the Monty Hall problem and returns the door they choose (Whether it is the same door or a door switch)
    def switch_door_decision(self, open_door):
        # If the Player's object level switch variable is True, then switch the player's door variable to the unopened
        # door they did not initially pick.
        if self.switch is True:
            # Initialize a set of all 3 potential doors (1, 2, and 3). Remove the  player's initially chosen door and
            # the currently open door from the doors set. Then set the Player object variable door to the only door in
            # the remaining_door set using pop().
            self.door = {1, 2, 3}.difference({self.door, open_door}).pop()

        # Return the value representing the Player's chosen door stored in the Player object level variable door.
        return self.door


# AlwaysSwitchPlayer class derived from the Player base class that always switches
class AlwaysSwitchPlayer(Player):
    # Standard initialization function
    def __init__(self, player_name):
        # Use super() to call the base class __init__ function. In this case, it will be the Player __init__ function.
        # Pass the input player_name into the Player __init__ function and set the switch input for the Player __init__
        # function to True. This will ensure that the AlwaysSwitchPlayer always switches doors when given the
        # opportunity in the Monty Hall problem.
        super(AlwaysSwitchPlayer, self).__init__(player_name, True)


# NeverSwitchPlayer class derived from the Player base class that never switches
class NeverSwitchPlayer(Player):
    # Standard initialization function
    def __init__(self, player_name):
        # Use super() to call the base class __init__ function. In this case, it will be the Player __init__ function.
        # Pass the input player_name into the Player __init__ function and set the switch input for the Player __init__
        # function to False. This will ensure that the NeverSwitchPlayer never switches doors when given the
        # opportunity in the Monty Hall problem.
        super(NeverSwitchPlayer, self).__init__(player_name, False)
