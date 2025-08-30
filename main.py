import asyncio
import json
import google.generativeai as genai
from decouple import config
from serp import search_duckduckgo
from pdf_exporter import export_to_pdf

# Configure Gemini
genai.configure(api_key=config("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

# Define tool schemas using the correct format for this version
tools = [
    {
        "function_declarations": [
            {
                "name": "search_duckduckgo",
                "description": "Search DuckDuckGo for information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to look up"
                        }
                    },
                    "required": ["query"]
                },
            },
            {
                "name": "export_to_pdf",
                "description": "Export or save items to a PDF file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of text items to export"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Name of the PDF file to create"
                        }
                    },
                    "required": ["results"]
                },
            }
        ]
    }
]

async def execute_tool(name: str, args: dict):
    if name == "search_duckduckgo":
        return await search_duckduckgo(args["query"])
    elif name == "export_to_pdf":
        return export_to_pdf(args["results"], args.get("filename", "results.pdf"))
    return f"Unknown tool: {name}"

async def chat_loop():
    history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit"}:
            break

        # Add user message to history
        history.append({"role": "user", "parts": [{"text": user_input}]})

        response = model.generate_content(
            history,
            tools=tools,
        )

        # Check if Gemini requested a tool call
        fc = getattr(response.candidates[0].content.parts[0], "function_call", None)
        if fc:
            tool_name = fc.name
            # Convert MapComposite to dict if needed
            if hasattr(fc.args, 'to_dict'):
                tool_args = fc.args.to_dict()
            else:
                tool_args = dict(fc.args) if fc.args else {}
            print(f"🔧 Gemini wants to call {tool_name} with {tool_args}")

            # Run tool
            result = await execute_tool(tool_name, tool_args)

            # Feed back result
            # Function responses have a different format
            history.append({
                "role": "model",
                "parts": [{"text": str(result)}]
            })

            follow_up = model.generate_content(history)
            print("Gemini:", follow_up.text)
            history.append({"role": "assistant", "parts": [{"text": follow_up.text}]})

        else:
            print("Gemini:", response.text)
            history.append({"role": "assistant", "parts": [{"text": response.text}]})

if __name__ == "__main__":
    asyncio.run(chat_loop())
