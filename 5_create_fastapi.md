# Create an API to the game
You are implementing an REST API to the game. Through the API, you can start a new game, move the player, and close the game.

A popular library for creating REST APIs is FastAPI. It is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Installation

First you need to add the fastapi dependency to the project.

```bash
uv add fastapi
uv add uvicorn
```

## Create the FastAPI Game
You start by creating the game class for FastAPI. Create a new file called fastapi_game.py and add the following code. Notice the TODO, implement the get_state method.

```python
from typing import List, Optional

from pydantic import BaseModel

from solution.board import Character, Board, Move, MoveResultType


class GameState(BaseModel):
    game_id: str
    score: int
    messages: List[str]
    finished: bool
    compass: Optional[str] = None
    player_location: List[int]

class MoveRequest(BaseModel):
    game_id: str
    direction: str  # N, E, S, W

class StopRequest(BaseModel):
    game_id: str


class FastAPIGame:
    def __init__(self, game_id: str):
        self.game_id = game_id
        characters = [
            Character(points=1, message="You found a key!"),
            Character(points=-2, message="You stepped into a puddle of muddy water!"),
            Character(points=-1, message="You hit a wall!"),
            Character(points=-1, message="You hit a monster!"),
            Character(points=5, message="You found a gem")
        ]
        self.board = Board(characters=characters, height=10, width=10)
        self.score = 100
        self.messages = ["Welcome to the Adventure Game! Find the exit."]
        self.finished = False

    def move(self, direction_str: str):
        if self.finished:
            return

        direction_map = {
            "N": Move.NORTH,
            "E": Move.EAST,
            "S": Move.SOUTH,
            "W": Move.WEST
        }

        move_direction = direction_map.get(direction_str.upper())
        if not move_direction:
            raise ValueError("Invalid direction. Use N, E, S, or W.")

        move_result = self.board.move_player(move_direction)
        self.score -= 1

        if move_result.type == MoveResultType.EXIT_FOUND:
            self.score += 100
            self.messages.append(f"*** Yes you found the exit! Congratulations! Final score: {self.score}")
            self.finished = True
        elif move_result.type == MoveResultType.CHARACTER_FOUND:
            self.score += move_result.character.points
            self.messages.append(
                f"Character found: {move_result.character.message} ({move_result.character.points} pts)")
        elif move_result.type == MoveResultType.OUT_OF_BOUNDS:
            self.score -= 10
            self.messages.append("You are at the end of the board! (-10 pts)")
        elif move_result.type == MoveResultType.SUCCESS:
            compass = self.board.get_compass_direction()
            self.messages.append(f"Moved {move_direction.name}. The exit is {compass.name}.")

    def get_state(self) -> GameState:
        # TODO: Implement this method
    

```

### Assignment
- Install the FastAPI dependencies.
- Create the FastAPIGame class and implement the get_state method in the file fastapi_game.py.
- (Optional) Write a unit test for the move method.

## Implement the API
Next, you create the runner for the FastAPI game. Create the file run_fastapi.py in the root of the project and add the following code. First you create the app, next you create the memory of active games. In the previous applications, you could start one game at a time. With the web api, you can run multiple games simultaneously. Each game is identified by a unique game_id.

```python
from typing import Dict

from fastapi import FastAPI

from solution.fastapi_game import FastAPIGame

app = FastAPI(title="Adventure Game API")

active_games: Dict[str, FastAPIGame] = {}
```

Next, you create the endpoint for starting a new game. You use the game_id as the key in the active_games dictionary. Look at the annotation in the code to see how an endpoint is configured.

```python
@app.post("/start", response_model=GameState, operation_id="start_game")
async def start_game() -> GameState:
    """
    Start a new adventure game.

    Returns the initial game state including game_id, starting score, and location.
    """
    game_id = str(uuid.uuid4())
    new_game = FastAPIGame(game_id)
    active_games[game_id] = new_game
    return new_game.get_state()
```

You can now start the game by by uv or direct using a normal python runner.

```bash
uv run uvicorn run_fastapi:app --reload
```

or add the following to the run_fastapi.py file.

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

Now you can start a new game by sending a POST request to the /start endpoint. Try it using curl or whatever you prefer.

Can you implement the move endpoint? Use the code in the fastapi_game.py file. Below is the interface for the move endpoint.

```python
@app.post("/move", response_model=GameState, operation_id="move_player")
async def move_player(request: MoveRequest):
    """
    Move the player in the adventure game. Valid directions are N, E, S, and W.

    :return: The updated game state.
    """

```

The final method is the stop endpoint. I leave that completely up to you.

### Assignments
- Create the file run_fastapi.py and add code to initialize the FastAPI server.
- Copy the code for the start endpoint, run the server and test it.
- Implement the move endpoint.
- Implement the stop endpoint.
- Use the endpoints to create a game and move the player.

## Ideas for exercises

- Add an overview of active games
- Add the event_listener to the game and store games into the game_events.jsonl file.
- Let them create the move method


