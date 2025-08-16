from agents import Runner, Agent
from config import config 


# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant powered by Gemini.",
)

# Run agent
try:
    result = Runner.run_sync(agent, "Hello!How are you", run_config=config)
    print(result.final_output)
except Exception as e:
    print(f"Error running agent: {str(e)}")

