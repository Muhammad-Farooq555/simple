from agents import Agent, Runner, function_tool
import requests
import asyncio
from config import config 


@function_tool
def get_weather(city:str)->str:
    """
    Get the current weather for a given city.
    """
    result= requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    data= result.json()
    return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."

conversation_history = []

def add_to_history(role, content):
    conversation_history.append({"role": role, "content": content})

# Programming Agent
agent1 = Agent(
    name="Programming Agent",
    handoff_description="Handles programming questions.",
    instructions="""
You are a helpful programming assistant.

1. If the user asks about a programming concept, give a **simple and clear explanation** in 3–5 lines.
2. If the user says "in detail" or asks a follow-up, then respond with a **detailed explanation** and more examples.
3. If the query is not related to programming, respond only with: HANDOFF_TO:general
""",
)

# General Agent
agent2 = Agent(
    name="General Agent",
    handoff_description="Handles general questions or those handed off from other agents.",
    instructions="""
You are a helpful general-purpose assistant.

1. If the question is about programming, code, Python, functions, etc., respond with: HANDOFF_TO:programming
2. Otherwise, answer normally with helpful, clear responses.
""",
    tools=[get_weather],
)

# Multi-agent handoff handler
async def multi_agent(prompt):
    current_agent = agent1
    result = await Runner.run(current_agent, prompt, run_config=config)

    while True:
        if "HANDOFF_TO:general" in result.final_output:
            print("🔁 Handoff: Programming Agent → General Agent")
            current_agent = agent2
            result = await Runner.run(current_agent, prompt, run_config=config)
        elif "HANDOFF_TO:programming" in result.final_output:
            print("🔁 Handoff: General Agent → Programming Agent")
            current_agent = agent1
            result = await Runner.run(current_agent, prompt, run_config=config)
        else:
            return result.final_output

# Run CLI loop
print("\n🧠 Multi-Agent System is Ready!\n")
if __name__ == "__main__":
    while True:
        try:
            user_input = input("🧑 You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting. Goodbye!")
                break

            final_answer = asyncio.run(multi_agent(user_input))
            print(f"🤖 Agent: {final_answer}\n")
        except Exception as e:
            print("❌ Error:", e)




