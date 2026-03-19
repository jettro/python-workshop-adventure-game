import random

from enum import Enum
from dataclasses import dataclass

class Compass(Enum):
    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    SOUTH_EAST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    NORTH_WEST = 7
    HERE = 8

class Move(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

@dataclass
class Character:
    """A character that can be placed on the board. It contains a point value and a message."""
    points: int
    message: str

@dataclass
class CharacterLocation:
    """The location of a character on the board."""
    location: tuple[int, int]
    character: Character

def random_location(width: int = 10,
                      height: int = 10,
                      occupied: list[tuple[int, int]] = None,
                      max_retries: int = 100) -> tuple[int, int]:
    occupied_set = set(occupied) if occupied else set()

    for _ in range(max_retries):
        new_random = (
            random.randint(0, height - 1),
            random.randint(0, width - 1)
        )
        if new_random not in occupied_set:
            return new_random

    raise RuntimeError(f"Could not find an empty location on the board after {max_retries} retries.")

class MoveResultType(Enum):
    SUCCESS = "success"
    OUT_OF_BOUNDS = "out_of_bounds"
    CHARACTER_FOUND = "character_found"
    EXIT_FOUND = "exit_found"


@dataclass
class MoveResult:
    """
    Represents the result of a move. Each move result has a type, location, and the character.
    The type is a MoveResultType representing the type of the move result. The location is a tuple of type int.
    The character is an instance of the Character class.
    """
    type: MoveResultType
    location: tuple[int, int]
    character: Character = None


class Board:
    def __init__(self, characters: list[Character] = None, height: int = 10, width: int = 10):
        self.height = height
        self.width = width
        self.character_locations = []

        for character in characters:
            occupied = [char_loc.location for char_loc in self.character_locations]
            new_location = random_location(width=width, height=height, occupied=occupied)
            self.character_locations.append(CharacterLocation(new_location, character))

        occupied = [char_loc.location for char_loc in self.character_locations]
        self.start_location = random_location(width, height, occupied)
        occupied.append(self.start_location)
        self.end_location = random_location(width, height, occupied)
        self.player_location = self.start_location

    def move_player(self, move: Move) -> MoveResult:
        if not self._validate_move(move):
            return MoveResult(MoveResultType.OUT_OF_BOUNDS, self.player_location)

        # Find the new location and return the success response.
        self.player_location = self._new_location(move)

        if self._check_for_exit():
            return MoveResult(MoveResultType.EXIT_FOUND, self.player_location)
        found_character = self._check_for_character()
        if found_character:
            return MoveResult(MoveResultType.CHARACTER_FOUND, self.player_location, found_character)

        return MoveResult(MoveResultType.SUCCESS, self.player_location)

    def get_compass_direction(self) -> Compass:
        """
        Calculates the compass direction from the current location to the end location.
        :return: The compass direction as an instance of the Compass enum.
        """
        curr_r, curr_c = self.player_location
        end_r, end_c = self.end_location

        dr = end_r - curr_r
        dc = end_c - curr_c

        if dr > 0:  # Southward
            if dc > 0:
                return Compass.SOUTH_EAST
            elif dc < 0:
                return Compass.SOUTH_WEST
            else:
                return Compass.SOUTH
        elif dr < 0:  # Northward
            if dc > 0:
                return Compass.NORTH_EAST
            elif dc < 0:
                return Compass.NORTH_WEST
            else:
                return Compass.NORTH
        else:  # Same row
            if dc > 0:
                return Compass.EAST
            elif dc < 0:
                return Compass.WEST
            else:
                # Default case if location is exactly the end_location
                return Compass.HERE

    def _validate_move(self, direction: Move) -> bool:
        """
        Checks if the move is valid based on the current location and the direction.
        :param direction: direction to move
        :return: true if the move is valid, false otherwise
        """
        if direction == Move.NORTH:
            return self.player_location[0] - 1 >= 0
        if direction == Move.EAST:
            return self.player_location[1] + 1 < self.width
        if direction == Move.SOUTH:
            return self.player_location[0] + 1 < self.height
        if direction == Move.WEST:
            return self.player_location[1] - 1 >= 0

        return False

    def _new_location(self, direction: Move) -> tuple[int, int]:
        if direction == Move.NORTH:
            return self.player_location[0] - 1, self.player_location[1]
        if direction == Move.EAST:
            return self.player_location[0], self.player_location[1] + 1
        if direction == Move.SOUTH:
            return self.player_location[0] + 1, self.player_location[1]
        if direction == Move.WEST:
            return self.player_location[0], self.player_location[1] - 1
        return self.player_location

    def _check_for_exit(self) -> bool:
        return self.player_location == self.end_location

    def _check_for_character(self) -> Character | None:
        for char_loc in self.character_locations:
            if char_loc.location == self.player_location:
                return char_loc.character
        return None

    def print_board_info(self):
        print(f"Board dimensions: {self.width} x {self.height}")
        print(f"Number of characters: {len(self.character_locations)}")
        print(f"Characters on board: {[char_loc.location for char_loc in self.character_locations]}")
        print(f"Start location: {self.start_location}")
        print(f"End location: {self.end_location}")

# Assignments 0
def init_board():
    """Only used in the beginning of the assignment."""
    print("Hello from board!")

def sum_numbers(a: int, b: int) -> int:
    """Sums two numbers, only to demonstrate testing."""
    return a + b