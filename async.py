from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,ModelProvider
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

# Get Gemini api key 
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

class GeminiModelProvider(ModelProvider):
    def __init__(self,api_key,model_name="gemini-2.0-flash"):
        # super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    def get_model(self):
        return OpenAIChatCompletionsModel(
            model=self.model_name,
            openai_client=self.client
        )

model_provider = GeminiModelProvider(api_key=gemini_api_key)    

# Configure model
config = RunConfig(
    model=model_provider.get_model(),
    model_provider=model_provider,
    tracing_disabled=True
)

# Create Agent in Async
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant powered by Gemini.",
        model=model_provider.get_model(),
    )
    result = await Runner.run(agent,"Hello!How are you",run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())