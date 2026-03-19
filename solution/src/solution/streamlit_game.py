import streamlit as st

from solution.board import Character, Board, Move, MoveResultType


class StreamlitGame:
    def __init__(self):
        if 'game_initialized' not in st.session_state:
            self._initialize_game()

    def _initialize_game(self):
        characters = [
            Character(points=1, message="You found a key!"),
            Character(points=-2, message="You stepped into a puddle of muddy water!"),
            Character(points=-1, message="You hit a wall!"),
            Character(points=-1, message="You hit a monster!"),
            Character(points=5, message="You found a gem")
        ]
        st.session_state.board = Board(characters=characters, height=10, width=10)
        st.session_state.score = 100
        st.session_state.messages = ["Welcome to the Adventure Game! Find the exit."]
        st.session_state.finished = False
        st.session_state.game_initialized = True

    def move(self, move_direction: Move):
        if st.session_state.finished:
            return

        move_result = st.session_state.board.move_player(move_direction)
        st.session_state.score -= 1

        # TODO handle the result of the move
        if move_result.type == MoveResultType.EXIT_FOUND:
            st.session_state.score += 100
            st.session_state.messages.append(
                f"*** Yes you found the exit! Congratulations! Final score: {st.session_state.score}")
            st.session_state.finished = True
        elif move_result.type == MoveResultType.CHARACTER_FOUND:
            st.session_state.score += move_result.character.points
            st.session_state.messages.append(
                f"Character found: {move_result.character.message} ({move_result.character.points} pts)")
        elif move_result.type == MoveResultType.OUT_OF_BOUNDS:
            st.session_state.score -= 10
            st.session_state.messages.append("You are at the end of the board! (-10 pts)")
        elif move_result.type == MoveResultType.SUCCESS:
            compass = st.session_state.board.get_compass_direction()
            st.session_state.messages.append(f"Moved {move_direction.name}. The exit is {compass.name}.")


    def reset(self):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self._initialize_game()
