import os

from dotenv import load_dotenv
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

if __name__ == "__main__":
    load_dotenv()

    model = OpenAIModel(
        client_args={
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
        model_id="gpt-5-mini",
    )

    mcp_client = MCPClient(
        lambda: streamable_http_client(url="http://localhost:8000/mcp")
    )

    with mcp_client:
        tools = mcp_client.list_tools_sync()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.tool_name}")

        agent = Agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are an adventure game agent. "
                "You MUST only use the provided tools to interact with the game. "
                "Do NOT invent game states, scores, or messages. "
                "Every move must be made via the `move_player` tool using the `game_id` obtained from `start_game`. "
                "The game is played on a 10x10 grid. Your goal is to find the exit. "
                "After each move, analyze the game state returned by the tool to decide your next move. "
                "The 'compass' in the state tells you the direction to the exit."
            )
        )

        agent("Play a game of Adventure. Return the final score and the steps you took with the response messages.")