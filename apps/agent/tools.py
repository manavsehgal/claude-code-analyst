"""
Tool Manager for Claude Code Agent

Manages tool permissions and configurations for Claude Code interactions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Tool(Enum):
    """Available tools in Claude Code."""

    BASH = "Bash"
    EDIT = "Edit"
    MULTI_EDIT = "MultiEdit"
    READ = "Read"
    WRITE = "Write"
    TODO_WRITE = "TodoWrite"
    GREP = "Grep"
    GLOB = "Glob"
    WEB_SEARCH = "WebSearch"
    WEB_FETCH = "WebFetch"
    TASK = "Task"
    EXIT_PLAN_MODE = "ExitPlanMode"
    NOTEBOOK_EDIT = "NotebookEdit"
    BASH_OUTPUT = "BashOutput"
    KILL_BASH = "KillBash"


@dataclass
class ToolProfile:
    """Predefined tool profile for common use cases."""

    name: str
    description: str
    allowed_tools: list[Tool]
    disallowed_tools: list[Tool]


class ToolManager:
    """Manages tool permissions and profiles for Claude Code."""

    # Predefined tool profiles for common scenarios
    PROFILES = {
        "read_only": ToolProfile(
            name="Read Only",
            description="Only allows reading and searching operations",
            allowed_tools=[Tool.READ, Tool.GREP, Tool.GLOB, Tool.WEB_SEARCH, Tool.WEB_FETCH],
            disallowed_tools=[Tool.BASH, Tool.EDIT, Tool.MULTI_EDIT, Tool.WRITE, Tool.NOTEBOOK_EDIT],
        ),
        "code_analysis": ToolProfile(
            name="Code Analysis",
            description="For analyzing and understanding codebases",
            allowed_tools=[Tool.READ, Tool.GREP, Tool.GLOB, Tool.TODO_WRITE, Tool.TASK],
            disallowed_tools=[Tool.BASH, Tool.EDIT, Tool.MULTI_EDIT, Tool.WRITE],
        ),
        "code_editing": ToolProfile(
            name="Code Editing",
            description="For making code changes and refactoring",
            allowed_tools=[Tool.READ, Tool.EDIT, Tool.MULTI_EDIT, Tool.WRITE, Tool.GREP, Tool.GLOB, Tool.TODO_WRITE],
            disallowed_tools=[Tool.BASH],
        ),
        "full_access": ToolProfile(
            name="Full Access", description="All tools available", allowed_tools=list(Tool), disallowed_tools=[]
        ),
        "web_research": ToolProfile(
            name="Web Research",
            description="For web-based research and information gathering",
            allowed_tools=[Tool.WEB_SEARCH, Tool.WEB_FETCH, Tool.TODO_WRITE],
            disallowed_tools=[Tool.BASH, Tool.EDIT, Tool.MULTI_EDIT, Tool.WRITE, Tool.READ],
        ),
        "safe_execution": ToolProfile(
            name="Safe Execution",
            description="Allows code execution with safety restrictions",
            allowed_tools=[Tool.READ, Tool.GREP, Tool.GLOB, Tool.BASH_OUTPUT, Tool.TODO_WRITE],
            disallowed_tools=[Tool.BASH, Tool.EDIT, Tool.WRITE, Tool.KILL_BASH],
        ),
    }

    def __init__(self):
        """Initialize tool manager."""
        self.allowed_tools: set[Tool] = set()
        self.disallowed_tools: set[Tool] = set()
        self.custom_permissions: dict[str, Any] = {}

    def apply_profile(self, profile_name: str):
        """
        Apply a predefined tool profile.

        Args:
            profile_name: Name of the profile to apply
        """
        if profile_name not in self.PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}. Available: {list(self.PROFILES.keys())}")

        profile = self.PROFILES[profile_name]
        self.allowed_tools = set(profile.allowed_tools)
        self.disallowed_tools = set(profile.disallowed_tools)

    def allow_tools(self, tools: list[Tool]):
        """Add tools to the allowed list."""
        self.allowed_tools.update(tools)
        # Remove from disallowed if present
        self.disallowed_tools.difference_update(tools)

    def disallow_tools(self, tools: list[Tool]):
        """Add tools to the disallowed list."""
        self.disallowed_tools.update(tools)
        # Remove from allowed if present
        self.allowed_tools.difference_update(tools)

    def get_allowed_tools_string(self) -> str:
        """Get comma-separated string of allowed tools for Claude command."""
        return ",".join(tool.value for tool in self.allowed_tools)

    def get_disallowed_tools_string(self) -> str:
        """Get comma-separated string of disallowed tools for Claude command."""
        return ",".join(tool.value for tool in self.disallowed_tools)

    def is_tool_allowed(self, tool: Tool) -> bool:
        """Check if a specific tool is allowed."""
        if tool in self.disallowed_tools:
            return False
        if self.allowed_tools:
            return tool in self.allowed_tools
        return True

    def get_profile_info(self, profile_name: str) -> dict[str, Any]:
        """Get information about a specific profile."""
        if profile_name not in self.PROFILES:
            return {}

        profile = self.PROFILES[profile_name]
        return {
            "name": profile.name,
            "description": profile.description,
            "allowed_tools": [tool.value for tool in profile.allowed_tools],
            "disallowed_tools": [tool.value for tool in profile.disallowed_tools],
        }

    def list_profiles(self) -> list[str]:
        """List all available tool profiles."""
        return list(self.PROFILES.keys())

    def create_custom_profile(self, name: str, description: str, allowed: list[Tool], disallowed: list[Tool]):
        """
        Create a custom tool profile.

        Args:
            name: Profile name
            description: Profile description
            allowed: List of allowed tools
            disallowed: List of disallowed tools
        """
        self.PROFILES[name] = ToolProfile(
            name=name, description=description, allowed_tools=allowed, disallowed_tools=disallowed
        )

    def reset(self):
        """Reset tool permissions to default (all allowed)."""
        self.allowed_tools.clear()
        self.disallowed_tools.clear()
        self.custom_permissions.clear()
