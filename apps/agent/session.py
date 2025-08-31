"""
Session Manager for Claude Code Agent

Manages conversation sessions and persistence for Streamlit apps.
"""

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ConversationTurn:
    """Represents a single turn in a conversation."""

    timestamp: str
    role: str  # "user" or "assistant"
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    """Represents a conversation session."""

    id: str
    created_at: str
    updated_at: str
    title: str | None = None
    turns: list[ConversationTurn] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    conversation_id: str | None = None  # Claude's conversation ID


class SessionManager:
    """Manages conversation sessions for Claude Code interactions."""

    def __init__(self, storage_dir: Path | None = None):
        """
        Initialize session manager.

        Args:
            storage_dir: Directory to store session data. Defaults to .claude_sessions
        """
        self.storage_dir = storage_dir or Path.home() / ".claude_sessions"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Session | None = None

    def create_session(self, title: str | None = None) -> Session:
        """Create a new conversation session."""
        session = Session(
            id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            title=title or f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        )
        self.current_session = session
        self.save_session(session)
        return session

    def load_session(self, session_id: str) -> Session:
        """Load an existing session from storage."""
        session_file = self.storage_dir / f"{session_id}.json"

        if not session_file.exists():
            raise FileNotFoundError(f"Session {session_id} not found")

        with open(session_file) as f:
            data = json.load(f)

        # Reconstruct session from JSON
        session = Session(
            id=data["id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            title=data.get("title"),
            turns=[ConversationTurn(**turn) for turn in data.get("turns", [])],
            metadata=data.get("metadata", {}),
            conversation_id=data.get("conversation_id"),
        )

        self.current_session = session
        return session

    def save_session(self, session: Session | None = None):
        """Save session to storage."""
        session = session or self.current_session
        if not session:
            raise ValueError("No session to save")

        session.updated_at = datetime.now().isoformat()

        session_file = self.storage_dir / f"{session.id}.json"

        # Convert to dict for JSON serialization
        session_data = asdict(session)

        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

    def add_turn(self, role: str, content: str, metadata: dict[str, Any] | None = None):
        """Add a conversation turn to the current session."""
        if not self.current_session:
            raise ValueError("No active session. Create or load a session first.")

        turn = ConversationTurn(
            timestamp=datetime.now().isoformat(), role=role, content=content, metadata=metadata or {}
        )

        self.current_session.turns.append(turn)
        self.save_session()

    def list_sessions(self) -> list[dict[str, Any]]:
        """List all available sessions."""
        sessions = []

        for session_file in self.storage_dir.glob("*.json"):
            try:
                with open(session_file) as f:
                    data = json.load(f)
                    sessions.append(
                        {
                            "id": data["id"],
                            "title": data.get("title", "Untitled"),
                            "created_at": data["created_at"],
                            "updated_at": data["updated_at"],
                            "turns_count": len(data.get("turns", [])),
                        }
                    )
            except (json.JSONDecodeError, KeyError):
                # Skip corrupted session files
                continue

        # Sort by updated_at descending
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions

    def delete_session(self, session_id: str):
        """Delete a session from storage."""
        session_file = self.storage_dir / f"{session_id}.json"

        if session_file.exists():
            session_file.unlink()

        if self.current_session and self.current_session.id == session_id:
            self.current_session = None

    def get_conversation_history(self, session: Session | None = None) -> list[dict[str, str]]:
        """
        Get conversation history in format suitable for Claude SDK.

        Returns:
            List of message dicts with 'role' and 'content' keys
        """
        session = session or self.current_session
        if not session:
            return []

        return [{"role": turn.role, "content": turn.content} for turn in session.turns]

    def update_conversation_id(self, conversation_id: str):
        """Update the Claude conversation ID for the current session."""
        if not self.current_session:
            raise ValueError("No active session")

        self.current_session.conversation_id = conversation_id
        self.save_session()

    def clear_current_session(self):
        """Clear the current session without deleting it."""
        if self.current_session:
            self.current_session.turns.clear()
            self.current_session.conversation_id = None
            self.save_session()
