from config import config
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
class MessageOutput(BaseModel): 
    response: str

class MathOutput(BaseModel): 
    reasoning: str
    is_math: bool

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail
async def math_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:    
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

agent = Agent( 
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



# from pydantic import BaseModel

# from agents import (
#     Agent,
#     GuardrailFunctionOutput,
#     InputGuardrailTripwireTriggered,
#     RunContextWrapper,
#     Runner,
#     TResponseInputItem,
#     input_guardrail,
# )

# class MathHomeworkOutput(BaseModel):
#     is_math_homework: bool
#     reasoning: str

# guardrail_agent = Agent( 
#     name="Guardrail check",
#     instructions="Check if the user is asking you to do their other any type of data",
#     output_type=MathHomeworkOutput,
# )

# @input_guardrail
# async def math_guardrail( 
#     ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output, 
#         tripwire_triggered=result.final_output.is_math_homework,
#     )


# agent = Agent(  
#     name="Customer Support Agent",
#     instructions="You are a customer support agent. You help customers with their questions.",
#     input_guardrails=[math_guardrail],
# )

# async def main():
#     # This should trip the guardrail
#     try:
#         await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?",run_config=config)
#         print("Guardrail didn't trip - this is unexpected")

#     except InputGuardrailTripwireTriggered:
#         print("Guardrail tripped as expected")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())