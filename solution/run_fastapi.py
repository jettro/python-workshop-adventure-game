import uuid
from typing import Dict

from fastapi import FastAPI, HTTPException

from solution.fastapi_game import FastAPIGame, GameState, MoveRequest, StopRequest, StopResponse

app = FastAPI(title="Adventure Game API")

active_games: Dict[str, FastAPIGame] = {}


@app.post("/start", response_model=GameState, operation_id="start_game")
async def start_game():
    """
    Start a new adventure game.

    Returns the initial game state including game_id, starting score, and location.
    """
    game_id = str(uuid.uuid4())
    new_game = FastAPIGame(game_id)
    active_games[game_id] = new_game
    return new_game.get_state()


@app.post("/move", response_model=GameState, operation_id="move_player")
async def move_player(request: MoveRequest):
    """
    Move the player in the adventure game. Valid directions are N, E, S, and W.

    :return: The updated game state.
    """
    game = active_games.get(request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.finished:
        raise HTTPException(status_code=400, detail="Game already finished")

    try:
        game.move(request.direction)
        return game.get_state()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/stop", response_model=StopResponse, operation_id="stop_game")
async def stop_game(request: StopRequest):
    game = active_games.get(request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game.finished = True
    game.messages.append("Game stopped by user.")

    return StopResponse(game_id=request.game_id, message="Game stopped")

# This is for the agent assignment only
from fastapi_mcp import FastApiMCP

# Add MCP server to the FastAPI app
mcp = FastApiMCP(app)

# Mount the MCP server to the FastAPI app
mcp.mount_http()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

