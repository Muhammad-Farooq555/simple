from agents import Agent,Runner
import asyncio
from config import config

# Create Agent in Async
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant powered by Gemini.",
    )
    result = await Runner.run(agent,"Hello!How are you",run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())