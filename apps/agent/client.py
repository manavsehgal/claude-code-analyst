"""
Claude Code Agent Client

Core client module for interacting with Claude Code SDK in headless mode.
"""

import asyncio
import json
import subprocess
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class OutputFormat(Enum):
    """Output format options for Claude Code responses."""

    TEXT = "text"
    JSON = "json"
    STREAMING_JSON = "streaming-json"


class PermissionMode(Enum):
    """Permission modes for Claude Code operations."""

    ACCEPT_EDITS = "acceptEdits"
    BYPASS_PERMISSIONS = "bypassPermissions"
    DEFAULT = "default"
    PLAN = "plan"


@dataclass
class AgentConfig:
    """Configuration for Claude Code agent."""

    system_prompt: str | None = None
    allowed_tools: list[str] = field(default_factory=list)
    disallowed_tools: list[str] = field(default_factory=list)
    permission_mode: PermissionMode = PermissionMode.DEFAULT
    output_format: OutputFormat = OutputFormat.TEXT
    max_turns: int = 10
    working_directory: Path | None = None
    use_bedrock: bool = False
    aws_region: str | None = None
    model: str | None = None
    environment: dict[str, str] = field(default_factory=dict)


class ClaudeAgent:
    """Main client for interacting with Claude Code SDK."""

    def __init__(self, config: AgentConfig | None = None):
        """Initialize Claude Agent with configuration."""
        self.config = config or AgentConfig()
        self.conversation_id: str | None = None
        self._process: subprocess.Popen | None = None

    async def query(self, prompt: str, resume_id: str | None = None) -> AsyncIterator[str]:
        """
        Execute a query to Claude Code in headless mode.

        Args:
            prompt: The prompt to send to Claude
            resume_id: Optional conversation ID to resume

        Yields:
            Response chunks from Claude
        """
        cmd = self._build_command(prompt, resume_id)

        # Set up environment
        env = self._prepare_environment()

        # Execute command
        async for chunk in self._execute_command(cmd, env):
            yield chunk

    async def query_sync(self, prompt: str, resume_id: str | None = None) -> str:
        """
        Execute a synchronous query to Claude Code.

        Args:
            prompt: The prompt to send to Claude
            resume_id: Optional conversation ID to resume

        Returns:
            Complete response from Claude
        """
        response_parts = []
        async for chunk in self.query(prompt, resume_id):
            response_parts.append(chunk)
        return "".join(response_parts)

    def _build_command(self, prompt: str, resume_id: str | None = None) -> list[str]:
        """Build the Claude command with all configuration options."""
        cmd = ["claude", "-p", prompt]

        # Add output format
        cmd.extend(["--output-format", self.config.output_format.value])

        # Add permission mode
        cmd.extend(["--permission-mode", self.config.permission_mode.value])

        # Add system prompt if provided
        if self.config.system_prompt:
            cmd.extend(["--appendSystemPrompt", self.config.system_prompt])

        # Add allowed tools
        if self.config.allowed_tools:
            cmd.extend(["--allowedTools", ",".join(self.config.allowed_tools)])

        # Add disallowed tools
        if self.config.disallowed_tools:
            cmd.extend(["--disallowedTools", ",".join(self.config.disallowed_tools)])

        # Add resume ID if provided
        if resume_id:
            cmd.extend(["--resume", resume_id])
        elif self.conversation_id:
            cmd.extend(["--resume", self.conversation_id])

        # Add model if specified
        if self.config.model:
            cmd.extend(["--model", self.config.model])

        return cmd

    def _prepare_environment(self) -> dict[str, str]:
        """Prepare environment variables for Claude execution."""
        import os

        env = os.environ.copy()

        # Add custom environment variables
        env.update(self.config.environment)

        # Set Bedrock configuration if enabled
        if self.config.use_bedrock:
            env["CLAUDE_CODE_USE_BEDROCK"] = "1"
            if self.config.aws_region:
                env["AWS_REGION"] = self.config.aws_region

        return env

    async def _execute_command(self, cmd: list[str], env: dict[str, str]) -> AsyncIterator[str]:
        """Execute Claude command and yield response chunks."""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=self.config.working_directory,
        )

        # Handle streaming output
        if self.config.output_format == OutputFormat.STREAMING_JSON:
            async for line in self._read_streaming_output(process):
                yield line
        else:
            # Read complete output
            stdout, stderr = await process.communicate()
            if stdout:
                yield stdout.decode()
            if stderr and process.returncode != 0:
                raise RuntimeError(f"Claude command failed: {stderr.decode()}")

    async def _read_streaming_output(self, process: asyncio.subprocess.Process) -> AsyncIterator[str]:
        """Read and parse streaming JSON output from Claude."""
        if not process.stdout:
            return

        while True:
            line = await process.stdout.readline()
            if not line:
                break

            try:
                # Parse JSON line
                data = json.loads(line.decode().strip())

                # Extract conversation ID if present
                if "conversationId" in data:
                    self.conversation_id = data["conversationId"]

                # Yield content if present
                if "content" in data:
                    yield data["content"]

            except json.JSONDecodeError:
                # Skip non-JSON lines
                continue

    async def continue_conversation(self, prompt: str) -> AsyncIterator[str]:
        """Continue the most recent conversation."""
        if not self.conversation_id:
            raise ValueError("No conversation to continue. Execute a query first.")

        async for chunk in self.query(prompt, self.conversation_id):
            yield chunk

    def reset_conversation(self):
        """Reset the conversation state."""
        self.conversation_id = None
