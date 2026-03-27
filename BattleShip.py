# Author: Heather Bullard
# GitHub username: bullardh
# Date: 9/14/2025
# Description: a class called ShipGame that allows two people to play the game Battleship. Each player
#               has their own 10x10 grid they place their ships on. On their turn, they can fire a torpedo
#               at a square on the enemy's grid. Player 'first' gets the first turn to fire a torpedo,
#               after which players alternate firing torpedoes. A ship is sunk when all of its squares
#               have been hit. When a player sinks their opponent's final ship, they win.
import itertools
import pandas as pd

# TODO: add docstrings and sunken ships, clean up code,
import random

"""
        BATTLESHIP
        1. Each Player secretly arranges 5 ships on a 10x10 grid
            a. ships occupy a number of consecutive squares (horizontal or vertical)
                i. carrier -> 5 spaces
                ii. battleship -> 4 spaces
                iii. cruiser -> 3 spaces
                iv. submarine -> 3 spaces
                v. destroyer-> 2 spaces
            b. the ships' placement is validated for occupied spaces or out of bound spaces
        2. Each Player takes turns
            a. if ship is hit, print hit or miss
            b. on a different marking board, each attacking player keeps track of the hits, misses and ships sunk
            c. each receiving player marks hits or misses on their own ships
            d. when all the squares of ship is hit, print player ship sunk
            e. update the player's ship count
            f. win count is zero then attacking player wins
"""


class Ships:
    """Keeps track of ship's size, the number of hits, and sunk logic"""
    def __init__(self, name, size):
        """ Takes no parameters and initializes data members pertaining to the player's ships"""
        self._name = name
        self._size = size
        self._positions = set()
        self._hits = set()

    def place(self, start_row, start_col, horizontal, board_size):
        """Place ship in given orientation if valid, return set of coordinates or None."""
        coords = set()
        for i in range(self._size):
            r = start_row + (0 if horizontal else i)
            c = start_col + (i if horizontal else 0)
            if not (0 <= r < board_size and 0 <= c < board_size):
                return None
            coords.add((r, c))
        self._positions = coords
        return coords

    def hit(self, row, col):
        """Register hit if this ship occupies (row, col)."""
        pos = (row, col)
        if pos in self._positions:
            self._hits.add(pos)
            return True
        return False

    def is_sunk(self):
        return self._positions == self._hits

    def get_positions(self):
        return self._positions.copy()

    def get_name(self):
        return self._name


class GameBoard:
    """Creates the Board grid. Keeps track of ship placement and attacks."""
    def __init__(self, size=10):
        """Takes no parameters. Initializes the gameboard for each player when called"""
        self._size = size
        self._ships = []
        self._occupied = set()
        self._hits = set()
        self._misses = set()

    # --- Encapsulation helpers ---
    def get_size(self):
        return self._size

    def display_board(self, reveal=False):
        """Displays board, reveal=True, shows ships for debug"""
        for r in range(self._size):
            row = []
            for c in range(self._size):
                pos = (r, c)
                if pos in self._hits:
                    row.append("X")   # hit
                elif pos in self._misses:
                    row.append("O")   # miss
                elif reveal and pos in self._ships:
                    row.append("S")   # ship
                else:
                    row.append(".")
            print(" ".join(row))
        print()

    def place_ship(self, ship, start_row, start_col, horizontal):
        """Place ship at given coordinates, if valid"""
        coords = ship.place(start_row, start_col, horizontal, self._size)
        if coords is None:
            return "Out of Bounds"
        if any(pos in self._occupied for pos in coords):
            return "Overlap"
        self._ships.append(ship)
        self._occupied |= coords
        return "Placed"

    def fire(self, row, col):
        """Player fires at coordinate, returns result"""
        pos = (row, col)
        if pos in self._hits or pos in self._misses:
            return "Invalid" # Already fired
        for ship in self._ships:
            if ship.hit(row, col):
                self._hits.add(pos)
                if ship.is_sunk():
                    return f'Sunk {ship.get_name()}'
                return "Hit"
        self._misses.add(pos)
        return "Miss"

    def is_defeated(self):
        """Check if all ships are destroyed"""
        return all(ship.is_sunk() for ship in self._ships)


