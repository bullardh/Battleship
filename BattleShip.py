# Author: Heather Bullard
# GitHub username: bullardh
# Date: 3/12/2022
# Description: a class called ShipGame that allows two people to play the game Battleship. Each player
#               has their own 10x10 grid they place their ships on. On their turn, they can fire a torpedo
#               at a square on the enemy's grid. Player 'first' gets the first turn to fire a torpedo,
#               after which players alternate firing torpedoes. A ship is sunk when all of its squares
#               have been hit. When a player sinks their opponent's final ship, they win.

# TODO: add docstrings and sunken ships, clean up code,

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


class GameBoard:
    def __init__(self):
        """Takes no parameters. Initializes the gameboard for each player when called"""
        self._first_placement_board = [[" "] * 10 for item in range(10)]
        self._first_guess_board = [[" "] * 10 for item in range(10)]
        self._second_placement_board = [[" "] * 10 for item in range(10)]
        self._second_guess_board = [[" "] * 10 for item in range(10)]
        self._x_row = 0
        self._y_col = 0

    def add_placement_board(self, player, marker, coordinate):
        """ Add the player's ships placement choices to their respective boards
        :param player: current player
        :param marker: the marker designated for each ship
        :param coordinate: the coordinate of the upper leftmost coordinate the player
                chose to place the ship
        :return: true
        """
        coord = ord(coordinate[0]) - 65
        num = int(coordinate[1])
        if player == 'first':
            if self._first_placement_board[coord][num] == " ":
                self._first_placement_board[coord][num] = marker
        if player == 'second':
            if self._second_placement_board[coord][num]:
                self._second_placement_board[coord][num] = marker
        return

    def get_placement_board(self, player):
        """ Retrieve the player's ship placement board
        :param player: the current player
        """
        if player == 'first':
            return self._first_placement_board
        if player == 'second':
            return self._second_placement_board

    def add_guess_board(self, player, marker, coordinate):
        """ Add the player's torpedo launch guesses to their respective board.
        If the torpedo lands in water, the marker is 'w', else it is the marker
        designated in the ship's marker value. The coordinate is the guess location.
        :param player: current player
        :param marker: the marker designated for each ship
        :param coordinate: the coordinate of the torpedo launched by the player
        :return: true
        """
        coord = ord(coordinate[0]) - 65
        num = int(coordinate[1])
        if player == 'first':
            self._first_guess_board[coord][num] = marker
        if player == 'second':
            self._second_guess_board[coord][num] = marker
        return

    def get_guess_board(self, player):
        """ Retrieve the player's guess board for their torpedo launch
        :param player: the current player
        """
        if player == 'first':
            return self._first_guess_board
        if player == 'second':
            return self._second_guess_board

    def create_board(self) -> list[list[str]]:
        """Creates game boards in a 10x10 grid with empty spaces. Takes no parameters"""
        self._board = [[" "] * 10 for item in range(10)]
        return self._board

    def print_board(self, board):
        """Each time the player makes a guess the program prints the board
        :param board: prints the board for the specific player
        """
        print(" A B C D E F G H I J")
        print(" +-+-+-+-+-+-+-+-+-+")
        row_num = 1
        for row in board:
            print("%d|%s|" % (row_num, "|".join(row)))
            row_num += 1
        return


