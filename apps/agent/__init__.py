"""
Claude Code Agent Package

Reusable capabilities for Streamlit apps using headless Claude Code SDK.
"""

from .client import AgentConfig, ClaudeAgent
from .mcp import MCPServer
from .session import SessionManager
from .subagents import SubAgentManager
from .tools import ToolManager

__all__ = [
    "ClaudeAgent",
    "AgentConfig",
    "SessionManager",
    "ToolManager",
    "MCPServer",
    "SubAgentManager",
]

__version__ = "0.1.0"
