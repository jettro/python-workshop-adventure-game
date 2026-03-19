from solution import init_board
from solution.board import Board, Character, Move, MoveResultType, Compass
from solution.events import EventHandler
from solution.game import Game

if __name__ == "__main__":
    # Assignment 0
    # init_board()
    # print("Board initialized successfully")

    # Assignment 1
    # board = Board(characters=[
    #     Character(points=1, message="You found a key!"),
    #     Character(points=-2, message="You stepped into a puddle of muddy water!"),
    #     Character(points=-1, message="You hit a wall!"),
    #     Character(points=-1, message="You hit a monster!"),
    #     Character(points=5, message="You found a gem")
    # ], height=10, width=10)
    #
    # board.print_board_info()

    # do_exit = False
    # while not do_exit:
    #     result = board.move_player(Move.NORTH)
    #     print(result)
    #     do_exit = result.type == MoveResultType.EXIT_FOUND or result.type == MoveResultType.OUT_OF_BOUNDS

    # do_exit = False
    # steps = 0
    # while not do_exit and steps < 15:
    #     steps += 1
    #     compass = board.get_compass_direction()
    #     if compass in [Compass.NORTH, Compass.NORTH_EAST, Compass.NORTH_WEST]:
    #         result = board.move_player(Move.NORTH)
    #     elif compass in [Compass.SOUTH, Compass.SOUTH_EAST, Compass.SOUTH_WEST]:
    #         result = board.move_player(Move.SOUTH)
    #     elif compass == Compass.EAST:
    #         result = board.move_player(Move.EAST)
    #     elif compass == Compass.WEST:
    #         result = board.move_player(Move.WEST)
    #     elif compass == Compass.HERE:
    #         print(f"{steps}.You are at the destination! Stop moving.")
    #         result = None
    #     else:
    #         raise RuntimeError(f"Invalid compass direction: {compass}")
    #     if result:
    #         print(f"{steps}. You moved {compass.name}. The result is: {result}")
    #     do_exit = result.type == MoveResultType.EXIT_FOUND if result else False

    game = Game()
    event_handler = EventHandler()
    game.add_event_listener(event_handler.handle_event)
    game.run()