"""
SubAgent Manager for Claude Code Agent

Manages specialized subagents for delegating specific tasks.
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class SubAgentScope(Enum):
    """Scope of subagent availability."""

    PROJECT = "project"  # Available only in current project
    USER = "user"  # Available across all projects


@dataclass
class SubAgent:
    """Represents a specialized subagent."""

    name: str
    description: str
    system_prompt: str
    tools: list[str] = field(default_factory=list)
    scope: SubAgentScope = SubAgentScope.PROJECT
    proactive: bool = False  # Whether to proactively suggest this agent
    metadata: dict[str, Any] = field(default_factory=dict)


class SubAgentManager:
    """Manages specialized subagents for task delegation."""

    # Predefined subagents for common scenarios
    BUILTIN_AGENTS = {
        "code_reviewer": SubAgent(
            name="Code Reviewer",
            description="Expert code review specialist",
            system_prompt="""You are an expert code reviewer. Your role is to:
1. Review code for quality, security, and maintainability
2. Identify potential bugs and edge cases
3. Suggest improvements and best practices
4. Check for proper error handling
5. Ensure code follows project conventions""",
            tools=["Read", "Grep", "Glob", "TodoWrite"],
            proactive=True,
        ),
        "debugger": SubAgent(
            name="Debugger",
            description="Debugging specialist for errors and test failures",
            system_prompt="""You are a debugging specialist. Your role is to:
1. Analyze error messages and stack traces
2. Identify root causes of failures
3. Suggest fixes with explanations
4. Add appropriate logging and error handling
5. Write or update tests to prevent regressions""",
            tools=["Read", "Edit", "MultiEdit", "Grep", "Bash", "TodoWrite"],
            proactive=True,
        ),
        "test_writer": SubAgent(
            name="Test Writer",
            description="Specialist in writing comprehensive tests",
            system_prompt="""You are a testing specialist. Your role is to:
1. Write comprehensive unit tests
2. Create integration tests
3. Design edge case scenarios
4. Ensure high test coverage
5. Follow testing best practices and project conventions""",
            tools=["Read", "Write", "Edit", "Grep", "Glob", "Bash"],
            proactive=False,
        ),
        "documentation_writer": SubAgent(
            name="Documentation Writer",
            description="Technical documentation specialist",
            system_prompt="""You are a technical documentation specialist. Your role is to:
1. Write clear, comprehensive documentation
2. Create API documentation with examples
3. Write user guides and tutorials
4. Document code with appropriate comments
5. Maintain README files and project documentation""",
            tools=["Read", "Write", "Edit", "Grep", "Glob"],
            proactive=False,
        ),
        "performance_optimizer": SubAgent(
            name="Performance Optimizer",
            description="Performance analysis and optimization specialist",
            system_prompt="""You are a performance optimization specialist. Your role is to:
1. Identify performance bottlenecks
2. Optimize algorithms and data structures
3. Reduce memory usage
4. Improve response times
5. Add performance monitoring and metrics""",
            tools=["Read", "Edit", "MultiEdit", "Bash", "Grep", "TodoWrite"],
            proactive=False,
        ),
        "security_auditor": SubAgent(
            name="Security Auditor",
            description="Security analysis and vulnerability detection specialist",
            system_prompt="""You are a security auditing specialist. Your role is to:
