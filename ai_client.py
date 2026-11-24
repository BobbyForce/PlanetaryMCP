import asyncio
import sys

from mcp import Client
from ollama import AsyncClient

MODEL = "qwen3:4b"
QUESTION = "Which planets have rings, and how many queries has our app served so far?"


async def main(question):
    llm = AsyncClient()
    async with Client("http://127.0.0.1:8000/mcp") as mcp_client:
        # 1. Get the tools from MCP and convert them to Ollama's format
        tools = await mcp_client.list_tools()
        ollama_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or "",
                    "parameters": t.input_schema,
                },
            }
            for t in tools.tools
        ]

        messages = [{"role": "user", "content": question}]

        # 2. Let the model call tools, at most 5 rounds
        for _ in range(5):
            response = await llm.chat(model=MODEL, messages=messages, tools=ollama_tools)
            messages.append(response.message)

            if not response.message.tool_calls:
                print("\nFinal answer:\n" + (response.message.content or ""))
                return

            # 3. Run each tool the model asked for and send the result back
            for call in response.message.tool_calls:
                name = call.function.name
                args = dict(call.function.arguments or {})
                print(f"Model called {name}({args})")
                result = await mcp_client.call_tool(name, args)
                text = "\n".join(block.text for block in result.content)
                print("  ->", text[:150].replace("\n", " "))
                messages.append({"role": "tool", "tool_name": name, "content": text})

        print("Stopped after 5 rounds.")


asyncio.run(main(" ".join(sys.argv[1:]) or QUESTION))