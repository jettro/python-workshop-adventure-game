# Python Workshop — Adventure Game

![Python Training](image/python-training.jpg)

Welcome to the Python Workshop! In this workshop you will build a text-based adventure game step by step, and along the way explore a wide range of Python concepts: from core language features and data analysis to building GUIs, REST APIs, and AI agents.

---

## Assignments

Work through the assignments in order. Each one builds on the previous.

| # | File | Topic |
|---|------|-------|
| 0 | [Setting up the project](0_setting_up_the_project.md) | Bootstrap your Python project with UV |
| 1 | [Program the game](1_program_the_game.md) | Implement the core game logic and domain classes |
| 2 | [Add events](2_add_events.md) | Emit and store game events |
| 3 | [Exploring events](3_exploring_events.md) | Analyse game data with Jupyter, Pandas & Matplotlib |
| 4 | [Create a GUI with Streamlit](4_create_gui_streamlit.md) | Build an interactive web UI for the game |
| 5 | [Create a FastAPI](5_create_fastapi.md) | Expose the game through a REST API |
| 6 | [Use an agent to play the game](6_use_agent_to_play_game.md) | Let an AI agent play the game via MCP + Strands |

---

## Solution

The `solution/` folder contains a complete, working implementation of all assignments. It serves as a reference if you get stuck or want to compare your approach. Avoid peeking too early — you'll learn more by trying first!

---

## Webapp

The `webapp/` folder contains a pre-built React (Vite) frontend that connects to the FastAPI backend you create in assignment 5. Once your API is up and running, you can start the webapp and play the game through a proper browser interface instead of the command line.
