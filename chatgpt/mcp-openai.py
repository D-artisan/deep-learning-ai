import os
import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']


client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "deepwiki",
            "server_url": "https://mcp.deepwiki.com/mcp",
            "require_approval": "never",
        },
    ],
    input="What transport protocols are supported in the 2025-03-26 version of the MCP spec?",
)

with open("mcp-openai.md", "w", encoding="utf-8") as f:
    f.write("# MCP OpenAI Response\n\n")
    f.write(resp.output_text.strip() + "\n")
print("Response written to mcp-openai.md")