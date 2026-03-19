# Use Agent to Play Game
In this section, we will use an AI agent to play the game by interacting with the FastAPI server. You first expose the FastAPI server as an MCP server. Next you use Strands to program an agent to play the game.

## Installation
Install the dependencies:

```bash
uv add 'strands-agents[openai]'
uv add strands-agents-tools
```

## MCP Server

You can also expose the API as an MCP (Model Context Protocol) server. This allows AI models to interact with your game as a tool.

First install a new dependency: `fastapi_mcp`

```bash
uv add fastapi_mcp
```

Wrap the fastapi application to expose the API as an MCP server. Do this after the definition of all the endpoints.


```python
from fastapi_mcp import FastApiMCP

# Add MCP server to the FastAPI app
mcp = FastApiMCP(app)

# Mount the MCP server to the FastAPI app
mcp.mount_http()
```

## Load the OpenAI API Key
You create a .env file in the root directory of the project. This file contains the following line.

```dotenv
OPENAI_API_KEY=sk-proj-YOUR_API_KEY
```

## Write the agent
You can copy paste the code from the next code block into the file run_agent.py. Look at the code, try to understand what happens. If you have done all the steps correctly, you should be able to run the agent.

```python
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
```

Can you change the prompt so the agent starts looking for all the characters before it searches for the exit?
