import uuid
from typing import Callable

from solution.board import Board, Character, MoveResultType, Move
from solution.events import GameEvent, GameEndedEvent, ExitFoundEvent, CharacterFoundEvent, MoveFailedEvent, \
    PlayerMovedEvent, GameStartedEvent


class Game:
    game_id: str = str(uuid.uuid4())
    finished: bool = False
    score: int = 100
    event_listeners = []

    def __init__(self):
        self.board = Board(characters=[
            Character(points=1, message="You found a key!"),
            Character(points=-2, message="You stepped into a puddle of muddy water!"),
            Character(points=-1, message="You hit a wall!"),
            Character(points=-1, message="You hit a monster!"),
            Character(points=5, message="You found a gem")
        ], height=10, width=10)

        self.board.print_board_info()

    def run(self):
        directions = {
            "N": Move.NORTH,
            "E": Move.EAST,
            "S": Move.SOUTH,
            "W": Move.WEST
        }
        self.__emit_event(
            GameStartedEvent(
                game_id=self.game_id,
                height=self.board.height,
                width=self.board.width,
                score=self.score,
                row=self.board.player_location[0],
                column=self.board.player_location[1]
            ))
        while not self.finished:
            user_input = input("Enter direction (N, E, S, W) or Q to quit: ").strip().upper()
            if user_input == "Q":
                self.__emit_event(GameEndedEvent(
                    game_id=self.game_id,
                    score=self.score,
                    message="Game ended by user.",
                    row=self.board.player_location[0],
                    column=self.board.player_location[1]
                ))
                break

            if user_input in directions:
                move_result = self.board.move_player(directions[user_input])
                self.score -= 1

                if move_result.type == MoveResultType.EXIT_FOUND:
                    print("*** Yes you found the exit! Congratulations!")
                    self.score += 100
                    print(f"Your final score is: {self.score}")
                    self.finished = True
                    self.__emit_event(
                        ExitFoundEvent(game_id=self.game_id,
                                       score=self.score,
                                       row=move_result.location[0],
                                       column=move_result.location[1]
                                       ))
                elif move_result.type == MoveResultType.CHARACTER_FOUND:
                    print(f"You found a character, this is its message: `{move_result.character.message}`!")
                    self.score += move_result.character.points
                    self.__emit_event(CharacterFoundEvent(game_id=self.game_id,
                                                          character_message=move_result.character.message,
                                                          points=move_result.character.points,
                                                          score=self.score,
                                                          row=move_result.location[0],
                                                          column=move_result.location[1]
                                                          ))
                elif move_result.type == MoveResultType.OUT_OF_BOUNDS:
                    print("You are at the end of the board!")
                    self.score -= 10
                    self.__emit_event(MoveFailedEvent(game_id=self.game_id,
                                                      direction=user_input,
                                                      message="You are at the end of the board.",
                                                      score=self.score,
                                                      row=move_result.location[0],
                                                      column=move_result.location[1]
                                                      ))
                elif move_result.type == MoveResultType.SUCCESS:
                    compass = self.board.get_compass_direction()
                    print(f"You moved to {move_result.location}.")
                    print(f"The exit is in the {compass.name} direction.")
                    self.__emit_event(PlayerMovedEvent(game_id=self.game_id,
                                                       direction=user_input,
                                                       score=self.score,
                                                       row=move_result.location[0],
                                                       column=move_result.location[1]
                                                       ))
                else:
                    print("Unknown move result type!")
            else:
                print("Invalid input! Please enter N, E, S, W, or Q.")

    def add_event_listener(self, listener: Callable[[GameEvent], None]):
        self.event_listeners.append(listener)

    def __emit_event(self, event: GameEvent):
        for listener in self.event_listeners:
            listener(event)