class Ships:
    def __init__(self):
        """ Takes no parameters and initializes data members pertaining to the player's ships"""
        self._ships = {"carrier": {"marker": "c", "length": 5, "orientation": "", "position": "", "placed": [], "sunk": False},
                       "battleship": {"marker": "b", "length": 4, "orientation": "", "position": "", "placed": [], "sunk": False},
                       "cruiser": {"marker": "r", "length": 3, "orientation": "", "position": "", "placed": [], "sunk": False},
                       "submarine": {"marker": "s", "length": 3, "orientation": "", "position": "", "placed": [], "sunk": False},
                       "destroyer": {"marker": "d", "length": 2, "orientation": "", "position": "", "placed": [], "sunk": False}}
        self._first_ships = self._ships
        self._second_ships = self._ships
        self._first_sunk_count = 0
        self._second_sunk_count = 0
        self._first_placed_count = 0
        self._second_placed_count = 0

    def get_first_ships(self):
        """Retrieves the ship's dictionary for the first player. Takes no parameters"""
        return self._first_ships

    def get_second_ships(self):
        """Retrieves the ship's dictionary for the second player. Takes no parameters"""
        return self._second_ships

    def add_ship_orientation(self, player, ship, orient):
        """Add the ship's placement orientation for each player's choices
        :param player: current player
        :param ship: the ship the player wants to place
        :param orient: the orientation, either R for horizontal or C for vertical
        :return: true"""
        if orient == 'R' or orient == 'C':
            if player == 'first':
                self._first_ships[ship]["orientation"] = orient
            else:
                self._second_ships[ship]["orientation"] = orient
        return

    def add_ship_position(self, player, ship, posit):
        """Add the ship's placement starting position for each player's choices
        :param player: current player
        :param ship: the ship the player wants to place
        :param posit: states which uppermost left column and row the ship will occupy
        :return: true"""
        if player == 'first':
            self._first_ships[ship]["position"] = posit
        else:
            self._second_ships[ship]["position"] = posit
        return True

    def verify_empty(self, player, ship, orient, position):
        """
        Validates the placement of ships to make sure they are valid moves
        :param player: current player
        :param ship: the ship the player wants to place
        :param orient: the orientation, either R for horizontal or C for vertical
        :param position: states which uppermost left column and row the ship will occupy
        :return: variable 'verify' either true if all the spaces are empty and on the board, else false
        """
        verify = True
        board = GameBoard()
        ships = Ships()
        board.print_board(player)
        new_letter = ord(position[0]) - 65
        new_num = int(position[1])
        if orient == 'R' and ((new_num + ships.get_ship_length(ship)) < 10):
            for item in range(ships.get_ship_length(ship)):
                if board.get_placement_board(player)[item+new_letter][new_num] != " ":
                    verify = False
        if orient == 'C' and ((new_letter + ships.get_ship_length(ship)) < 10):
            for item in range(ships.get_ship_length(ship)):
                if board.get_placement_board(player)[new_letter][item+new_num] != " ":
                    verify = False
        return verify

    def add_ship_placed(self, player, ship, direction, coord):
        """ Validate each of the ships have not already been added to the player's placement board
        and that the coordinates do not cause the length of the ship to extend out of bounds
        :param player: current player
        :param ship: the ship
        :param direction: the orientation, either R for horizontal or C for vertical
        :param coord: the upper leftmost coordinates of the ship placed
        :return: true
        """
        board = GameBoard()
        if Ships.get_ship_placed_count(self, player) == 5:
            GamePlay.error_message(f"All ships are placed for {player}!")
            return
        if player == 'first':
            ships = self._first_ships[ship]
        else:
            ships = self._second_ships[ship]

        letter, num = ord(coord[0]), int(coord[1])
        empty = Ships.verify_empty(self, player, ship, direction, coord)
        if empty is False:
            print("Ship Error: placement occupied or placement off the board")
            return
        ships["position"].append(coord)
        for item in range(ships["length"]):
            if ships["orientation"] == 'R':
                letter += 1  # add letters
                new_coord = f'{chr(letter)}{coord[1]}'
                ships["placed"].append(new_coord)
                board.add_placement_board(player, ships["marker"], new_coord)

            if ships["orientation"] == 'C':
                num += 1
                new_coord = f'{coord[0]}{num}'
                ships["placed"].append(new_coord)
                board.add_placement_board(player, ships["marker"], new_coord)
        self.add_ship_placed_count(player)
        return

    def add_ship_placed_count(self, player):
        """ Keep track of each player's ships that have been placed
        :param player: the current player
        """
        if player == 'first':
            self._first_placed_count += 1
            return self._first_placed_count
        else:
            self._second_placed_count += 1
            return self._second_placed_count

    def get_ship_placed_count(self, player):
        """Retrieve each of the player's current count for the number of ships placed
        :param player: the current player
        """
        if player == 'first':
            return self._first_placed_count
        else:
            return self._second_placed_count

    def get_ship_marker(self, ship):
        """Retrieve each of the ships' abbreviated term for placement
        :param ship: the ship name listed as a key"""
        return self._ships[ship]["marker"]

    def get_ship_length(self, ship):
        """Retrieves each of the ships' lengths
        :param ship: the ship's name listed as a key"""
        return self._ships[ship]["length"]

    def get_ship_coordinates(self, player, ship):
        """Retrieves each of the ships' coordinates for a specific player
        :param player: the current player
        :param ship: the ship's name listed as a key
        """
        if player == 'first':
            return self._first_ships[ship]['placed']
        else:
            return self._second_ships[ship]['placed']

    def get_ship_orientation(self, player, ship):
        """Retrieves each of the ships' orientation
        :param player: the current player
        :param ship: the ship's name listed as a key
        """
        if player == 'first':
            return self._first_ships[ship]["orientation"]
        else:
            return self._second_ships[ship]["orientation"]

    def add_first_sunk(self):
        """Adds one to the First player Sunk Ship Count. Takes no parameters"""
        self._first_sunk_count += 1
        return

    def get_first_sunk(self):
        """Retrieves the First Player's Sunk Ship Count. Takes no parameters"""
        return self._first_sunk_count

    def add_second_sunk(self):
        """Adds one to the Second Player's Sunk Ship Count. Takes no parameters"""
        self._second_sunk_count += 1
        return

    def get_second_sunk(self):
        """Retrieves the Second Player's Sunk Ship Count. Takes no parameters"""
        return self._second_sunk_count


