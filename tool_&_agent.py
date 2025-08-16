from agents import Agent,Runner,function_tool,OpenAIChatCompletionsModel,ModelProvider,AsyncOpenAI
from agents.run import RunConfig
from agents.agent import call_model_function
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
        super().__init__()
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
# =========================
# Now Start to Create Agent and Tool
# =========================
@function_tool
async def summarizer_tool(text: str) -> str:
    prompt = f"Please summarize the following clearly and briefly:\n\n{text}"
    return await call_model_function(prompt)


async def main():
    agent = Agent(
        name="Summerize Agent",
        instructions="You are a helpful assistant. Use tool when needed. ",
        tools=[summarizer_tool],
        model=model_provider.get_model(),
    )

    qury = "Summerize this : Lifelong learning is a vital part of real life that helps us grow, adapt, and stay engaged with the world around us. It goes beyond formal education and includes everyday experiences like learning a new skill, joining clubs, or even listening to educational podcasts during daily routines. For example, someone might decide to learn a new language, take an online cooking class, or join a local community group to meet like-minded people and share knowledge. Keeping a reflective journal can also be a powerful tool, helping individuals track their progress and think critically about their experiences. Lifelong learning is not just about professional development but also about personal enrichment, such as exploring new hobbies, improving mental well-being through mindfulness, or gaining financial literacy to manage everyday life better. Stories like that of Alex Smith, who used education to rebuild confidence after severe health challenges, highlight how continuous learning can transform lives and foster resilience. Successful people like Bill Gates and Elon Musk exemplify lifelong learning by constantly reading, exploring new topics, and pushing boundaries. Ultimately, embracing lifelong learning in real life means staying curious, open to change, and committed to personal growth no matter your age or background, making life richer and more fulfilling"

    result = await Runner.run(agent,qury,run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())