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

class StopResponse(BaseModel):
    game_id: str
    message: str

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
        compass_dir = self.board.get_compass_direction()
        return GameState(
            game_id=self.game_id,
            score=self.score,
            messages=self.messages,
            finished=self.finished,
            compass=compass_dir.name if compass_dir else None,
            player_location=list(self.board.player_location)
        )
