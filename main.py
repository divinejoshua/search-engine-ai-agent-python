import asyncio
import google.generativeai as genai
from serp import search_duckduckgo
from pdf_exporter import export_to_pdf
from decouple import config

# Configure Gemini
genai.configure(api_key=config("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

async def chat_loop():
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit"}:
            print("Exiting chat...")
            break

        # Get response from Gemini
        response = model.generate_content(user_input)
        print("Gemini:", response.text)

        # Simple intent parsing (demo version)
        if user_input.lower().startswith("search "):
            query = user_input[7:]
            print(f"🔎 Searching DuckDuckGo for: {query}")
            results = await search_duckduckgo(query)
            for r in results[:3]:
                print(r)
                print("-" * 40)

            if "export pdf" in user_input.lower():
                print("📄 Exporting results to PDF...")
                msg = export_to_pdf(results, "search_results.pdf")
                print(msg)

if __name__ == "__main__":
    asyncio.run(chat_loop())
