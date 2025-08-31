"""
MCP Server Manager for Claude Code Agent

Manages Model Context Protocol (MCP) server connections and configurations.
"""

import json
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class ServerType(Enum):
    """Types of MCP servers."""

    STDIO = "stdio"  # Local process servers
    SSE = "sse"  # Server-Sent Events (streaming)
    HTTP = "http"  # Standard HTTP servers


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    type: ServerType
    command: str | None = None  # For stdio servers
    url: str | None = None  # For SSE/HTTP servers
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    auth: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class MCPServer:
    """Manages MCP server connections for Claude Code."""

    def __init__(self, config_dir: Path | None = None):
        """
        Initialize MCP server manager.

        Args:
            config_dir: Directory for MCP configurations. Defaults to current directory.
        """
        self.config_dir = config_dir or Path.cwd()
        self.servers: dict[str, MCPServerConfig] = {}
        self.load_project_config()

    def load_project_config(self):
        """Load MCP configuration from .mcp.json if it exists."""
        config_file = self.config_dir / ".mcp.json"

        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                    self._parse_config(config)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load .mcp.json: {e}")

    def _parse_config(self, config: dict[str, Any]):
        """Parse MCP configuration from JSON."""
        servers = config.get("servers", {})

        for name, server_config in servers.items():
            server_type = ServerType(server_config.get("type", "stdio"))

            self.servers[name] = MCPServerConfig(
                name=name,
                type=server_type,
                command=server_config.get("command"),
                url=server_config.get("url"),
                args=server_config.get("args", []),
                env=server_config.get("env", {}),
                auth=server_config.get("auth"),
                metadata=server_config.get("metadata", {}),
            )

    def add_server(self, config: MCPServerConfig):
        """Add a new MCP server configuration."""
        self.servers[config.name] = config

    def remove_server(self, name: str):
        """Remove an MCP server configuration."""
        if name in self.servers:
            del self.servers[name]

    def get_server(self, name: str) -> MCPServerConfig | None:
        """Get a specific server configuration."""
        return self.servers.get(name)

    def list_servers(self) -> list[str]:
        """List all configured server names."""
        return list(self.servers.keys())

    def save_project_config(self):
        """Save MCP configuration to .mcp.json."""
        config_file = self.config_dir / ".mcp.json"

        config = {"servers": {}}

        for name, server in self.servers.items():
            server_dict = {"type": server.type.value}

            if server.command:
                server_dict["command"] = server.command
            if server.url:
                server_dict["url"] = server.url
            if server.args:
                server_dict["args"] = server.args
            if server.env:
                server_dict["env"] = server.env
            if server.auth:
                server_dict["auth"] = server.auth
            if server.metadata:
                server_dict["metadata"] = server.metadata

            config["servers"][name] = server_dict

        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

    def configure_server_cli(self, name: str, server_type: str, **kwargs):
        """
        Configure an MCP server using Claude CLI.

        Args:
            name: Server name
            server_type: Server type (stdio, sse, http)
            **kwargs: Additional configuration options
        """
        cmd = ["claude", "mcp", "add", name, "--type", server_type]

        # Add optional parameters
        if "command" in kwargs:
            cmd.extend(["--command", kwargs["command"]])
        if "url" in kwargs:
            cmd.extend(["--url", kwargs["url"]])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Reload configuration
                self.load_project_config()
                return True
            else:
                print(f"Failed to configure server: {result.stderr}")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error configuring server: {e}")
            return False

    def list_available_servers_cli(self) -> list[dict[str, str]]:
        """List available MCP servers using Claude CLI."""
        try:
            result = subprocess.run(["claude", "mcp", "list"], capture_output=True, text=True)

            if result.returncode == 0:
                # Parse the output (assuming JSON format)
                try:
                    servers = json.loads(result.stdout)
                    # Ensure proper typing
                    if isinstance(servers, list):
                        return servers
                    return [{"output": str(servers)}]
                except json.JSONDecodeError:
                    # If not JSON, return raw output
                    return [{"output": result.stdout}]
            else:
                return []
        except subprocess.CalledProcessError:
            return []

    def authenticate_server(self, name: str) -> bool:
        """
        Authenticate with an MCP server using Claude CLI.

        Args:
            name: Server name to authenticate

        Returns:
            True if authentication successful
        """
        try:
            result = subprocess.run(["claude", "mcp", "auth", name], capture_output=True, text=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def get_server_status(self, name: str) -> dict[str, Any]:
        """
        Get status of an MCP server.

        Args:
            name: Server name

        Returns:
            Status information dictionary
        """
        server = self.servers.get(name)
        if not server:
            return {"status": "not_configured"}

        return {
            "name": server.name,
            "type": server.type.value,
            "configured": True,
            "auth_required": server.auth is not None,
            "metadata": server.metadata,
        }

    @staticmethod
    def create_stdio_server(name: str, command: str, args: list[str] | None = None) -> MCPServerConfig:
        """Helper to create a stdio server configuration."""
        return MCPServerConfig(name=name, type=ServerType.STDIO, command=command, args=args or [])

    @staticmethod
    def create_http_server(name: str, url: str, auth: dict[str, str] | None = None) -> MCPServerConfig:
        """Helper to create an HTTP server configuration."""
        return MCPServerConfig(name=name, type=ServerType.HTTP, url=url, auth=auth)

    @staticmethod
    def create_sse_server(name: str, url: str, auth: dict[str, str] | None = None) -> MCPServerConfig:
        """Helper to create an SSE server configuration."""
        return MCPServerConfig(name=name, type=ServerType.SSE, url=url, auth=auth)
