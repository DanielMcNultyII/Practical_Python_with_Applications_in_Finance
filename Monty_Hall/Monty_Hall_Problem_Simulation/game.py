'''
Daniel McNulty II
Last Modified: 08/14/2018
This file contains the game class for the Monty Hall Problem Simulation
'''


# Import randint from the random module
from random import randint


# The Monty Hall Problem Simulation game class
class MontyHallGame(object):
    # Standard initialization function
    def __init__(self):
        # Initialize an object level prize variable to represent the door behind which there is a prize as an integer
        # between 1 and 3 inclusive. Uses randint to make the door decision "random"
        self.prize = randint(1, 3)

    # door_open function that opens the door that neither the player has not chosen and the prize has not been put
    # behind.
    def door_open(self, player):
        # Initialize a set of all 3 potential doors (1, 2, and 3). Remove the player's initially chosen door and
        # the door with the prize behind it. Then return the door that remains in the difference, and hence represents
        # the door that will be opened, using pop().
        return {1, 2, 3}.difference({player.door, self.prize}).pop()

    # play_game function that simulates the Monty Hall game itself.
    def play_game(self, player):
        # Returns True if player.switch_door_decision(self.door_open(player)) == self.prize and False if it doesn't. The
        # player.switch_door_decision(self.door_open(player)) == self.prize statement checks if the user's chosen door,
        # after they have made the decision on whether to change their door or not, is the door with the prize behind
        # it.
        #   - If the player's chosen door is the door with the prize behind it, they won and return True
        #   - If the player's chosen door is not the door with the prize behind it, they lost and return False
        return True if player.switch_door_decision(self.door_open(player)) == self.prize else False
