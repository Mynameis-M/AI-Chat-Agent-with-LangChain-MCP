# AI Agent System with LangChain & MCP

An AI-powered conversational agent built using LangChain and Chainlit with support for streaming responses, session-based conversation memory, tool-augmented reasoning, and MCP (Model Context Protocol) integration.

The project progressively evolved from a basic LLM connection into a multi-tool AI agent capable of dynamically retrieving external documentation and real-time weather data through both local tools and remote MCP servers.

---

## Features

- Real-time streaming responses using Chainlit
- Session-based conversation memory
- LangChain agent orchestration
- Tool-calling capabilities with external APIs
- MCP integration for dynamic documentation retrieval
- Async multi-tool execution workflow
- Interactive tool execution visualization
- External weather API integration
- Dynamic LangChain documentation search via MCP

---

## Demo

### Multi-tool Agent Workflow

The agent dynamically invokes:
- `get_weather` for real-time weather retrieval
- `search_docs_by_lang_chain` via MCP for LangChain documentation lookup

Example query:

```text
Check Paris weather and explain LangChain agents
```

Example workflow:
1. Agent calls weather tool
2. Agent retrieves weather information
3. Agent calls MCP documentation tool
4. Agent searches LangChain documentation
5. Agent combines both tool outputs into a final response

---

## Screenshots

### AI Agent Chat Interface
<img width="611" height="520" alt="Screenshot 2026-05-25 225021" src="https://github.com/user-attachments/assets/7afbd8e6-e836-4314-9c3d-150f99ca573b" />
">
---

## System Architecture

```text
User
 ↓
Chainlit UI
 ↓
LangChain Agent
 ├── Conversation Memory
 ├── Weather Tool
 └── MCP Tool Server
         ↓
   LangChain Documentation Search
```

---

## Tech Stack

- Python
- LangChain
- Chainlit
- GitHub Models
- WeatherAPI
- MCP (Model Context Protocol)


---

## Project Evolution

The project was developed progressively across multiple phases:

| Phase | Description |
|------|-------------|
| Phase 2 | GitHub Models connection setup |
| Phase 3 | Chainlit chat interface with conversation memory |
| Phase 4 | LangChain agent integration |
| Phase 5 | Tool-augmented agent with weather API |
| Phase 6 | MCP integration with remote documentation tools |

This phased structure demonstrates iterative development and increasing system complexity.

---

## Example: Agent Setup

```python
agent = create_agent(
    model=llm,
    tools=[*TOOLS, *mcp_tools],
    system_prompt=SYSTEM_PROMPT,
)
```

This allows the agent to dynamically:
- reason about tasks
- decide which tools to use
- execute external tools
- integrate tool results into responses

---

## Example: MCP Tool Integration

```python
mcp_client = MultiServerMCPClient(
    {
        "langchain_docs": {
            "transport": "http",
            "url": "https://docs.langchain.com/mcp",
        }
    }
)

mcp_tools = await mcp_client.get_tools()
```

The MCP integration enables dynamic retrieval of external tools from remote MCP servers.

---

## Example: Tool Execution Visualization

```python
if isinstance(msg, AIMessage) and msg.tool_calls:
    for tool_call in msg.tool_calls:
        step = cl.Step(f"🔧 {tool_call['name']}", type="tool")
        step.input = tool_call["args"]
        await step.send()
```

This implementation visualizes the agent's tool usage directly within the Chainlit interface.

---

## Project Structure

```text
AI-Agent-System-with-LangChain-MCP/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── solutions/
│   ├── phase-03-basic-chat-memory/
│   ├── phase-04-langchain-agent/
│   ├── phase-05-agent-tools/
│   └── phase-06-mcp-integration/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Mynameis-M/AI-Chat-Agent-with-LangChain-MCP.git
cd AI-Chat-Agent-with-LangChain-MCP
```

---

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_token
WEATHER_API_KEY=your_weather_api_key
```

---

## Run Application

```bash
chainlit run app.py -w
```

---

## Key Learning Outcomes

Through this project, I explored:

- LLM orchestration using LangChain agents
- Tool-augmented AI workflows
- MCP-based tool integration
- Asynchronous agent execution
- Conversation memory management
- Real-time response streaming
- Dynamic tool discovery
- Interactive AI application development

---
