import asyncio
import os
import json
import logging
from typing import List
from github import Github
from github.ContentFile import ContentFile
from github.GithubException import GithubException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from anyio import ClosedResourceError
import urllib.parse
import subprocess
import traceback


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

base_url = os.getenv("CORAL_SSE_URL")
agentID = os.getenv("CORAL_AGENT_ID")

params = {
    # "waitForAgents": 1,
    "agentId": agentID,
    "agentDescription": """BlackboxAI agent. Responsible for creating code."""
}
query_string = urllib.parse.urlencode(params)
MCP_SERVER_URL = f"{base_url}?{query_string}"

def get_tools_description(tools):
    return "\n".join(f"Tool: {t.name}, Schema: {json.dumps(t.args).replace('{', '{{').replace('}', '}}')}" for t in tools)

async def create_blackboxai_agent(client, tools):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are `blackboxai_agent`, responsible for code related task. Follow this workflow:

        **Important: NEVER EVER end up the chain**
        
        1. Use `wait_for_mentions(timeoutMs=60000)` to wait for instructions from other agents.**
        2. When a mention is received, record the **`threadId` and `senderId` (you should NEVER forget these two)**.
        3. Think about sender's query, try your best to solve it.
        4. Use `send_message(senderId=..., mentions=[senderId], threadId=..., content=...)` to reply to the sender with your answer.
        5. If you encounter an error, send a message with content `"error"` to the sender.
        6. Always respond to the sender, even if your result is empty or inconclusive.
        7. Wait 2 seconds and repeat from step 1.
         
        **Important: NEVER EVER end up the chain**
        
        Tools: {get_tools_description(tools)}"""),
        ("placeholder", "{history}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    model = ChatOpenAI(
        openai_api_key=os.getenv("BLACKBOXAI_API_KEY"),
        base_url=os.getenv("BLACKBOXAI_URL"),
        model_name=os.getenv("MODEL_NAME")
    )

    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, max_iterations=None ,verbose=True)

async def main():
    CORAL_SERVER_URL = f"{base_url}?{query_string}"
    logger.info(f"Connecting to Coral Server: {CORAL_SERVER_URL}")

    client = MultiServerMCPClient(
        connections={
            "coral": {
                "transport": "sse",
                "url": CORAL_SERVER_URL,
                "timeout": 600,
                "sse_read_timeout": 600,
            }
        }
    )
    logger.info("Coral Server Connection Established")

    tools = await client.get_tools()
    coral_tool_names = [
        "list_agents",
        "create_thread",
        "add_participant",
        "remove_participant",
        "close_thread",
        "send_message",
        "wait_for_mentions",
    ]
    tools = [tool for tool in tools if tool.name in coral_tool_names]

    logger.info(f"Tools Description:\n{get_tools_description(tools)}")

    agent_executor = await create_blackboxai_agent(client, tools)

    while True:
        try:
            logger.info("Starting new agent invocation")
            await agent_executor.ainvoke({"agent_scratchpad": []})
            logger.info("Completed agent invocation, restarting loop")
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in agent loop: {str(e)}")
            logger.error(traceback.format_exc())
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
