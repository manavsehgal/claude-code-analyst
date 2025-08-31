"""
Claude Code Agent Package

Reusable capabilities for Streamlit apps using headless Claude Code SDK.
"""

from .auth import AuthManager, AuthMethod, AuthStatus
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
    "AuthManager",
    "AuthMethod",
    "AuthStatus",
]

__version__ = "0.1.0"
