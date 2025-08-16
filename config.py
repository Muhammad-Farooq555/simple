import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents.run import RunConfig
from agents import OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Validate environment variables
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY must be set in the .env file")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

config = RunConfig(
    model=model,
    model_provider=client, # type: ignore
    tracing_disabled=True
)