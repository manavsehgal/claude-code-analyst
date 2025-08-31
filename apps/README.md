# Claude Code Agent Apps

This directory contains Streamlit applications that leverage the headless Claude Code SDK for building AI-powered interfaces.

## Structure

```
apps/
├── agent/              # Reusable agent capabilities package
│   ├── __init__.py
│   ├── client.py      # Core Claude agent client
│   ├── session.py     # Session management
│   ├── tools.py       # Tool permissions manager
│   ├── mcp.py         # MCP server management
│   └── subagents.py   # Subagent delegation
└── example_chat.py    # Example chat application
```

## Agent Package Components

### ClaudeAgent (client.py)
The main interface for interacting with Claude Code in headless mode.

```python
from apps.agent import ClaudeAgent, AgentConfig

config = AgentConfig(
    system_prompt="You are a helpful assistant",
    allowed_tools=["Read", "Grep"],
    permission_mode=PermissionMode.DEFAULT
)

agent = ClaudeAgent(config)

# Synchronous query
response = await agent.query_sync("Analyze this codebase")

# Streaming query
async for chunk in agent.query("Explain this function"):
    print(chunk)
```

### SessionManager (session.py)
Manages conversation sessions with persistence.

```python
from apps.agent import SessionManager

manager = SessionManager()
session = manager.create_session("Code Review Session")
manager.add_turn("user", "Review this function")
manager.add_turn("assistant", "Here's my analysis...")
```

### ToolManager (tools.py)
Controls which tools Claude can use with predefined profiles.

```python
from apps.agent import ToolManager

tools = ToolManager()
tools.apply_profile("code_analysis")  # Read-only analysis
tools.apply_profile("code_editing")   # Allow edits
tools.apply_profile("full_access")    # All tools
```

Available profiles:
- `read_only`: Only reading and searching
- `code_analysis`: Analysis without modifications
- `code_editing`: Code changes allowed
- `full_access`: All tools available
- `web_research`: Web search and fetch only
- `safe_execution`: Limited execution capabilities

### MCPServer (mcp.py)
Manages Model Context Protocol server connections.

```python
from apps.agent import MCPServer

mcp = MCPServer()
mcp.add_server(MCPServer.create_http_server(
    name="github",
    url="https://api.github.com/mcp"
))
```

### SubAgentManager (subagents.py)
Handles specialized subagents for task delegation.

```python
from apps.agent import SubAgentManager

subagents = SubAgentManager()
agent = subagents.get_agent("code_reviewer")
suggested = subagents.suggest_agent_for_task("debug this error")
```

Built-in subagents:
- `code_reviewer`: Code quality and security review
- `debugger`: Error analysis and fixes
- `test_writer`: Comprehensive test creation
- `documentation_writer`: Technical documentation
- `performance_optimizer`: Performance improvements
- `security_auditor`: Security vulnerability detection

## Running the Example App

1. Install dependencies:
```bash
uv sync
```

2. Install Claude Code SDK prerequisites:
```bash
npm install -g @anthropic-ai/claude-code
```

3. Run the example chat app:
```bash
uv run streamlit run apps/example_chat.py
```

## Creating Your Own App

1. Import the agent package:
```python
from apps.agent import (
    ClaudeAgent, 
    AgentConfig,
    SessionManager,
    ToolManager,
    SubAgentManager
)
```

2. Configure the agent:
```python
config = AgentConfig(
    system_prompt="Your custom prompt",
    allowed_tools=["Read", "Write"],
    output_format=OutputFormat.TEXT
)
```

3. Use in your Streamlit app:
```python
agent = ClaudeAgent(config)
response = await agent.query_sync(user_input)
st.write(response)
```

## Environment Variables

For Amazon Bedrock integration:
```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
```

## Requirements

- Python >=3.13
- Node.js 18+
- Claude Code CLI installed
- Valid Claude subscription (Pro or Max plan)

## Notes

- The agent package is designed for headless operation
- Sessions are persisted locally in `~/.claude_sessions/`
- MCP configurations are stored in `.mcp.json`
- Subagent configs are in `.claude/subagents.json`