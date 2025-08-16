from agents import AsyncOpenAI, Runner, Agent, OpenAIChatCompletionsModel, ModelProvider
from agents.run import RunConfig
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Custom ModelProvider for Gemini API
class GeminiModelProvider(ModelProvider):
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def get_model(self):
        """
        Implement the abstract get_model method to return an OpenAIChatCompletionsModel.
        """
        return OpenAIChatCompletionsModel(model=self.model_name, openai_client=self.client)

# Get Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Create model provider
model_provider = GeminiModelProvider(api_key=gemini_api_key)

# Configure RunConfig
config = RunConfig(
    model=model_provider.get_model(),
    model_provider=model_provider,
    tracing_disabled=True
)

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant powered by Gemini.",
    model=model_provider.get_model(),
)

# Run agent
try:
    result = Runner.run_sync(agent, "Hello!How are you", run_config=config)
    print(result.final_output)
except Exception as e:
    print(f"Error running agent: {str(e)}")

