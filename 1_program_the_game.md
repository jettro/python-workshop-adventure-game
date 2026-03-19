# Program the game

In this exercise, you will program a game. You start with the domain classes: Character, CharacterLocation, Compass, Move, Board and Game. You create a game board with a length and height. The board is a game board like checkers or chess. You are dropped somewhere on the board and need to navigate to the exit. You can move North, East, South, or West. You move one location at a time. Each move costs you one point of health. You start with 10 health points, reaching the end gives you a bonus. With each move, you can run into other characters. Some of them are friendly and give you a bonus, others are hostile and take away health points.

## Enums for Compass and Move

The compass is a tool that helps you navigate. If you have seen the _Pirates of the Caribbean_, you know this devise. It points to what you want most, for the game, it points to the direction of the exit.

You need to create a compass enum that has eight directions and the _Here_ when you are on the exit location. Below is the start of the compass enum. Finish it in you own code base by adding North east, South east, South west, and North west. You can add it to the board.py class from the previous section.

```python
from enum import Enum

class Compass(Enum):
    NORTH = 0
    EAST = 2
    SOUTH = 4
    WEST = 6
    HERE = 8
```
If you are interested in the Enum class, you can read more about it here: [Python docs Enum class]( https://docs.python.org/3/library/enum.html). The Enum class is a good fit, it has only constant instances without any methods.

Next, create the Move class. Again an enum is the way to go. This time with 4 values, NORTH, EAST, SOUTH and WEST.

### Assignments
- Create and finish the compass enum
- Create the Move enum

## @dataclass for Character and CharacterLocation
Dataclasses are a way to create classes that have attributes. By adding the annotation, the class becomes a dataclass. A default _init_ method is created automatically. You can add additional methods to the class like a to_json for instance. 

If you want to learn more about dataclasses, you can read more about them here: [Python docs dataclass]( https://docs.python.org/3/library/dataclasses.html).

Create the dataclass for Character and CharacterLocation. Notice the use of types. The _Tuple_ works like a coordinate in a game board. The top left field is 0,0. We prefer to type the parameters of the dataclass.

```python
from dataclasses import dataclass

@dataclass
class Character:
    """A nice description of the character class"""
    points: int
    message: str

@dataclass
class CharacterLocation:
    """A nice description of the character location class"""
    location: tuple[int, int]
    character: "<what should go here?>"
```
### Assignments
- Create the Character dataclass
- Create the CharacterLocation dataclass

## Implement the Board
Create a board class that has a width and height. Next to the width and height, pass the characters to put on the board. Each character gets a random location on the board, just like the start location of the player, and the exit location.

```python
class Board:
    def __init__(self, characters: list[Character] = None, height: int = 10, width: int = 10):
        self.height = height
        self.width = width
        self.character_locations = []
```

Next we want to put all the provided characters on the board at a random location. An important requirement, each location can host one character at a time. Use the next utility function to find a random location on the board that is not yet occupied.

```python
import random

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
```

This is a utility function for the board. Can you write a test for it? You can use the pytest library to write tests. Check if a new location is within the board boundaries. Check with occupied locations. Think about the number of valid locations versus the amount of occupied locations how many retries are needed to guarantee a new location.

If you have a hard time with the tests, check the tips at the bottom of the page.

Next, you have to loop over all the provided characters, find the current occupied locations, ask for a new location using the utility function, and add the character to the board by appending it to the character_locations list. To check your Board, implement a print_board_info method that prints information about the board. You can use the method below to print the board.

Again, the tips at the bottom of the page can help you with the iteration if you need it.

```python
def print_board_info(self):
    print(f"Board dimensions: {self.width} x {self.height}")
    print(f"Number of characters: {len(self.character_locations)}")
    print(f"Characters on board: {[char_loc.location for char_loc in self.character_locations]}")
```

Next, change the init_board function to create a board with some characters and run the script main.py just like before. You can use this code to initialise the board.

```python
board = Board(characters=[
    Character(points=1, message="You found a key!"),
    Character(points=-2, message="You stepped into a puddle of muddy water!"),
    Character(points=-1, message="You hit a wall!"),
    Character(points=-1, message="You hit a monster!"),
    Character(points=5, message="You found a gem")
], height=10, width=10)
```

### Assignments
- Implement the board class, use the random_location function to put all the characters on the board.
- Write a test for the random_location function in the test_game.py file.
- Implement a print_board method to print information about the size of the board and what is on the board.
- Change the start_game function to create a board with some characters and run the script main.py just like before.

If everything went well, you should see an output like this:

```
Board dimensions: 10 x 10
Number of characters: 5
Characters on board: [(5, 2), (0, 6), (4, 6), (9, 3), (1, 5)]
```

## Create start position and exit location
You can reuse the random_location function to find a random location on the board that is not yet occupied for the start position and the exit location. The next code block shows how to do this. Add this block to the init method of the Board class. Extend the print method to print the start and exit locations.

```python
occupied = [char_loc.location for char_loc in self.character_locations]
self.start_location = random_location(width, height, occupied)
occupied.append(self.start_location)
self.end_location = random_location(width, height, occupied)
self.player_location = self.start_location
```

### Assignments
- Add the random start and exit locations to the board.
- Print the start and exit locations in the print_board method.

The output of the script should look like this:

```
Board dimensions: 10 x 10
Number of characters: 5
Characters on board: [(5, 8), (6, 8), (7, 8), (4, 9), (1, 8)]
Start location: (6, 9)
End location: (1, 4)
```
## Move the player
You implement the move method in the Board class. There are four moves possible: NORTH, EAST, SOUTH and WEST. You have to validate the move and check if the move is valid. The player cannot move outside the board. If the move is valid, move the player to the new location.

Each move returns a MoveResult response. The response contains the type of the response, the location of the player, and the found character (optional). Implement the move method in the Board class. For now validate the move, if the move is valid, return the new location of the player. If the move is not valid, return the current location of the player.

```python
class MoveResultType(Enum):
    SUCCESS = "success"
    OUT_OF_BOUNDS = "out_of_bounds"
    CHARACTER_FOUND = "character_found"
    EXIT_FOUND = "exit_found"


@dataclass
class MoveResult:
    character: Character = None
    # Finish this class with a type and a location attribute. 
```

These methods help you with the implementation, add them to the Board class.

```python
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
```

```python
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
```

This is the beginning of the move method.

```python
def move_player(self, move: Move) -> MoveResult:
    if not self._validate_move(move):
        return MoveResult(MoveResultType.OUT_OF_BOUNDS, self.player_location)

    # Find the new location and return the success response.
```

You are now able to move the player around the board. Add some moves to the main method of the script. Print the result of a move.

### Assignments
- Add the MoveResultType enum.
- Add the MoveResult class.
- Implement the move method in the Board class. Use the _validate_move and _new_location methods.
- Add some moves to the main method of the script. Move North until you are out of bounds.

## Enhance the move with finding the exit or a character
The move method is now able to move the player around the board. You can now add some logic to find the exit or a character. If the player reached a new location, check if there is a character on that location or if the location is the exit location. Use the methods below to find the character or the exit location and change the result of the move accordingly.

```python
def _check_for_exit(self) -> bool:
    return self.player_location == self.end_location

def _check_for_character(self) -> Character | None:
    for char_loc in self.character_locations:
        if char_loc.location == self.player_location:
            return char_loc.character
    return None
```

Think about a way to test this logic. I added a loop and kept moving north until I find the exit or I get an out of bounds error.

```python
board.print_board_info()
do_exit = False
while not do_exit:
    result = board.move_player(Move.NORTH)
    print(result)
    do_exit = result.type == MoveResultType.EXIT_FOUND or result.type == MoveResultType.OUT_OF_BOUNDS
```
The output of the script should look like this:

```
Board dimensions: 10 x 10
Number of characters: 5
Characters on board: [(1, 1), (2, 2), (6, 9), (8, 0), (3, 1)]
Start location: (4, 0)
End location: (4, 1)
MoveResult(type=<MoveResultType.SUCCESS: 'success'>, location=(3, 0), character=None)
MoveResult(type=<MoveResultType.SUCCESS: 'success'>, location=(2, 0), character=None)
MoveResult(type=<MoveResultType.SUCCESS: 'success'>, location=(1, 0), character=None)
MoveResult(type=<MoveResultType.SUCCESS: 'success'>, location=(0, 0), character=None)
MoveResult(type=<MoveResultType.OUT_OF_BOUNDS: 'out_of_bounds'>, location=(0, 0), character=None)
```

### Assignments
- Add the _check_for_exit and _check_for_character methods to the Board class.
- Add some logic to the move method to check for the exit or a character.
- Run the script and see if you can find the exit or a character.

## Get a tip using the compass
To make searching for the exit easier, you implement the compass functionality. The compass is a tool that helps you navigate by pointing to the exit. Below is the compass method. Add it to the Board class.

```python
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
```
Can you rewrite the main part of the script to use the compass and find the exit? Be carefull to not run into the infamous infinite loop.

### Assignments
- Add the compass method to the Board class.
- Rewrite the main part of the script to use the compass.

The tips section contains a tip to find the exit using the compass.

## Create a Game class
The Game class is the main class that will be used to run the game. You use the board to play, but now you add a score to the game.

Create the Game class in game.py. In the init method, create the board with characters, height, and width.

```python
import uuid

class Game:
    game_id: str = str(uuid.uuid4())
    finished: bool = False
    score: int = 100
    
    def __init__(self):
        # Implement the init method here.
        pass
```    

Now implement the run method that accepts input from the user from the terminal to move the player around the board. Below is the method.

```python
def run(self):
    directions = {
        "N": Move.NORTH,
        "E": Move.EAST,
        "S": Move.SOUTH,
        "W": Move.WEST
    }
    while not self.finished:
        user_input = input("Enter direction (N, E, S, W) or Q to quit: ").strip().upper()
        if user_input == "Q":
            break

        if user_input in directions:
            move_result = self.board.move_player(directions[user_input])
            if move_result.type == MoveResultType.EXIT_FOUND:
                print("*** Yes you found the exit! Congratulations!")
                self.finished = True
            elif move_result.type == MoveResultType.CHARACTER_FOUND:
                print(f"You found a character, this is its message: `{move_result.character.message}`!")
            elif move_result.type == MoveResultType.OUT_OF_BOUNDS:
                print("You are at the end of the board!")
            elif move_result.type == MoveResultType.SUCCESS:
                compass = self.board.get_compass_direction()
                print(f"The exit is in the {compass.name} direction.")
            else:
                print("Unknown move result type!")
        else:
            print("Invalid input! Please enter N, E, S, W, or Q.")
```

you can run the game by changing the main method to the following.

```python
if __name__ == "__main__":
    game = Game()
    game.run()
```

### Assignments
- Create the Game class.
- Implement the run method.
- Run the script and play the game.

## Add a scoring mechanism to the game
The game is now playable, but it does not have a scoring mechanism. You will implement the following rules in the game.

- Start with 100 points.
- If you find a character, read the score from the character and add it to your score.
- If you find the exit, add 100 points to your score.
- Subtract 1 point for every step you take.
- Subtract 10 points if you try to move outside the board.

Print the score at the end of the game.

### Assignments
- Add the scoring mechanism to the Game class.

## Tips

- Createa test for the random_location function.

Below are some lines of code that you can use in your tests.

```python
assert 0 <= result[0] < 10

# Success case
result = random_location(occupied=[(1, 1)], max_retries=10, width=3, height=3)

# Failure case: fully occupied
with pytest.raises(RuntimeError):
    random_location(occupied=[(0, 0), (0, 1), (1, 0), (1, 1)], max_retries=1, width=2, height=2)

```

- Loop over the characters to give them an unoccupied spot.

```python
for character in characters:
    occupied = [char_loc.location for char_loc in self.character_locations]
    new_location = random_location(width=width, height=height, occupied=occupied)
    self.character_locations.append(CharacterLocation(new_location, character))
```

- Find the exit using the compass.

```python
do_exit = False
steps = 0
while not do_exit and steps < 15:
    steps += 1
    compass = board.get_compass_direction()
    if compass in [Compass.NORTH, Compass.NORTH_EAST, Compass.NORTH_WEST]:
        result = board.move_player(Move.NORTH)
    elif compass in [Compass.SOUTH, Compass.SOUTH_EAST, Compass.SOUTH_WEST]:
        result = board.move_player(Move.SOUTH)
    elif compass == Compass.EAST:
        result = board.move_player(Move.EAST)
    elif compass == Compass.WEST:
        result = board.move_player(Move.WEST)
    elif compass == Compass.HERE:
        print(f"{steps}.You are at the destination! Stop moving.")
        result = None
    else:
        raise RuntimeError(f"Invalid compass direction: {compass}")
    if result:
        print(f"{steps}. You moved {compass.name}. The result is: {result}")
    do_exit = result.type == MoveResultType.EXIT_FOUND if result else False
```