1. Identify security vulnerabilities
2. Check for common security issues (SQL injection, XSS, etc.)
3. Review authentication and authorization
4. Ensure secure data handling
5. Suggest security improvements and best practices""",
            tools=["Read", "Grep", "Glob", "TodoWrite"],
            proactive=True,
        ),
    }

    def __init__(self, config_dir: Path | None = None):
        """
        Initialize subagent manager.

        Args:
            config_dir: Directory for subagent configurations
        """
        self.config_dir = config_dir or Path.cwd() / ".claude"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.project_agents: dict[str, SubAgent] = {}
        self.user_agents: dict[str, SubAgent] = {}

        self.load_agents()

    def load_agents(self):
        """Load subagent configurations from disk."""
        # Load project-level agents
        project_config = self.config_dir / "subagents.json"
        if project_config.exists():
            self._load_agents_from_file(project_config, SubAgentScope.PROJECT)

        # Load user-level agents
        user_config = Path.home() / ".claude" / "subagents.json"
        if user_config.exists():
            self._load_agents_from_file(user_config, SubAgentScope.USER)

    def _load_agents_from_file(self, file_path: Path, scope: SubAgentScope):
        """Load agents from a JSON file."""
        try:
            with open(file_path) as f:
                data = json.load(f)

            for agent_data in data.get("agents", []):
                agent = SubAgent(
                    name=agent_data["name"],
                    description=agent_data["description"],
                    system_prompt=agent_data["system_prompt"],
                    tools=agent_data.get("tools", []),
                    scope=scope,
                    proactive=agent_data.get("proactive", False),
                    metadata=agent_data.get("metadata", {}),
                )

                if scope == SubAgentScope.PROJECT:
                    self.project_agents[agent.name] = agent
                else:
                    self.user_agents[agent.name] = agent

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Failed to load agents from {file_path}: {e}")

    def save_agents(self, scope: SubAgentScope = SubAgentScope.PROJECT):
        """Save agent configurations to disk."""
        if scope == SubAgentScope.PROJECT:
            config_file = self.config_dir / "subagents.json"
            agents = self.project_agents
        else:
            config_file = Path.home() / ".claude" / "subagents.json"
            config_file.parent.mkdir(parents=True, exist_ok=True)
            agents = self.user_agents

        data = {
            "agents": [
                {
                    "name": agent.name,
                    "description": agent.description,
                    "system_prompt": agent.system_prompt,
                    "tools": agent.tools,
                    "proactive": agent.proactive,
                    "metadata": agent.metadata,
                }
                for agent in agents.values()
            ]
        }

        with open(config_file, "w") as f:
            json.dump(data, f, indent=2)

    def create_agent(self, agent: SubAgent):
        """Create a new subagent."""
        if agent.scope == SubAgentScope.PROJECT:
            self.project_agents[agent.name] = agent
        else:
            self.user_agents[agent.name] = agent

        self.save_agents(agent.scope)

    def get_agent(self, name: str) -> SubAgent | None:
        """Get a subagent by name."""
        # Check project agents first, then user agents, then builtin
        return self.project_agents.get(name) or self.user_agents.get(name) or self.BUILTIN_AGENTS.get(name)

    def list_agents(self) -> dict[str, list[str]]:
        """List all available agents organized by scope."""
        return {
            "builtin": list(self.BUILTIN_AGENTS.keys()),
            "project": list(self.project_agents.keys()),
            "user": list(self.user_agents.keys()),
        }

    def get_proactive_agents(self) -> list[SubAgent]:
        """Get all agents marked as proactive."""
        agents = []

        # Check all agent sources
        for agent in self.BUILTIN_AGENTS.values():
            if agent.proactive:
                agents.append(agent)

        for agent in self.project_agents.values():
            if agent.proactive:
                agents.append(agent)

        for agent in self.user_agents.values():
            if agent.proactive:
                agents.append(agent)

        return agents

    def suggest_agent_for_task(self, task_description: str) -> SubAgent | None:
        """
        Suggest the most appropriate agent for a given task.

        Args:
            task_description: Description of the task

        Returns:
            Suggested agent or None
        """
        task_lower = task_description.lower()

        # Simple keyword matching for demonstration
        # In practice, this could use more sophisticated matching
        if any(word in task_lower for word in ["review", "quality", "check"]):
            return self.get_agent("code_reviewer")
        elif any(word in task_lower for word in ["debug", "error", "fix", "bug"]):
            return self.get_agent("debugger")
        elif any(word in task_lower for word in ["test", "testing", "coverage"]):
            return self.get_agent("test_writer")
        elif any(word in task_lower for word in ["document", "docs", "readme"]):
            return self.get_agent("documentation_writer")
        elif any(word in task_lower for word in ["performance", "optimize", "speed"]):
            return self.get_agent("performance_optimizer")
        elif any(word in task_lower for word in ["security", "vulnerability", "audit"]):
            return self.get_agent("security_auditor")

        return None

    def delete_agent(self, name: str, scope: SubAgentScope):
        """Delete a subagent."""
        if scope == SubAgentScope.PROJECT and name in self.project_agents:
            del self.project_agents[name]
            self.save_agents(scope)
        elif scope == SubAgentScope.USER and name in self.user_agents:
            del self.user_agents[name]
            self.save_agents(scope)
