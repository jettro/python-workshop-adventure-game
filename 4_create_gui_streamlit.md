# Create GUI with Streamlit

Streamlit is an open-source Python framework for building interactive web applications, especially for data science and machine learning projects. It allows you to turn a Python script into a web app with very little code and no front-end experience. You write normal Python, and Streamlit automatically renders widgets, charts, tables, and text in the browser. The framework follows a simple execution model: every time a user interacts with a widget, the script reruns from top to bottom. Streamlit provides built-in components such as sliders, buttons, text inputs, file uploaders, and data visualizations. It integrates easily with popular libraries like pandas, matplotlib, Plotly, and scikit-learn. Layout options such as columns, sidebars, and containers help structure your app cleanly. State management is handled through st.session_state, allowing you to persist data across interactions. Apps can be run locally with a single command (streamlit run app.py) and deployed easily to the cloud. Overall, Streamlit is designed to make building data apps fast, intuitive, and accessible for Python developers.

## Install Streamlit and learn the basics

First, add the dependency to your project:

```bash
uv add streamlit
```

Next write a simple script `run_streamlit.py` in the root of the project (not the src folder) and run it with the following code:

```python
import streamlit as st

st.write("Hello, do you want to play a game?")
```

Run the script with `streamlit run run_streamlit.py`. If you are not in the python context of the project, run the followin command:

```bash
source .venv/bin/activate
streamlit run run_streamlit.py
```

One essential feature to understand in Streamlit is that the complete script is executed every time you interact with a widget. It does not remember the state of your app. Use the next lines of code to add a counter to your app. Force a safe of the file (for me it is `command + s`), notice the menu at the right top corner of the browser window. You can press the Rerun or the Always rerun button to see the changes. This is a feature of Streamlit that allows you to quickly iterate on your app during development.

```python
import streamlit as st

counter = 0
if st.button("Click me"):
    counter += 1

st.write(f"Counter: {counter}")
```

Now click the button and see the counter increase, once.

To make the counter persistent, we have to use `st.session_state`. This is a dictionary-like object that allows you to store and retrieve data across reruns of your app. It is useful for storing stateful information that you want to persist between user interactions. For example, you can use it to store the current value of a counter, or the state of a game.

```python
import streamlit as st

counter = st.session_state.get("counter", 0)
if st.button("Click me"):
    counter += 1
    st.session_state["counter"] = counter
    
st.write(f"Counter: {counter}")
```

The `st.session_state` object is used to store and retrieve data across reruns of your app. It is useful for storing stateful information that you want to persist between user interactions. In this case, we use it to store the current value of the counter. The `get` method is used to retrieve the value of the counter from the session state, with a default value of 0 if the counter is not present. The `st.session_state["counter"] = counter` line is used to update the value of the counter in the session state. This ensures that the counter is persistent across reruns of the app.

Try it out!

### Assignment
- Create the streamlit app and learn the basic elements of streamlit 
- work with a session state.

## Create the GUI

The next code block create the GUI for the game, it reuses the code from the previous exercise. Most of the code is available, you need to create the game logic in the move method. 

You start with the StreamliGame class. Create a file streamlit_game in the solution package and copy the class from the block below.

```python

import streamlit as st
import random
from run_game__2 import Board, Character, Move, MoveResultType, Compass

# --- Game Class for Streamlit ---
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
        

    def reset(self):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self._initialize_game()
```

Notice the following parts of the code:
- In _initialize_game_ we create the board and set the initial state in the session state.
- In the __init__ method we check if the game is already initialized.

Search for the TODO en use the Game class you created in the previous exercise for inspiration. Do not change the code from the previous exercise. You need it in a next assignment. Tip, finish the next part first so you can run the game.

Next, copy the code for the GUI below into the run_streamlit.py file from before. You most likely need to change the imports to match the new file structure.

Notice the following parts of the code:
- The GUI consists of two columns. there are multiple ways to write to the screen in streamlit. With `with col1:` the st has the context of the first column. This is a shorthand for `st.col1.write()`


```python

import streamlit as st
import random

# --- UI Layout ---
st.set_page_config(page_title="Adventure Game", layout="wide")

game = StreamlitGame()

st.title("🏹 Adventure Game")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Status")
    st.metric("Score", st.session_state.score)
    
    # Compass Display
    st.subheader("Compass")
    compass_dir = st.session_state.board.get_compass_direction()
    
    # Simple visual representation of compass
    compass_icons = {
        Compass.NORTH: "⬆️ North",
        Compass.NORTH_EAST: "↗️ North East",
        Compass.EAST: "➡️ East",
        Compass.SOUTH_EAST: "↘️ South East",
        Compass.SOUTH: "⬇️ South",
        Compass.SOUTH_WEST: "↙️ South West",
        Compass.WEST: "⬅️ West",
        Compass.NORTH_WEST: "↖️ North West",
        Compass.HERE: "📍 You are at the Exit!"
    }
    st.info(f"Direction to Exit: **{compass_icons.get(compass_dir, 'Unknown')}**")

    # Reset Button
    if st.button("Reset Game"):
        game.reset()
        st.rerun()

with col2:
    st.header("Controls")
    
    # Grid for buttons
    c1, c2, c3 = st.columns(3)
    with c2:
        if st.button("North", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.NORTH)
            st.rerun()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("West", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.WEST)
            st.rerun()
    with c3:
        if st.button("East", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.EAST)
            st.rerun()
            
    c1, c2, c3 = st.columns(3)
    with c2:
        if st.button("South", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.SOUTH)
            st.rerun()

    st.header("Game Log")
    # Display last 10 messages in reverse order
    for msg in reversed(st.session_state.messages[-10:]):
        st.write(msg)

```

### Assignment
- Copy the code for the StreamlitGame class into a new file called streamlit_game.py within the package you have created.
- Copy the code for the GUI into the run_streamlit.py file.
- Implement the move method, look for the TODO. You can use the implementation from the game class of the previous exercise.

## Play with the GUI

Tryout the GUI and see if you can find the exit. You can change the code and see how the GUI changes.
