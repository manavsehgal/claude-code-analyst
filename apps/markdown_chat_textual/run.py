#!/usr/bin/env python3
"""
Markdown Chat Textual - A modern terminal UI chatbot powered by Claude Code SDK
Built with Textual for superior markdown rendering and streaming capabilities.
"""

import os
import sys
import glob
import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Input, DataTable, Markdown, 
    Static, Label, LoadingIndicator, TabbedContent, TabPane
)
from textual.reactive import reactive
from textual.worker import Worker, WorkerState
from textual.message import Message

# Add graceful fallback for Claude SDK
try:
    from claude_code_sdk import query
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False


class MarkdownChatTextual(App):
    """A modern terminal chatbot with perfect markdown rendering."""
    
    CSS = """
    #sidebar {
        width: 40;
        background: $surface;
        border-right: solid $primary;
    }
    
    #main-content {
        background: $background;
    }
    
    #chat-display {
        height: 100%;
        padding: 1;
    }
    
    #input-area {
        height: 3;
        dock: bottom;
        background: $surface;
        padding: 0 1;
    }
    
    #file-table {
        height: 100%;
    }
    
    .status-label {
        color: $text-muted;
        text-style: italic;
    }
    
    .error-message {
        color: $error;
        text-style: bold;
    }
    
    .success-message {
        color: $success;
        text-style: bold;
    }
    
    .chat-message {
        margin: 1 0;
    }
    
    .user-message {
        background: $primary-lighten-2;
        padding: 1;
        border-left: solid $primary;
    }
    
    .claude-message {
        background: $secondary-lighten-2;
        padding: 1;
        border-left: solid $secondary;
    }
    
    Markdown {
        margin: 1;
    }
    
    LoadingIndicator {
        height: 3;
        content-align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", priority=True),
        Binding("ctrl+l", "load_file", "Load File"),
        Binding("ctrl+r", "refresh", "Refresh Files"),
        Binding("ctrl+n", "navigate", "Navigate"),
        Binding("ctrl+h", "toggle_help", "Help"),
        Binding("escape", "clear_input", "Clear"),
    ]
    
    # Reactive properties
    current_directory = reactive(Path("."))
    current_file = reactive(None)
    is_processing = reactive(False)
    
    def __init__(self, working_directory: str = "."):
        super().__init__()
        self.working_directory = Path(working_directory).resolve()
        self.current_directory = self.working_directory
        self.markdown_files: List[Path] = []
        self.folders_with_markdown: List[Path] = []
        self.current_context: Optional[Dict[str, Any]] = None
        self.chat_history: List[Dict[str, str]] = []
        self.config_status = self._detect_claude_config()
        
    def compose(self) -> ComposeResult:
        """Create the app layout."""
        yield Header(show_clock=True)
        
        with Horizontal():
            # Sidebar with file navigation
            with Vertical(id="sidebar"):
                yield Label("📁 Files & Folders", classes="success-message")
                yield DataTable(id="file-table", cursor_type="row")
                yield Label("", id="file-status", classes="status-label")
            
            # Main content area
            with Vertical(id="main-content"):
                # Chat display area with tabs
                with TabbedContent(initial="chat"):
                    with TabPane("💬 Chat", id="chat"):
                        yield ScrollableContainer(
                            Markdown("# Welcome to Markdown Chat\n\nLoad a file to start chatting!"),
                            id="chat-display"
                        )
                    
                    with TabPane("📄 Current File", id="file-view"):
                        yield ScrollableContainer(
                            Markdown("*No file loaded*"),
                            id="file-content"
                        )
                    
                    with TabPane("ℹ️ Help", id="help"):
                        yield ScrollableContainer(
                            Markdown(self._get_help_content()),
                            id="help-content"
                        )
                
                # Status and loading indicator
                yield Container(
                    LoadingIndicator(id="loading"),
                    id="status-container"
                )
                
                # Input area
                yield Input(
                    placeholder="Type your message or command (Enter to send)...",
                    id="chat-input"
                )
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the app when mounted."""
        self.title = "Markdown Chat Textual"
        self.sub_title = f"📂 {self.current_directory.name}"
        
        # Hide loading indicator initially
        self.query_one("#loading").display = False
        
        # Populate file table
        self.refresh_files()
        
        # Show configuration status
        self._show_config_status()
        
        # Focus on input
        self.query_one("#chat-input").focus()
    
    def refresh_files(self) -> None:
        """Discover and display markdown files and folders."""
        self._discover_content()
        self._update_file_table()
    
    def _discover_content(self) -> None:
        """Discover markdown files and folders in current directory."""
        self.markdown_files = []
        self.folders_with_markdown = []
        
        # Find markdown files in current directory
        patterns = ["*.md", "*.markdown"]
        for pattern in patterns:
            files = glob.glob(str(self.current_directory / pattern))
            self.markdown_files.extend([Path(f) for f in files])
        
        # Find subdirectories with markdown files
        if self.current_directory.is_dir():
            for item in self.current_directory.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    if self._directory_has_markdown(item):
                        self.folders_with_markdown.append(item)
        
        # Sort lists
        self.markdown_files.sort(key=lambda x: x.name.lower())
        self.folders_with_markdown.sort(key=lambda x: x.name.lower())
    
    def _directory_has_markdown(self, directory: Path) -> bool:
        """Check if directory contains markdown files."""
        patterns = ["**/*.md", "**/*.markdown"]
        for pattern in patterns:
            files = glob.glob(str(directory / pattern), recursive=True)
            if files:
                return True
        return False
    
    def _update_file_table(self) -> None:
        """Update the file table with current directory contents."""
        table = self.query_one("#file-table", DataTable)
        table.clear(columns=True)
        
        # Add columns
        table.add_column("Type", width=4)
        table.add_column("Name", width=25)
        table.add_column("Info", width=10)
        
        # Add folders
        for folder in self.folders_with_markdown:
            file_count = len(glob.glob(str(folder / "**/*.md"), recursive=True))
            table.add_row("📁", folder.name, f"{file_count} files")
        
        # Add files
        for file_path in self.markdown_files:
            try:
                size = file_path.stat().st_size
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
            except OSError:
                size_str = "--"
            
            # Highlight current file
            if self.current_context and self.current_context['file_path'] == file_path:
                table.add_row("📄", f"[bold cyan]{file_path.name}[/]", size_str)
            else:
                table.add_row("📄", file_path.name, size_str)
        
        # Update status
        status = self.query_one("#file-status", Label)
        total_folders = len(self.folders_with_markdown)
        total_files = len(self.markdown_files)
        status.update(f"📊 {total_folders} folders, {total_files} files")
    
    @on(DataTable.RowSelected)
    def on_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle file/folder selection from table."""
        if event.data_table.row_count == 0:
            return
        
        row_index = event.cursor_row
        folder_count = len(self.folders_with_markdown)
        
        if row_index < folder_count:
            # Navigate to folder
            folder = self.folders_with_markdown[row_index]
            self.change_directory(folder)
        else:
            # Load file
            file_index = row_index - folder_count
            if 0 <= file_index < len(self.markdown_files):
                self.load_file(self.markdown_files[file_index])
    
    def change_directory(self, new_dir: Path) -> None:
        """Change to a new directory."""
        self.current_directory = new_dir
        self.sub_title = f"📂 {self.current_directory.name}"
        self.refresh_files()
        self.notify(f"📁 Entered: {new_dir.name}", severity="information")
    
    def load_file(self, file_path: Path) -> None:
        """Load a markdown file into context."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_context = {
                'file_path': file_path,
                'content': content
            }
            
            # Update file view tab
            file_display = self.query_one("#file-content", ScrollableContainer)
            file_display.remove_children()
            file_display.mount(Markdown(content))
            
            # Update file table to show loaded file
            self._update_file_table()
            
            # Add to chat
            rel_path = file_path.relative_to(self.working_directory)
            self.add_to_chat(
                f"📄 **Loaded:** {rel_path}\n"
                f"📊 {len(content):,} characters, {content.count(chr(10)) + 1:,} lines",
                role="system"
            )
            
            self.notify(f"✅ Loaded: {file_path.name}", severity="information")
            
        except Exception as e:
            self.notify(f"❌ Error loading file: {e}", severity="error")
    
    def add_to_chat(self, message: str, role: str = "user") -> None:
        """Add a message to the chat display."""
        chat_display = self.query_one("#chat-display", ScrollableContainer)
        
        # Create styled message based on role
        if role == "user":
            prefix = "👤 **You:**\n"
            class_list = ["user-message", "chat-message"]
        elif role == "assistant":
            prefix = "🤖 **Claude:**\n"
            class_list = ["claude-message", "chat-message"]
        else:
            prefix = ""
            class_list = ["chat-message"]
        
        # Add to history
        self.chat_history.append({"role": role, "content": message})
        
        # Create markdown widget for the message
        markdown_widget = Markdown(prefix + message)
        for class_name in class_list:
            markdown_widget.add_class(class_name)
        
        # Add to display
        chat_display.mount(markdown_widget)
        
        # Auto-scroll to bottom
        chat_display.scroll_end(animate=True)
    
    @on(Input.Submitted)
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        message = event.value.strip()
        if not message:
            return
        
        # Clear input
        event.input.value = ""
        
        # Check for commands
        if message.lower() == "quit" or message.lower() == "exit":
            self.exit()
        elif message.lower() == "help":
            self.query_one(TabbedContent).active = "help"
        elif message.lower() == "clear":
            self.clear_chat()
        elif message.lower() == "refresh":
            self.refresh_files()
        elif message.lower() == "up":
            self.go_up_directory()
        elif message.lower().startswith("cd "):
            self.handle_cd_command(message)
        elif message.lower().startswith("load "):
            self.handle_load_command(message)
        else:
            # Send to Claude
            self.add_to_chat(message, role="user")
            await self.chat_with_claude(message)
    
    def clear_chat(self) -> None:
        """Clear the chat display."""
        chat_display = self.query_one("#chat-display", ScrollableContainer)
        chat_display.remove_children()
        chat_display.mount(Markdown("# Chat Cleared\n\nReady for new conversation!"))
        self.chat_history.clear()
        self.notify("Chat cleared", severity="information")
    
    def go_up_directory(self) -> None:
        """Navigate to parent directory."""
        if self.current_directory == self.working_directory:
            self.notify("Already at root directory", severity="warning")
            return
        
        parent = self.current_directory.parent
        if not str(parent).startswith(str(self.working_directory)):
            self.notify("Cannot navigate above root", severity="warning")
            return
        
        self.change_directory(parent)
    
    def handle_cd_command(self, command: str) -> None:
        """Handle cd command."""
        try:
            index = int(command.split()[1]) - 1
            if 0 <= index < len(self.folders_with_markdown):
                self.change_directory(self.folders_with_markdown[index])
            else:
                self.notify("Invalid folder number", severity="error")
        except (IndexError, ValueError):
            self.notify("Usage: cd <folder_number>", severity="error")
    
    def handle_load_command(self, command: str) -> None:
        """Handle load command."""
        try:
            index = int(command.split()[1]) - 1
            folder_count = len(self.folders_with_markdown)
            file_index = index - folder_count
            
            if index < folder_count:
                self.notify("That's a folder, use 'cd' instead", severity="warning")
            elif 0 <= file_index < len(self.markdown_files):
                self.load_file(self.markdown_files[file_index])
            else:
                self.notify("Invalid file number", severity="error")
        except (IndexError, ValueError):
            self.notify("Usage: load <file_number>", severity="error")
    
    @work(exclusive=True)
    async def chat_with_claude(self, user_message: str) -> None:
        """Send message to Claude with streaming support."""
        if not CLAUDE_SDK_AVAILABLE:
            self.add_to_chat(
                "❌ Claude Code SDK not available. Please install it first:\n"
                "`uv add claude-code-sdk`",
                role="system"
            )
            return
        
        # Show loading indicator
        loading = self.query_one("#loading")
        loading.display = True
        
        # Build prompt
        if self.current_context:
            rel_path = self.current_context['file_path'].relative_to(self.working_directory)
            prompt = f"""I have loaded a markdown file called '{rel_path}' with the following content:

---
{self.current_context['content']}
---

User question: {user_message}"""
        else:
            prompt = f"""I'm using a markdown chatbot, but no specific file is currently loaded. 
Here's my question: {user_message}"""
        
        try:
            # Collect response with streaming
            response_content = ""
            response_started = False
            
            # Create a placeholder for streaming response
            chat_display = self.query_one("#chat-display", ScrollableContainer)
            response_widget = Markdown("🤖 **Claude:** *Thinking...*")
            response_widget.add_class("claude-message")
            response_widget.add_class("chat-message")
            chat_display.mount(response_widget)
            chat_display.scroll_end(animate=True)
            
            async for message in query(prompt=prompt):
                if hasattr(message, 'content'):
                    chunk = ""
                    
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                chunk = str(block.text)
                    elif hasattr(message.content, 'text'):
                        chunk = str(message.content.text)
                    elif message.content:
                        chunk = str(message.content)
                    
                    if chunk and not self._is_system_message(chunk):
                        if not response_started:
                            response_content = chunk
                            response_started = True
                        else:
                            response_content = chunk  # Use latest complete response
                        
                        # Update the response widget with streaming content
                        response_widget.update(f"🤖 **Claude:**\n\n{response_content}")
                        chat_display.scroll_end(animate=False)
            
            # Final update with complete response
            if response_content:
                response_widget.update(f"🤖 **Claude:**\n\n{response_content}")
                self.chat_history.append({"role": "assistant", "content": response_content})
            else:
                response_widget.update("🤖 **Claude:** *No response received*")
            
        except Exception as e:
            self.add_to_chat(f"❌ Error: {str(e)}", role="system")
        finally:
            loading.display = False
    
    def _is_system_message(self, text: str) -> bool:
        """Check if text is a system message to filter out."""
        if not text or not isinstance(text, str):
            return True
        
        text = text.strip()
        if not text or len(text) < 3:
            return True
        
        # Check for SDK-specific patterns
        system_patterns = [
            'system:', 'responsemessage:', 'systemmessage:', 
            '(subtype=', 'duration_ms=', 'session_id=', 'usage={',
            'total_cost_usd=', 'output_tokens=', 'input_tokens='
        ]
        
        text_lower = text.lower()
        for pattern in system_patterns:
            if pattern in text_lower:
                return True
        
        return False
    
    def _detect_claude_config(self) -> Dict[str, Any]:
        """Detect Claude SDK configuration."""
        config = {
            'has_valid_config': False,
            'status_message': 'No configuration detected',
            'method': None
        }
        
        if os.getenv('ANTHROPIC_API_KEY'):
            config['has_valid_config'] = True
            config['status_message'] = 'API Key configured'
            config['method'] = 'api_key'
        elif os.getenv('CLAUDE_CODE_USE_BEDROCK'):
            if (os.getenv('AWS_ACCESS_KEY_ID') or 
                os.path.isfile(os.path.expanduser('~/.aws/credentials'))):
                config['has_valid_config'] = True
                config['status_message'] = 'Bedrock configured'
                config['method'] = 'bedrock'
        else:
            # Check for Claude CLI
            import subprocess
            try:
                result = subprocess.run(['which', 'claude'], 
                                      capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    config['has_valid_config'] = True
                    config['status_message'] = 'Claude CLI detected'
                    config['method'] = 'pro_max'
            except:
                pass
        
        return config
    
    def _show_config_status(self) -> None:
        """Show configuration status in chat."""
        if CLAUDE_SDK_AVAILABLE:
            if self.config_status['has_valid_config']:
                status = f"✅ Ready ({self.config_status['method']})"
            else:
                status = "⚠️ Configuration needed"
        else:
            status = "❌ SDK not available"
        
        self.add_to_chat(
            f"**System Status:** {status}\n"
            f"**Working Directory:** {self.working_directory}\n"
            f"**Files Found:** {len(self.markdown_files)} markdown files",
            role="system"
        )
    
    def _get_help_content(self) -> str:
        """Get help content as markdown."""
        return """
# Markdown Chat Textual - Help

## 🎯 Quick Start
1. Select a file from the sidebar or use `load <number>`
2. Type your question and press Enter
3. Claude will respond with context from the loaded file

## ⌨️ Keyboard Shortcuts
- **Ctrl+L** - Load selected file
- **Ctrl+R** - Refresh file list
- **Ctrl+N** - Navigate folders
- **Ctrl+H** - Toggle this help
- **Ctrl+C** - Quit application
- **Escape** - Clear input field

## 💬 Chat Commands
- **help** - Show this help
- **clear** - Clear chat history
- **refresh** - Refresh file list
- **up** - Go to parent directory
- **cd <number>** - Enter folder by number
- **load <number>** - Load file by number
- **quit/exit** - Exit application

## 🚀 Features
- **Perfect Table Rendering** - Tables display correctly without spacing issues
- **Real-time Streaming** - See Claude's response as it's generated
- **Folder Navigation** - Browse through your markdown files easily
- **Syntax Highlighting** - Code blocks are properly highlighted
- **Responsive UI** - Smooth scrolling and animations

## 📝 Tips
- Click on files/folders in the sidebar to navigate
- The current file is highlighted in cyan
- Chat history is preserved during the session
- Use the tabs to switch between chat, file view, and help

## 🔧 Configuration
The app supports three authentication methods:
1. **API Key**: `export ANTHROPIC_API_KEY=your_key`
2. **Pro/Max Plan**: Authenticate with `claude` CLI
3. **Bedrock**: Set up AWS credentials

## 📄 About
Built with Textual for superior terminal UI experience.
Fixes all table rendering and streaming issues from the Rich-based version.
"""
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
    
    def action_load_file(self) -> None:
        """Load the selected file."""
        table = self.query_one("#file-table", DataTable)
        if table.cursor_row is not None:
            self.on_row_selected(DataTable.RowSelected(table, table.cursor_row))
    
    def action_refresh(self) -> None:
        """Refresh file list."""
        self.refresh_files()
        self.notify("Files refreshed", severity="information")
    
    def action_navigate(self) -> None:
        """Focus on file navigation."""
        self.query_one("#file-table").focus()
    
    def action_toggle_help(self) -> None:
        """Toggle help tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "help" if tabs.active != "help" else "chat"
    
    def action_clear_input(self) -> None:
        """Clear the input field."""
        self.query_one("#chat-input", Input).value = ""


def main():
    """Entry point for the Textual markdown chat app."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Markdown Chat Textual - Modern terminal chatbot with perfect rendering"
    )
    parser.add_argument(
        "--directory", "-d", 
        default=".", 
        help="Directory to search for markdown files (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Verify directory exists
    if not os.path.isdir(args.directory):
        print(f"❌ Directory not found: {args.directory}")
        sys.exit(1)
    
    # Check SDK availability
    if not CLAUDE_SDK_AVAILABLE:
        print("⚠️  Claude Code SDK not available. Install with: uv add claude-code-sdk")
        print("You can still browse files, but chat features will be limited.")
    
    # Run the app
    app = MarkdownChatTextual(working_directory=args.directory)
    app.run()


if __name__ == "__main__":
    main()