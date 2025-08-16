# import asyncio 
# import aiohttp # async HTTP library

# Practice With Single API 

# async def get_crypto_price():
#     url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = response.json()
#             print(f"Cryptp Price : {data}")

# asyncio.run(get_crypto_price())

# Practice With Multiple APIs

# async def get_weather(session):
#     async with session.get("https://wttr.in/?format=3") as response:
#         data = await response.text()
#         print(f"Weather: {data}")

# async def get_news(session):
#     async with session.get("https://api.publicapis.org/entries") as response:
#         data = await response.text()
#         print(f"News: {data}")

# async def get_crypto_price(session):
#     async with session.get("https://api.coindesk.com/v1/bpi/currentprice.json") as response:
#         data = await response.text()
#         print(f"Weather: {data}")

# async def main():
#     async with aiohttp.ClientSession() as session:
       
#        task1 = asyncio.create_task(get_weather(session))
#        task2 = asyncio.create_task(get_news(session))
#        task3 = asyncio.create_task(get_crypto_price(session))

#        await task1
#        await task2
#        await task3

#     #    await asyncio.gather(
#     #         get_weather(session),
#     #         get_news(session),
#     #         get_crypto_price(session),
#     #     )

# asyncio.run(main())


# import asyncio

# async def func1():
#     print("Start Task 1")
#     await asyncio.sleep(2)
#     print("Finished Task 1")

# async def func2():
#     print("Start Task 2")
#     await asyncio.sleep(2)
#     print("Finished Task 2")

# async def func3():
#     print("Start Task 3")
#     await asyncio.sleep(2)
#     print("Finished Task 3")

# async def slow_task():
#     print("Start Task!")
#     await asyncio.sleep(2)
#     print("Finished Task!")


# async def main():

#     # await slow_task()

#     # Option 1
#     t1 = asyncio.create_task(func1())
#     t2 = asyncio.create_task(func2())
#     t3 = asyncio.create_task(func3())

#     await t1
#     await t2
#     await t3

#     # # Option 2
#     # await asyncio.gather(
#     #     func1(),
#     #     func2(),
#     #     func3()
#     # )

# asyncio.run(main())


# import asyncio
# import time

# async def task(name):
#     print(f"Start {name}")
#     await asyncio.sleep(2)
#     print(f"End {name}")

# # Sequential version (wrong way)
# async def sequential():
#     start = time.time()
#     await asyncio.create_task(task("A"))
#     await asyncio.create_task(task("B"))
#     await asyncio.create_task(task("C"))
#     print(f"Sequential took: {time.time() - start:.2f} sec")

# # Concurrent version (right way)
# async def concurrent():
#     start = time.time()
#     t1 = asyncio.create_task(task("A"))
#     t2 = asyncio.create_task(task("B"))
#     t3 = asyncio.create_task(task("C"))
#     await t1
#     await t2
#     await t3
#     print(f"Concurrent took: {time.time() - start:.2f} sec")

# async def main():
#     print("\nSequential:")
#     await sequential()
    
#     print("\nConcurrent:")
#     await concurrent()

# asyncio.run(main())



# import asyncio
# import aiohttp  # async HTTP library

# async def get_weather(session):
#     async with session.get("https://wttr.in/?format=3") as response:
#         data = await response.text()
#         print("Weather:", data)

# async def get_news(session):
#     async with session.get("https://api.publicapis.org/entries") as response:
#         data = await response.text()
#         print("News:", data)

# async def get_crypto(session):
#     async with session.get("https://api.coindesk.com/v1/bpi/currentprice.json") as response:
#         data = await response.text()
#         print("Crypto:", data)

# async def main():
#     async with aiohttp.ClientSession() as session:
#         # All API calls at the same time!
#         await asyncio.gather(
#             get_weather(session),
#             get_news(session),
#             get_crypto(session)
#         )

# asyncio.run(main())

# With Files library

# import asyncio
# from pathlib import Path
# import aiofiles

# sem = asyncio.Semaphore(10)  

# async def write_table(n):
#     async with sem:
#         filename = f"tables/table_{n}.txt"
#         Path("tables").mkdir(exist_ok=True)  # folders 
#         async with aiofiles.open(filename, 'w') as f:
#             for i in range(1, 11):
#                 line = f"{n} x {i} = {n*i}\n"
#                 await f.write(line)
#         print(f"Table {n} written.")

# async def main():
#     tasks = [write_table(i) for i in range(1, 101)]
#     await asyncio.gather(*tasks)

# asyncio.run(main())


# -----------------------------

# OpenAI Agents SDK

# from openai import AssistantBuilder
# from openai.agents import function_tool

# @function_tool
# def add(a: int, b: int) -> int:
#     return a + b

# @function_tool
# def multiply(a: int, b: int) -> int:
#     return a * b

# agent = AssistantBuilder().tools([add,multiply]).build()
# response = agent.run("Add 5 and 9")
# print(response)




# from agents import Agent, Runner
# from dotenv import load_dotenv


# load_dotenv()

# agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# result = Runner.run_sync(agent, "What is LLM?")
# print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.


from openai import AsyncOpenAI
from agents import Agent,OpenAIChatCompletionsModel,Runner,set_tracing_disabled
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()   

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

# # This agent will use the custom LLM provider
# agent = Agent(
#     name="Assistant",
#     instructions="You are an expert programmer. Answer all coding problems in a simple, small, clear, and beginner-friendly way. Always provide examples when needed.",
#     model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=clinet)
# )

summerize_agent = Agent(
    name="Summerize Agent",
    handoff_description="Specialist agent for summarizing text",
    instructions="""
    You provide help with summarizing text. 
    Explain your reasoning at each step and include examples.
    Provide a short summary of the given text.
    You can also ask the user for clarification or more information.
    """,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)

programming_agent = Agent(
    name="Programming Agent",
    handoff_description="Specialist agent for theory of programming",
    instructions="""
    You provide help with theory of programming. 
    Explain your reasoning at each step and include examples.
    Provide a clear and concise answer to the given text.
    You can also ask the user for clarification or more information.
    """,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)

async def main():

    agent = Agent(
    name="Assistant",
    instructions="""
    You are an expert assistant. 
    Provide clear, concise, and accurate answers to all queries. 
    Include examples where applicable.
    Always provide enough information to be useful: provide context, explain your reasoning, and provide examples.
    """,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[summerize_agent, programming_agent]
    )
    
    result = await Runner.run(agent, "Lifelong learning is a vital part of real life that helps us grow, adapt, and stay engaged with the world around us. It goes beyond formal education and includes everyday experiences like learning a new skill, joining clubs, or even listening to educational podcasts during daily routines. For example, someone might decide to learn a new language, take an online cooking class, or join a local community group to meet like-minded people and share knowledge. Keeping a reflective journal can also be a powerful tool, helping individuals track their progress and think critically about their experiences. Lifelong learning is not just about professional development but also about personal enrichment, such as exploring new hobbies, improving mental well-being through mindfulness, or gaining financial literacy to manage everyday life better. Stories like that of Alex Smith, who used education to rebuild confidence after severe health challenges, highlight how continuous learning can transform lives and foster resilience. Successful people like Bill Gates and Elon Musk exemplify lifelong learning by constantly reading, exploring new topics, and pushing boundaries. Ultimately, embracing lifelong learning in real life means staying curious, open to change, and committed to personal growth no matter your age or background, making life richer and more fulfilling. Summarize text")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