class GamePlay:
    """Keeps track of game loop and win condition. Inherits board. allows two people to play the game Battleship. Each player has their own 10x10 grid they place their ships on.
        On their turn, they can fire a torpedo at a square on the enemy's grid. Player 'first' gets the first turn to
        fire a torpedo, after which players alternate firing torpedoes. A ship is sunk when all of its squares have been
        hit. When a player sinks their opponent's final ship, they win."""
    def __init__(self, size=10, vs_computer=True):
        """
        Takes no parameters. Initializes data members for the placement game boards and the guess boards for
        each player, players_turn, and the game_state
        """
        self._boards = {
            "Player 1": GameBoard(size),
            "Player 2": GameBoard(size)
        }
        self._turns = itertools.cycle(["Player 1", "Player 2"])
        self._current_player = next(self._turns)
        self._vs_computer = vs_computer
        self._fleet = [
            ("carrier", 5),
            ("battleship", 4),
            ("cruiser", 3),
            ("submarine", 3),
            ("destroyer", 2)
        ]

        self._game_state = "UNFINISHED"

    @staticmethod
    def error_message(message):
        """
        Prints a unique error message
        :param message: the error message
        """
        print(f"{message}")
        return

    def setup_phase(self):
        """ Let both players place their ships before game starts.
        Takes 4 parameters and places the ship on the player's board
        """
        for player in ["Player 1", "Player 2"]:
            print(f'\n{player}, place your fleet.')
            for name, size in self._fleet:
                placed = False
                while not placed:
                    if player == "Player 2" and self._vs_computer:
                        # Computer randomly places ships
                        row = random.randint(0, self._boards[player].get_size() - 1)
                        col = random.randint(0, self._boards[player].get_size() - 1)
                        horizontal = random.choice([True, False])
                    else:
                        try:
                            row = int(input(f'{name} (size {size}) - Enter start row: '))
                            col = int(input(f'{name} (size {size}) - Enter start col: '))
                            orientation = input("Horizontal? (y/n): ").strip().lower()
                            horizontal = orientation == "y"
                        except ValueError:
                            print("Invalid input. Try Again")
                            continue

                    ship = Ships(name, size)
                    result = self._boards[player].place_ship(ship, row, col, horizontal)
                    if result == "Placed":
                        placed = True
                        print(f"{name} placed ")
                    elif result == "Out of Bounds":
                        if player != "Player 2":  # Don't spam for computer
                            print("Out of Bounds. Try again.")
                    elif result == "Overlap":
                        if player != "Player 2":
                            print("Overlaps with another ship. Try again.")
                # Computer retries automatically

            if player != "Player 2" or not self._vs_computer:
                print(f"{player}'s board (debug view):")
                self._boards[player].display_board(reveal=True)

    def play(self):
        self.setup_phase()
        while True:  # Loop ends via return, no break
            opponent = "Player 2" if self._current_player == "Player 1" else "Player 1"
            print(f"\n{self._current_player}'s turn to fire at {opponent}'s board!")

            # show current board state before firing
            print(f"\n{opponent}'s board (current view):")
            self._boards[opponent].display_board(reveal=False)

            if self._current_player == "Player 2" and self._vs_computer:
                row = random.randint(0, self._boards[opponent].get_size() - 1)
                col = random.randint(0, self._boards[opponent].get_size() - 1)
                print(f"Computer fires at ({row}, {col})")
            else:
                try:
                    row = int(input("Enter row: "))
                    col = int(input("Enter col: "))
                except ValueError:
                    print("Invalid input. Numbers only.")
                    self._current_player = next(self._turns)
                    continue

            result = self._boards[opponent].fire(row, col)
            print(result)
            print(f"\nUpdated {opponent}'s board:")
            self._boards[opponent].display_board(reveal=False)

            if self._boards[opponent].is_defeated():
                print(f"\n🎉 {self._current_player} WINS! All ships destroyed! 🎉")
                return

            self._current_player = next(self._turns)

# ----------------------------------------
# Player works fine do not change for now
# ----------------------------------------


class Player:
    """The class Player owns the board and keeps track of turns."""
    def __init__(self):
        self._player_choice = {"first": "First Player", "second": "Second Player"}
        self._current_player = self._player_choice["first"]

    def get_current_player(self):
        return self._current_player

    def change_player(self, player):
        if player != self._current_player and self._player_choice.get(player) is not None:
            self._current_player = self._player_choice.get(player)
        return self._current_player


if __name__ == "__main__":
    game = GamePlay(size=10, vs_computer=True)
    game.play()


        # add checking for sunk ship based on catch_marker
        # if ship sinks, add 1 to player's sunken wins which keeps track of the number of sunken ships the player has sunk of the opponents fleet.
        # check if number of sunken ships equals total number of ships, if so change status to the player won, print message, exit
        # else, next player's turn to launch a torpedo, repeat until one player's ships have all been sunk.

    game.setup_phase()

