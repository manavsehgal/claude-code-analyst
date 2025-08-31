# Claude Code Agent Chat Application

This document covers the Claude Code Agent Chat application and the underlying agent package that powers AI-powered Streamlit interfaces.

## Overview

The chat application (`apps/chat.py`) leverages the headless Claude Code SDK to provide an interactive chat interface with comprehensive authentication support, session management, and progress indicators.

## Project Structure

```
apps/
├── agent/              # Reusable agent capabilities package
│   ├── __init__.py
│   ├── client.py      # Core Claude agent client
│   ├── session.py     # Session management
│   ├── tools.py       # Tool permissions manager
│   ├── mcp.py         # MCP server management
│   ├── auth.py        # Authentication management
│   └── subagents.py   # Subagent delegation
└── chat.py            # Chat application
```

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Install Claude Code SDK prerequisites:
```bash
npm install -g @anthropic-ai/claude-code
```

3. Run the chat app:
```bash
uv run streamlit run apps/chat.py
```

## Agent Package Components

### ClaudeAgent (client.py)
The main interface for interacting with Claude Code in headless mode.

```python
from apps.agent import ClaudeAgent, AgentConfig, AuthManager

# Basic usage
config = AgentConfig(
    system_prompt="You are a helpful assistant",
    allowed_tools=["Read", "Grep"],
    permission_mode=PermissionMode.DEFAULT
)

agent = ClaudeAgent(config)

# With authentication detection
auth_manager = AuthManager()
agent = ClaudeAgent(config, auth_manager=auth_manager)

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

### AuthManager (auth.py)
Detects and manages authentication methods for Claude Code.

```python
from apps.agent import AuthManager, AuthMethod

auth_manager = AuthManager()

# Detect current authentication method
auth_status = auth_manager.detect_auth_method()

print(f"Method: {auth_status.method.value}")
print(f"Authenticated: {auth_status.is_authenticated}")
print(f"Details: {auth_status.details}")

# Get configuration instructions
if not auth_status.is_authenticated:
    instructions = auth_manager.get_configuration_instructions(auth_status.method)
    print(instructions)

# Get auth config for ClaudeAgent
auth_config = auth_manager.get_auth_config()
```

Supported authentication methods:
- `ANTHROPIC_API`: Direct API key authentication
- `AMAZON_BEDROCK`: AWS Bedrock with AWS credentials
- `CLAUDE_ACCOUNT`: Pro/Max subscription login via CLI

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

## Chat Application Features

The chat application (`apps/chat.py`) provides:

- **Interactive Chat Interface**: Streamlit-based chat UI with message history
- **Authentication Management**: Automatic detection and configuration guidance for all three Claude Code authentication methods
- **Progress Indicators**: Visual feedback during response processing with animated spinner
- **Session Management**: Conversation persistence across app restarts
- **Tool Control**: Configurable tool permissions via sidebar
- **Subagent Integration**: Access to specialized AI agents for different tasks

## Authentication Configuration

Claude Code supports three authentication methods:

### 1. Anthropic API (Direct API Key)
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_API_BASE="https://api.anthropic.com"  # Optional
```

### 2. Amazon Bedrock
```bash
# Configure AWS credentials (one of these methods):
aws configure
# OR
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"

# Enable Bedrock mode
export CLAUDE_CODE_USE_BEDROCK=1

# Optional: Configure models
export CLAUDE_CODE_PRIMARY_MODEL="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
export CLAUDE_CODE_SMALL_MODEL="us.anthropic.claude-3-5-haiku-20241022-v1:0"
```

### 3. Claude Account (Pro/Max Subscription)
```bash
# Install and authenticate
npm install -g @anthropic-ai/claude-code
claude login

# Check status
claude status
```

The chat application automatically detects which method is configured and displays the status in the sidebar.

## Creating Custom Applications

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

## Requirements

- Python >=3.13
- Node.js 18+
- Claude Code CLI installed
- Valid Claude subscription (Pro or Max plan)

## Technical Notes

- The agent package is designed for headless operation
- Sessions are persisted locally in `~/.claude_sessions/`
- MCP configurations are stored in `.mcp.json`
- Subagent configs are in `.claude/subagents.json`
- Authentication status is checked on-demand to optimize app startup performance
- Progress indicators use Streamlit's native spinner component for reliable UX