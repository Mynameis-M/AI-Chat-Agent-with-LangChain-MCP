"""
Phase 4: LangChain Agents (without tools)
Run with: chainlit run app.py -w

This phase introduces LangChain agents - a higher-level abstraction built on
LangGraph that can reason about tasks, use tools, and iterate towards solutions.

In this phase, we create an agent WITHOUT tools to understand the concept.
In Phase 5, we'll add tools to give the agent the ability to take actions.

Key Concepts Introduced:
- LangChain Agents via create_agent()
- Agent vs Chain: Agents can reason and decide what to do next
- Agent streaming with stream_mode for real-time output
- Simplified message format (dict-based instead of LangChain message objects)

Building on Previous Phases:
- Phase 2: Same LLM configuration (ChatOpenAI with GitHub Models)
- Phase 3: Same Chainlit patterns (@cl.on_chat_start, @cl.on_message)
- Phase 3: Same session management (cl.user_session)
- Phase 3: Same streaming pattern for real-time responses

What's New:
- create_agent() replaces direct LLM calls
- Agent handles conversation flow automatically
- Prepared for tool integration in Phase 5

Prerequisites:
- Phase 3 completed (Chainlit chat working)
- langchain package installed (provides create_agent)
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk

load_dotenv()

SYSTEM_PROMPT = """You are a helpful AI assistant named Aria. 
Be friendly and concise. Reply in the same language as the user."""

def get_llm():
    return ChatOpenAI(
        model="openai/gpt-4.1-nano",
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.github.ai/inference",
        temperature=0.7,
    )

def create_assistant_agent():
    llm = get_llm()
    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

@cl.on_chat_start
async def start():
    agent = create_assistant_agent()
    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])
    await cl.Message(content="สวัสดีครับ ผมคือ Aria").send()

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    chat_history = cl.user_session.get("chat_history")
    
    chat_history.append({"role": "user", "content": message.content})
    
    msg = cl.Message(content="")
    full_response = ""
    
    async for stream_mode, data in agent.astream(
        {"messages": chat_history},
        stream_mode=["messages"]
    ):
        if stream_mode == "messages":
            token, _ = data
            if isinstance(token, AIMessageChunk):
                full_response += token.content
                await msg.stream_token(token.content)
    
    await msg.send()
    
    chat_history.append({"role": "assistant", "content": full_response})
    cl.user_session.set("chat_history", chat_history)