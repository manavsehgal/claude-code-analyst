"""
Authentication Manager for Claude Code Agent

Detects and manages different authentication methods for Claude Code.
"""

import json
import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class AuthMethod(Enum):
    """Available authentication methods for Claude Code."""

    ANTHROPIC_API = "anthropic_api"
    AMAZON_BEDROCK = "amazon_bedrock"
    CLAUDE_ACCOUNT = "claude_account"
    NONE = "none"


@dataclass
class AuthStatus:
    """Status of Claude Code authentication."""

    method: AuthMethod
    is_authenticated: bool
    details: dict[str, Any]
    error: str | None = None


class AuthManager:
    """Manages authentication detection and configuration for Claude Code."""

    def __init__(self):
        """Initialize authentication manager."""
        self.current_status: AuthStatus | None = None

    def detect_auth_method(self) -> AuthStatus:
        """
        Detect which authentication method is currently active.

        Returns:
            AuthStatus with detected method and authentication status
        """
        # Check for Amazon Bedrock configuration
        if self._is_bedrock_configured():
            return self._check_bedrock_auth()

        # Check for Anthropic API key
        if self._is_anthropic_api_configured():
            return self._check_anthropic_api_auth()

        # Check for Claude account authentication
        if self._is_claude_account_authenticated():
            return self._check_claude_account_auth()

        # No authentication method detected
        return AuthStatus(
            method=AuthMethod.NONE,
            is_authenticated=False,
            details={"message": "No authentication method configured"},
            error="No authentication method detected. Please configure one of: Anthropic API key, Amazon Bedrock, or Claude account login",
        )

    def _is_bedrock_configured(self) -> bool:
        """Check if Amazon Bedrock is configured."""
        return os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"

    def _is_anthropic_api_configured(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY"))

    def _is_claude_account_authenticated(self) -> bool:
        """Check if authenticated with Claude account."""
        try:
            # Check if claude CLI is available
            result = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return False

            # Test authentication by running a simple query in headless mode
            # Slash commands like /status don't work in headless mode, so we test with actual operation
            result = subprocess.run(
                ["claude", "-p", "Hi", "--output-format", "text"], 
                capture_output=True, text=True, timeout=10,
                input=""
            )
            
            # If the command succeeded, we have authentication
            if result.returncode == 0:
                return True
                
            # Check for authentication-related errors
            if result.stderr:
                stderr_lower = result.stderr.lower()
                # These indicate authentication issues
                if any(phrase in stderr_lower for phrase in [
                    "please run /login",
                    "invalid api key", 
                    "authentication",
                    "not logged in"
                ]):
                    return False
                    
            return False

        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _check_bedrock_auth(self) -> AuthStatus:
        """Check Amazon Bedrock authentication status."""
        details = {
            "method": "Amazon Bedrock",
            "aws_region": os.environ.get("AWS_REGION", "Not set"),
            "aws_profile": os.environ.get("AWS_PROFILE", "default"),
        }

        # Check for AWS credentials
        has_credentials = False
        error = None

        # Check environment variables
        if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            has_credentials = True
            details["credential_source"] = "Environment variables"
        # Check AWS credentials file
        elif (Path.home() / ".aws" / "credentials").exists():
            has_credentials = True
            details["credential_source"] = "AWS credentials file"
        # Check for IAM role (EC2/Lambda)
        elif os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"):
            has_credentials = True
            details["credential_source"] = "IAM role"
        else:
            error = (
                "AWS credentials not found. Please configure AWS CLI or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
            )

        # Add model information if available
        details["primary_model"] = os.environ.get(
            "CLAUDE_CODE_PRIMARY_MODEL", "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        )
        details["small_model"] = os.environ.get(
            "CLAUDE_CODE_SMALL_MODEL", "us.anthropic.claude-3-5-haiku-20241022-v1:0"
        )

        return AuthStatus(
            method=AuthMethod.AMAZON_BEDROCK, is_authenticated=has_credentials, details=details, error=error
        )

    def _check_anthropic_api_auth(self) -> AuthStatus:
        """Check Anthropic API authentication status."""
        api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
        api_key_masked = f"...{api_key[-4:]}" if api_key and len(api_key) > 4 else "Not set"

        details = {
            "method": "Anthropic API",
            "api_key": api_key_masked,
            "api_base": os.environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com"),
        }

        is_authenticated = bool(api_key)
        error = None if is_authenticated else "ANTHROPIC_API_KEY environment variable not set"

        return AuthStatus(
            method=AuthMethod.ANTHROPIC_API, is_authenticated=is_authenticated, details=details, error=error
        )

    def _check_claude_account_auth(self) -> AuthStatus:
        """Check Claude account authentication status."""
        details = {"method": "Claude Account (Pro/Max)"}

        try:
            # Test authentication by running a simple query
            # Note: Slash commands like /status and /doctor don't work in headless mode
            result = subprocess.run(
                ["claude", "-p", "Hi", "--output-format", "text"], 
                capture_output=True, text=True, timeout=10,
                input=""
            )
            
            if result.returncode == 0:
                # Authentication successful - we can't get detailed subscription info in headless mode
                # but we know the user is authenticated with a Pro/Max account
                details["subscription"] = "Pro or Max (authenticated)"
                details["authentication_method"] = "Headless test successful"
                details["note"] = "Detailed subscription info not available in headless mode"
                return AuthStatus(method=AuthMethod.CLAUDE_ACCOUNT, is_authenticated=True, details=details)
            
            # Check for specific authentication errors
            if result.stderr:
                stderr_text = result.stderr.strip()
                details["error_output"] = stderr_text[:200] + "..." if len(stderr_text) > 200 else stderr_text
                
                stderr_lower = stderr_text.lower()
                if any(phrase in stderr_lower for phrase in [
                    "please run /login",
                    "invalid api key", 
                    "authentication",
                    "not logged in"
                ]):
                    error = "Claude CLI authentication failed. Please run 'claude login' or check your subscription."
                    return AuthStatus(method=AuthMethod.CLAUDE_ACCOUNT, is_authenticated=False, details=details, error=error)
            
            # Generic failure
            error = "Unable to verify Claude account authentication."
            return AuthStatus(method=AuthMethod.CLAUDE_ACCOUNT, is_authenticated=False, details=details, error=error)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            error = f"Claude CLI not available or error: {str(e)}"
            return AuthStatus(method=AuthMethod.CLAUDE_ACCOUNT, is_authenticated=False, details=details, error=error)

    def get_configuration_instructions(self, method: AuthMethod) -> str:
        """
        Get configuration instructions for a specific auth method.

        Args:
            method: The authentication method to get instructions for

        Returns:
            Configuration instructions as a string
        """
        instructions = {
            AuthMethod.ANTHROPIC_API: """
## Anthropic API Configuration

1. Get your API key from https://console.anthropic.com/
2. Set the environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```
3. Optionally set custom API base:
   ```bash
   export ANTHROPIC_API_BASE="https://api.anthropic.com"
   ```
""",
            AuthMethod.AMAZON_BEDROCK: """
## Amazon Bedrock Configuration

1. Configure AWS credentials using one of these methods:
   - AWS CLI: `aws configure`
   - Environment variables:
     ```bash
     export AWS_ACCESS_KEY_ID="your-access-key"
     export AWS_SECRET_ACCESS_KEY="your-secret-key"
     export AWS_REGION="us-east-1"
     ```
   - IAM role (for EC2/Lambda)

2. Enable Bedrock mode:
   ```bash
   export CLAUDE_CODE_USE_BEDROCK=1
   ```

3. Optionally configure models:
   ```bash
   export CLAUDE_CODE_PRIMARY_MODEL="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
   export CLAUDE_CODE_SMALL_MODEL="us.anthropic.claude-3-5-haiku-20241022-v1:0"
   ```

4. Ensure Claude model access is enabled in AWS Bedrock console
""",
            AuthMethod.CLAUDE_ACCOUNT: """
## Claude Account Configuration (Pro/Max)

1. Install Claude Code CLI:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. Login to your account:
   ```bash
   claude login
   ```

3. Check your subscription status:
   ```bash
   claude status
   ```

4. Select model (Max plan only):
   ```bash
   claude model
   ```

Note: Requires active Pro ($20/month) or Max ($100-200/month) subscription
""",
            AuthMethod.NONE: """
## No Authentication Configured

Please configure one of the following authentication methods:

1. **Anthropic API**: Set ANTHROPIC_API_KEY environment variable
2. **Amazon Bedrock**: Configure AWS credentials and set CLAUDE_CODE_USE_BEDROCK=1
3. **Claude Account**: Run 'claude login' with Pro/Max subscription

See documentation for detailed setup instructions.
""",
        }

        return instructions.get(method, "Unknown authentication method")

    def refresh_status(self) -> AuthStatus:
        """
        Refresh the current authentication status.

        Returns:
            Updated AuthStatus
        """
        self.current_status = self.detect_auth_method()
        return self.current_status

    def is_authenticated(self) -> bool:
        """
        Check if any authentication method is active and authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        if not self.current_status:
            self.refresh_status()

        return self.current_status.is_authenticated if self.current_status else False

    def get_auth_config(self) -> dict[str, Any]:
        """
        Get configuration for the current authentication method.

        Returns:
            Configuration dictionary for use with ClaudeAgent
        """
        if not self.current_status:
            self.refresh_status()

        if not self.current_status or not self.current_status.is_authenticated:
            return {}

        config = {}

        if self.current_status.method == AuthMethod.AMAZON_BEDROCK:
            config["use_bedrock"] = True
            config["aws_region"] = os.environ.get("AWS_REGION")
            config["environment"] = {
                "CLAUDE_CODE_USE_BEDROCK": "1",
                "AWS_REGION": os.environ.get("AWS_REGION", "us-east-1"),
            }

        elif self.current_status.method == AuthMethod.ANTHROPIC_API:
            config["environment"] = {
                "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY", "")
            }

        # Claude account auth doesn't need special config, uses CLI directly

        return config