class GamePlay:
    """Inherits board. allows two people to play the game Battleship. Each player has their own 10x10 grid they place their ships on.
        On their turn, they can fire a torpedo at a square on the enemy's grid. Player 'first' gets the first turn to
        fire a torpedo, after which players alternate firing torpedoes. A ship is sunk when all of its squares have been
        hit. When a player sinks their opponent's final ship, they win."""
    def __init__(self):
        """
        Takes no parameters. Initializes data members for the placement game boards and the guess boards for
        each player, players_turn, and the game_state
        """
        self._first_placement_board = GameBoard.create_board
        self._first_guess_board = GameBoard.create_board
        self._second_placement_board = GameBoard.create_board
        self._second_guess_board = GameBoard.create_board
        self._players_turn = 'first'
        self._game_state = "UNFINISHED"

    @staticmethod
    def error_message(message):
        """
        Prints a unique error message
        :param message: the error message
        """
        print(f"{message}")
        return

    def placing_ships(self, player, ship, coordinate, orientation):
        """ Takes 4 parameters and places the ship on the player's board
        :param player: current player
        :param ship: the ship
        :param orientation: the orientation, either R for horizontal or C for vertical
        :param coordinate: the upper leftmost coordinates of the ship placed
        :return: true"""
        ships = Ships()
        play = GamePlay()
        if player == self._players_turn:
            if player == 'first':
                if ship not in ships.get_first_ships().keys:
                    play.error_message(f"Wrong Ship! {ship} is not a correct ship")
                    return

            if player == 'second':
                if ship not in ships.get_second_ships().keys:
                    return play.error_message(f"Wrong Ship! {ship} is not a correct")
            ships.add_ship_placed(player, ship, orientation, coordinate)
            ships.add_ship_orientation(player, ship, orientation)

            return
        else:
            return play.error_message(f"Wrong Player! It is not {player}'s turn yet")

    def launching_torpedoes(self, player, coordinates):
        """
        Takes the parameters for the player and the coordinates and validates that guess has bot been
        previously said.
        :param player: the current player
        :param coordinates: The coordinates guessed by the player to try to find the other player's ships.
        """
        ships = Ships()
        board = GameBoard()
        catch_marker = ""
        if player != self._players_turn:
            GamePlay.error_message(f"Wrong Player! It is not {player} player's turn!")
            return
        new_letter = ord(coordinates[0]) - 65
        new_num = int(coordinates[1])
        if board.get_guess_board(player)[new_letter][new_num] != " ":
            GamePlay.error_message("Already Launched Torpedo Here! Try Again!")
            return
        if board.get_placement_board(player)[new_letter][new_num] == " ":
            board.add_guess_board(player, "w", coordinates)

        catch_marker = board.get_placement_board(player)[new_letter][new_num]
        board.add_guess_board(player, catch_marker, coordinates)

        # add checking for sunk ship based on catch_marker
        # if ship sinks, add 1 to player's sunken wins which keeps track of the number of sunken ships the player has sunk of the opponents fleet.
        # check if number of sunken ships equals total number of ships, if so change status to the player won, print message, exit
        # else, next player's turn to launch a torpedo, repeat until one player's ships have all been sunk.






game = GamePlay()
game.placing_ships('first', 'carrier', 'A5', 'R')
game.placing_ships('second', 'submarine', 'B1', 'C')
game.placing_ships('first', 'submarine', 'C1', 'C')
game.placing_ships('second', 'carrier', 'D4', 'C')
game.placing_ships('first', 'cruiser', 'A9', 'R')
game.placing_ships('second', 'cruiser', 'F4', 'R')
game.placing_ships('first', 'destroyer', 'J7', 'C')
game.placing_ships('second', 'destroyer', 'E4', 'C')
game.placing_ships('first', 'battleship', 'A1', 'C')
game.placing_ships('second', 'battleship', 'H1', 'C')
