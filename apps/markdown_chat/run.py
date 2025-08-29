#!/usr/bin/env python3
"""
Markdown Chat - A terminal UI chatbot powered by Claude Code SDK
that can navigate and discuss markdown files in the current directory.
"""

import os
import sys
import glob
import asyncio
import time
import re
from pathlib import Path
from typing import List, Optional, AsyncGenerator

# Rich library for enhanced terminal UI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.layout import Layout
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.status import Status
from rich import box

# Add a graceful fallback for the claude-code-sdk import
try:
    from claude_code_sdk import query
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False

# Initialize Rich console
console = Console()


class MarkdownChatbot:
    """A terminal-based chatbot that can navigate and discuss markdown files."""
    
    def __init__(self, working_directory: str = "."):
        self.working_directory = Path(working_directory).resolve()
        self.current_directory = self.working_directory  # Current navigation directory
        self.markdown_files = []
        self.folders_with_markdown = []
        self.current_context = None
        self.console = Console()
        self.discover_content()
    
    def discover_content(self) -> None:
        """Discover markdown files and folders in the current directory."""
        with self.console.status("[bold blue]Discovering content...", spinner="dots"):
            self._discover_in_current_directory()
            
        # Enhanced discovery feedback
        total_files = len(self.markdown_files)
        total_folders = len(self.folders_with_markdown)
        
        if total_files > 0 or total_folders > 0:
            rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
            self.console.print(
                f"[bold green]✓ Discovered {total_files} markdown files and {total_folders} folders[/bold green] "
                f"in [dim]{rel_path}[/dim]"
            )
        else:
            rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
            self.console.print(f"[bold yellow]⚠️  No markdown content found[/bold yellow] in [dim]{rel_path}[/dim]")
            self.console.print("[dim]💡 Try navigating to a different directory or create markdown files[/dim]")
    
    def _discover_in_current_directory(self) -> None:
        """Discover markdown files and folders with markdown in current directory only."""
        self.markdown_files = []
        self.folders_with_markdown = []
        
        # Find markdown files in current directory
        patterns = ["*.md", "*.markdown"]
        for pattern in patterns:
            files = glob.glob(str(self.current_directory / pattern))
            self.markdown_files.extend([Path(f) for f in files])
        
        # Find subdirectories that contain markdown files
        if self.current_directory.is_dir():
            for item in self.current_directory.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if this directory contains markdown files (recursive)
                    has_markdown = self._directory_has_markdown(item)
                    if has_markdown:
                        self.folders_with_markdown.append(item)
        
        # Sort both lists
        self.markdown_files.sort(key=lambda x: x.name.lower())
        self.folders_with_markdown.sort(key=lambda x: x.name.lower())
    
    def _directory_has_markdown(self, directory: Path) -> bool:
        """Check if a directory contains any markdown files (recursive)."""
        patterns = ["**/*.md", "**/*.markdown"]
        for pattern in patterns:
            files = glob.glob(str(directory / pattern), recursive=True)
            if files:
                return True
        return False
    
    def list_content(self) -> None:
        """Display folders and markdown files in current directory with enhanced formatting."""
        total_items = len(self.folders_with_markdown) + len(self.markdown_files)
        
        if total_items == 0:
            rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
            no_content_panel = Panel(
                f"[bold yellow]No markdown content found in {rel_path}[/bold yellow]\n\n" +
                "[dim]💡 Tips:[/dim]\n" +
                "[dim]• Use 'up' to go to parent directory[/dim]\n" +
                "[dim]• Create some markdown files to get started[/dim]\n" +
                "[dim]• Use 'cd <folder>' to navigate to subfolders[/dim]",
                title="📁 Content Discovery",
                border_style="yellow",
                padding=(1, 2)
            )
            self.console.print(no_content_panel)
            return
        
        # Show current directory path
        rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
        current_dir_text = f"📂 Current Directory: [bold cyan]{rel_path}[/bold cyan]"
        self.console.print(current_dir_text)
        
        # Create table for folders and files
        table = Table(title=f"📋 Available Content ({total_items} items)", 
                     box=box.ROUNDED, title_style="bold cyan")
        table.add_column("#", style="bold blue", width=3, justify="right")
        table.add_column("Type", style="white", width=6, justify="center")
        table.add_column("Name", style="green", min_width=30)
        table.add_column("Info", style="dim", justify="right", width=20)
        
        item_index = 1
        
        # Add folders first
        for folder in self.folders_with_markdown:
            folder_name = folder.name
            # Count markdown files in this folder (recursive)
            file_count = len(glob.glob(str(folder / "**/*.md"), recursive=True)) + \
                        len(glob.glob(str(folder / "**/*.markdown"), recursive=True))
            info_str = f"{file_count} markdown files"
            
            table.add_row(str(item_index), "📁", f"[bold yellow]{folder_name}/[/bold yellow]", info_str)
            item_index += 1
        
        # Add markdown files
        for file_path in self.markdown_files:
            try:
                stat = file_path.stat()
                size = stat.st_size
                
                # Format size nicely
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                    
            except OSError:
                size_str = "--"
            
            # Highlight currently loaded file
            if (self.current_context and 
                self.current_context['file_path'] == file_path):
                table.add_row(str(item_index), "📄", f"[bold cyan]{file_path.name}[/bold cyan] ✓", size_str)
            else:
                table.add_row(str(item_index), "📄", file_path.name, size_str)
            item_index += 1
        
        self.console.print(table)
        
        # Enhanced navigation tips
        tips = []
        if len(self.folders_with_markdown) > 0:
            tips.append("Use 'cd <number>' to enter folders")
        if len(self.markdown_files) > 0:
            tips.append("Use 'load <number>' to load files")
        if self.current_directory != self.working_directory:
            tips.append("Use 'up' to go to parent directory")
        
        if tips:
            self.console.print(f"[dim]💡 {' • '.join(tips)}[/dim]")
    
    def load_markdown_file(self, item_index: int) -> Optional[str]:
        """Load content from a markdown file by index."""
        # Calculate the actual file index (subtract folder count)
        folder_count = len(self.folders_with_markdown)
        file_index = item_index - folder_count - 1
        
        if item_index <= folder_count:
            self.console.print("[bold red]❌ That's a folder, not a file.[/bold red] Use [bold cyan]'cd <number>'[/bold cyan] to enter folders.")
            return None
        
        if 0 <= file_index < len(self.markdown_files):
            file_path = self.markdown_files[file_index]
            try:
                with self.console.status(f"[bold blue]Loading file {item_index}...", spinner="dots"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                
                self.current_context = {
                    'file_path': file_path,
                    'content': content
                }
                rel_path = file_path.relative_to(self.working_directory)
                
                # Create a nice panel for the loaded file info
                info_text = Text()
                info_text.append("📄 ", style="bold")
                info_text.append(str(rel_path), style="bold green")
                info_text.append(f"\n📊 {len(content):,} characters, {content.count(chr(10)) + 1:,} lines", style="dim")
                
                panel = Panel(info_text, title="[bold green]✅ File Loaded[/bold green]", border_style="green")
                self.console.print(panel)
                
                return content
            except Exception as e:
                self.console.print(f"[bold red]❌ Error loading file:[/bold red] {e}")
                return None
        else:
            self.console.print("[bold red]❌ Invalid item number.[/bold red] Use [bold cyan]'list'[/bold cyan] to see available items.")
            return None
    
    def change_directory(self, item_index: int) -> bool:
        """Change to a folder by index."""
        if 1 <= item_index <= len(self.folders_with_markdown):
            folder_path = self.folders_with_markdown[item_index - 1]
            self.current_directory = folder_path
            
            with self.console.status("[bold blue]Navigating to folder...", spinner="dots"):
                self.discover_content()
            
            rel_path = self.current_directory.relative_to(self.working_directory)
            self.console.print(f"[bold green]✓ Entered folder:[/bold green] [bold cyan]{rel_path}[/bold cyan]")
            self.list_content()
            return True
        elif item_index > len(self.folders_with_markdown):
            self.console.print("[bold red]❌ That's a file, not a folder.[/bold red] Use [bold cyan]'load <number>'[/bold cyan] to load files.")
            return False
        else:
            self.console.print("[bold red]❌ Invalid folder number.[/bold red] Use [bold cyan]'list'[/bold cyan] to see available folders.")
            return False
    
    def go_up_directory(self) -> bool:
        """Go to parent directory."""
        if self.current_directory == self.working_directory:
            self.console.print("[bold yellow]⚠️ Already at the root directory.[/bold yellow]")
            return False
        
        # Check if parent is within working directory
        parent = self.current_directory.parent
        if not str(parent).startswith(str(self.working_directory)):
            self.console.print("[bold yellow]⚠️ Cannot navigate above the root directory.[/bold yellow]")
            return False
        
        self.current_directory = parent
        
        with self.console.status("[bold blue]Going up...", spinner="dots"):
            self.discover_content()
        
        rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
        self.console.print(f"[bold green]✓ Moved to:[/bold green] [bold cyan]{rel_path}[/bold cyan]")
        self.list_content()
        return True
    
    def show_help(self) -> None:
        """Display comprehensive help information with enhanced guidance."""
        # Create a comprehensive help table
        help_table = Table(title="🤖 Markdown Chat Commands", box=box.ROUNDED, title_style="bold cyan")
        help_table.add_column("Command", style="bold yellow", width=22)
        help_table.add_column("Description", style="white")
        help_table.add_column("Example", style="dim", width=15)
        
        # File and folder navigation commands
        help_table.add_row("list", "Show folders and files in current directory", "list")
        help_table.add_row("cd <number>", "Enter a folder by number", "cd 2")
        help_table.add_row("up", "Go to parent directory", "up")
        help_table.add_row("load <number>", "Load a markdown file into context", "load 5")
        
        # Information commands
        help_table.add_row("show", "Display current file information", "show")
        help_table.add_row("pwd", "Show current directory path", "pwd")
        help_table.add_row("refresh", "Refresh folder/file listing", "refresh")
        
        # System commands
        help_table.add_row("help", "Show this help message", "help")
        help_table.add_row("quit/exit/q", "Exit the chatbot gracefully", "quit")
        
        self.console.print(help_table)
        
        # Enhanced examples with categories
        chat_examples = Panel(
            "[bold cyan]📝 Chat Examples:[/bold cyan]\n\n" +
            "[bold green]Getting Started:[/bold green]\n" +
            "• [yellow]what is this document about?[/yellow]\n" +
            "• [yellow]summarize the main points[/yellow]\n" +
            "• [yellow]give me an overview[/yellow]\n\n" +
            "[bold green]Deep Analysis:[/bold green]\n" +
            "• [yellow]explain the technical concepts[/yellow]\n" +
            "• [yellow]what are the key takeaways?[/yellow]\n" +
            "• [yellow]find any issues or problems mentioned[/yellow]\n\n" +
            "[bold green]Specific Questions:[/bold green]\n" +
            "• [yellow]how does X work in this context?[/yellow]\n" +
            "• [yellow]what examples are provided?[/yellow]\n" +
            "• [yellow]create a todo list from this content[/yellow]",
            title="💡 Smart Chat Examples",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(chat_examples)
        
        # Navigation-specific guidance
        nav_guide = Panel(
            "[bold cyan]🗺️ Navigation Guide:[/bold cyan]\n\n" +
            "[bold green]📁 Folders vs 📄 Files:[/bold green]\n" +
            "• [yellow]Folders[/yellow] contain markdown files and show with 📁 icon\n" +
            "• [yellow]Files[/yellow] are markdown documents you can load with 📄 icon\n" +
            "• Numbers in 'list' command work for both folders and files\n\n" +
            "[bold green]Navigation Tips:[/bold green]\n" +
            "• Start with 'list' to see current directory contents\n" +
            "• Use 'cd <number>' to explore folders with markdown files\n" +
            "• Use 'load <number>' to load files for AI conversation\n" +
            "• Use 'up' to go back to parent directories\n" +
            "• Use 'pwd' to see where you are in the directory structure",
            title="🎠 Navigation Help",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(nav_guide)
        
        # Pro tips section
        pro_tips = Panel(
            "[bold magenta]🏆 Pro Tips:[/bold magenta]\n" +
            "• Load a file first with 'load <number>' for better context\n" +
            "• Ask follow-up questions to dive deeper into topics\n" +
            "• Navigate folders to organize your markdown exploration\n" +
            "• The chatbot remembers your loaded file throughout the session",
            title="✨ Advanced Usage",
            border_style="magenta"
        )
        self.console.print(pro_tips)
    
    def show_current_context(self) -> None:
        """Show enhanced information about the currently loaded file and current directory."""
        # Show current directory info
        rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
        dir_info = Panel(
            f"[bold blue]📂 Current Directory:[/bold blue] [bold cyan]{rel_path}[/bold cyan]\n" +
            f"[dim]📁 Folders: {len(self.folders_with_markdown)} • 📄 Files: {len(self.markdown_files)}[/dim]",
            border_style="blue",
            padding=(0, 1)
        )
        self.console.print(dir_info)
        
        # Show loaded file info if any
        if self.current_context:
            file_rel_path = self.current_context['file_path'].relative_to(self.working_directory)
            content_length = len(self.current_context['content'])
            lines = self.current_context['content'].count('\n') + 1
            
            # Calculate additional metadata
            words = len(self.current_context['content'].split())
            
            # Analyze content type
            content = self.current_context['content']
            headers = len([line for line in content.split('\n') if line.strip().startswith('#')])
            code_blocks = content.count('```')
            links = content.count('](') 
            
            # Create a comprehensive info panel
            info_text = Text()
            info_text.append("📄 Loaded File: ", style="bold")
            info_text.append(str(file_rel_path), style="bold green")
            info_text.append(f"\n📊 Content: {content_length:,} chars • {lines:,} lines • {words:,} words", style="dim")
            
            if headers > 0 or code_blocks > 0 or links > 0:
                info_text.append(f"\n📋 Structure: ", style="dim")
                if headers > 0:
                    info_text.append(f"{headers} headers • ", style="dim")
                if code_blocks > 0:
                    info_text.append(f"{code_blocks//2} code blocks • ", style="dim")
                if links > 0:
                    info_text.append(f"{links} links • ", style="dim")
            
            info_text.append(f"\n📂 Full path: {self.current_context['file_path']}", style="dim")
            
            panel = Panel(info_text, title="[bold green]✓ Currently Loaded File[/bold green]", border_style="green")
            self.console.print(panel)
            
            # Show content preview
            preview_lines = self.current_context['content'].split('\n')[:3]
            if preview_lines:
                preview_text = '\n'.join(preview_lines)
                if len(preview_lines) == 3 and len(self.current_context['content'].split('\n')) > 3:
                    preview_text += '\n...'
                
                preview_panel = Panel(
                    preview_text,
                    title="[dim]Content Preview[/dim]",
                    border_style="dim",
                    padding=(0, 1)
                )
                self.console.print(preview_panel)
        else:
            no_context_panel = Panel(
                "[bold yellow]No file currently loaded[/bold yellow]\n\n" +
                "[dim]To get started:[/dim]\n" +
                "[dim]• Type [bold cyan]'list'[/bold cyan] to see available content[/dim]\n" +
                "[dim]• Use [bold cyan]'cd <number>'[/bold cyan] to enter folders[/dim]\n" +
                "[dim]• Use [bold cyan]'load <number>'[/bold cyan] to load files for chat[/dim]",
                title="📁 Context Status",
                border_style="yellow",
                padding=(1, 2)
            )
            self.console.print(no_context_panel)
    
    def show_current_directory(self) -> None:
        """Show current directory path."""
        rel_path = self.current_directory.relative_to(self.working_directory) if self.current_directory != self.working_directory else "."
        pwd_panel = Panel(
            f"[bold blue]📂 Current Directory:[/bold blue] [bold cyan]{rel_path}[/bold cyan]\n" +
            f"[bold blue]🗺️ Full Path:[/bold blue] [dim]{self.current_directory}[/dim]\n" +
            f"[bold blue]📋 Contents:[/bold blue] [dim]{len(self.folders_with_markdown)} folders, {len(self.markdown_files)} files[/dim]",
            title="🗺️ Location Info",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(pwd_panel)
    
    def _is_system_message(self, text: str) -> bool:
        """Improved system message detection that preserves technical content."""
        if not text or not isinstance(text, str):
            return True
        
        text = text.strip()
        if not text:
            return True
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # System message prefixes - be more specific
        system_indicators = [
            # Common system prefixes
            'system:', 'responsemessage:', 'systemmessage:', 'resultmessage:', 'result:',
            'internal:', 'debug:', 'log:', 'error:', 'warning:',
            
            # API/SDK related
            'status:', 'timestamp:', 'id:', 'uuid:', 'token:', 'auth:',
            'request:', 'http:', 'api:', 'endpoint:', 'url:',
        ]
        
        # Check for exact matches at start of text
        for indicator in system_indicators:
            if text_lower.startswith(indicator):
                return True
        
        # Regex patterns for system messages (more conservative)
        system_patterns = [
            r'^<[^>]*>',  # XML-like tags at start
            r'^\[System\]:?',  # Specific [System]: prefix
            r'^\{.*?\}:?\s*$',  # JSON-like objects on single line
            r'^\w+Message\s*:',  # Word ending with 'Message' followed by colon
            r'^\w+Response\s*:',  # Word ending with 'Response' followed by colon
            r'^\w+Result\s*:',  # Word ending with 'Result' followed by colon
            r'^\s*$',  # Empty or whitespace only
            r'<\|.*?\|>',  # Special tokens
            r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}',  # Full timestamp patterns
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}',  # UUID patterns
        ]
        
        for pattern in system_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        
        # Very specific system content indicators (more conservative)
        system_content_indicators = [
            'internal error occurred', 'processing request', 'api response received', 
            'server response', 'authentication failed', 'authorization required',
            'permission denied', 'access granted', 'session expired',
            'json parsing error', 'xml parsing error', 'serialization failed',
        ]
        
        for indicator in system_content_indicators:
            if indicator in text_lower:
                return True
        
        # Filter extremely short responses
        if len(text) < 3:
            return True
        
        # Check for pure structured data (JSON/XML) - but allow markdown tables
        if (text.startswith(('{', '[')) and text.endswith(('}', ']')) and 
            not any(char in text for char in ['|', '#', '*', '-', '_'])):
            return True
            
        return False
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text to prevent JSON encoding errors and filter problematic content."""
        if not isinstance(text, str):
            text = str(text)
        
        # Replace problematic Unicode characters that could cause JSON errors
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        
        # Remove or replace control characters except common ones
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Remove any remaining problematic patterns that could indicate system messages
        text = re.sub(r'^[A-Za-z]*Message\s*[:\-]?\s*', '', text)  # Remove MessageType prefixes
        text = re.sub(r'^[A-Za-z]*Response\s*[:\-]?\s*', '', text)  # Remove ResponseType prefixes
        text = re.sub(r'^[A-Za-z]*Result\s*[:\-]?\s*', '', text)    # Remove ResultType prefixes
        
        return text.strip()
    
    async def _stream_text_output(self, text: str, title: str = "🤖 Claude") -> None:
        """Stream text output with smooth character-by-character display."""
        if not text or self._is_system_message(text):
            return
            
        # Sanitize the text to prevent encoding issues
        text = self._sanitize_text(text)
        if not text or self._is_system_message(text):  # Double-check after sanitization
            return
        
        # Final content quality check - ensure it's substantial user-facing content
        if len(text) < 5:  # Too short to be meaningful
            return
        
        # Check if it's markdown content
        is_markdown = self._looks_like_markdown(text)
        
        if is_markdown:
            # For markdown, render it directly without streaming to preserve formatting
            try:
                markdown = Markdown(text)
                panel = Panel(markdown, title=f"[bold green]{title}[/bold green]", 
                            border_style="green", padding=(1, 2))
                self.console.print(panel)
            except Exception:
                # Fallback to plain text if markdown rendering fails
                panel = Panel(text, title=f"[bold green]{title}[/bold green]", 
                            border_style="green", padding=(1, 2))
                self.console.print(panel)
        else:
            # For plain text, use streaming display
            self.console.print(f"\n[bold green]{title}:[/bold green]")
            
            # Stream text word by word for better readability
            words = text.split()
            current_line = ""
            
            for word in words:
                current_line += word + " "
                # Print line if it gets too long or we hit a natural break
                if len(current_line) > 80 or word.endswith(('.', '!', '?', ':')):
                    self.console.print(current_line.strip())
                    current_line = ""
                    await asyncio.sleep(0.02)  # Small delay for streaming effect
                
            # Print any remaining text
            if current_line.strip():
                self.console.print(current_line.strip())
    
    async def chat_with_claude(self, user_message: str) -> None:
        """Send a message to Claude with current context and improved streaming display."""
        if not CLAUDE_SDK_AVAILABLE:
            self.console.print("[bold red]❌ Claude Code SDK is not available.[/bold red] Please install it first.")
            return
        
        # Sanitize user input to prevent encoding issues
        user_message = self._sanitize_text(user_message)
        if not user_message:
            self.console.print("[yellow]⚠️  Please enter a valid message.[/yellow]")
            return
        
        # Build the full prompt with context
        if self.current_context:
            rel_path = self.current_context['file_path'].relative_to(self.working_directory)
            prompt = f"""I have loaded a markdown file called '{rel_path}' with the following content:

---
{self._sanitize_text(self.current_context['content'])}
---

User question: {user_message}"""
        else:
            prompt = f"""I'm using a markdown chatbot, but no specific file is currently loaded. 
Here's my question: {user_message}"""
        
        # Enhanced progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]🤖 Claude is thinking..."),
            transient=True
        ) as progress:
            task = progress.add_task("thinking", total=None)
            
            response_received = False
            try:
                async for message in query(prompt=prompt):
                    if not response_received:
                        progress.stop()
                        response_received = True
                    
                    # Enhanced message processing with comprehensive filtering
                    content_to_display = None
                    
                    if hasattr(message, 'content'):
                        if isinstance(message.content, list):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    text_content = self._sanitize_text(str(block.text))
                                    if text_content and not self._is_system_message(text_content):
                                        content_to_display = text_content
                                        break  # Use first valid content block
                        elif hasattr(message.content, 'text'):
                            text_content = self._sanitize_text(str(message.content.text))
                            if text_content and not self._is_system_message(text_content):
                                content_to_display = text_content
                        else:
                            # Handle other content types - be less restrictive
                            content_str = self._sanitize_text(str(message.content))
                            if (content_str and not self._is_system_message(content_str)):
                                content_to_display = content_str
                    else:
                        # Handle messages without content attribute - be less restrictive
                        msg_str = self._sanitize_text(str(message))
                        # Only display if it looks like genuine user-facing content
                        if (msg_str and 
                            not self._is_system_message(msg_str) and
                            len(msg_str) > 10):  # Reduced length requirement
                            content_to_display = msg_str
                    
                    # Display content only if it passed all filters
                    if content_to_display:
                        await self._stream_text_output(content_to_display)
                            
            except Exception as e:
                if not response_received:
                    progress.stop()
                error_msg = self._sanitize_text(str(e))
                self.console.print(f"[bold red]❌ Error communicating with Claude:[/bold red] {error_msg}")
                
        # Show helpful next steps
        self._show_conversation_tips()
    
    def _looks_like_markdown(self, text: str) -> bool:
        """Enhanced heuristic to detect if text contains markdown formatting."""
        if not text or len(text) < 3:
            return False
            
        markdown_indicators = [
            r'^#{1,6}\s',  # Headers
            r'\*\*.*\*\*',  # Bold
            r'\*.*\*',  # Italic (but not bold)
            r'`[^`]+`',  # Inline code
            r'^```',  # Code blocks
            r'^\s*[-*+]\s',  # Lists
            r'^\s*\d+\.\s',  # Numbered lists
            r'\[.*\]\(.*\)',  # Links
            r'^\|.*\|.*\|',  # Tables (at least 2 pipes)
            r'^\s*\|.*\|.*\|',  # Tables with leading spaces
            r'^>\s',  # Blockquotes
            r'^---+\s*$',  # Horizontal rules
            r'^\s*\|[\s\-:]*\|',  # Table separators
        ]
        
        for pattern in markdown_indicators:
            if re.search(pattern, text, re.MULTILINE):
                return True
        
        # Additional checks for tables
        lines = text.split('\n')
        table_line_count = 0
        for line in lines:
            if '|' in line and line.count('|') >= 2:
                table_line_count += 1
                if table_line_count >= 2:  # If we have at least 2 lines with pipes, likely a table
                    return True
                
        return False
    
    def _show_conversation_tips(self) -> None:
        """Show helpful tips after each response."""
        tips = [
            "💡 Ask follow-up questions about the content",
            "💡 Try 'load <number>' to switch to a different file",
            "💡 Use 'list' to see all available files",
            "💡 Type 'help' to see all commands"
        ]
        
        # Rotate tips to show different ones
        import random
        tip = random.choice(tips)
        self.console.print(f"\n[dim]{tip}[/dim]")
    
    def run(self) -> None:
        """Main chatbot loop."""
        # Enhanced welcome banner with improved system status detection
        system_status = ""
        if CLAUDE_SDK_AVAILABLE:
            config_status = _detect_claude_config()
            if config_status['has_valid_config']:
                method_name = {
                    'api_key': 'API Key',
                    'bedrock': 'Bedrock',
                    'pro_max': 'Pro/Max'
                }.get(config_status['method'], 'Unknown')
                system_status = f"[bold green]✓ Ready for AI chat ({method_name})[/bold green]"
            else:
                system_status = "[bold yellow]⚠️  Configuration needed[/bold yellow]"
        else:
            system_status = "[bold red]❌ SDK not available[/bold red]"
        
        welcome_panel = Panel(
            "[bold cyan]🤖 Welcome to Enhanced Markdown Chat![/bold cyan]\n" +
            "[dim]A powerful terminal chatbot with Claude Code SDK integration[/dim]\n\n" +
            f"[bold]Status:[/bold] {system_status}\n" +
            f"[bold]Files:[/bold] {len(self.markdown_files)} markdown files discovered\n\n" +
            "[dim]🚀 Quick start: Type [bold cyan]'help'[/bold cyan] for commands or [bold cyan]'list'[/bold cyan] to browse files[/dim]",
            title="[bold magenta]Markdown Chat v3.0[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(welcome_panel)
        
        # Check Claude SDK availability
        if not CLAUDE_SDK_AVAILABLE:
            self.console.print("[bold red]⚠️  Warning:[/bold red] claude-code-sdk not available. Install with: [bold cyan]uv add claude-code-sdk[/bold cyan]")
        
        # Show files initially
        self.list_content()
        
        while True:
            try:
                # Enhanced prompt with context indication and better guidance
                context_indicator = ""
                context_info = ""
                if self.current_context:
                    rel_path = self.current_context['file_path'].relative_to(self.working_directory)
                    context_indicator = f" [dim]({rel_path.name})[/dim]"
                    lines = len(self.current_context['content'].splitlines())
                    context_info = f" [dim]• {lines:,} lines loaded[/dim]"
                
                # Show current status
                status_line = f"\n[bold blue]💬 You{context_indicator}{context_info}:[/bold blue]"
                self.console.print(status_line, end=" ")
                
                try:
                    user_input = input().strip()
                except (EOFError, KeyboardInterrupt):
                    self.console.print("\n[bold cyan]👋 Goodbye![/bold cyan]")
                    break
                
                if not user_input:
                    # Show rotating helpful tips for empty input
                    empty_tips = [
                        "[dim]💡 Type a question about the loaded file, or 'help' for commands[/dim]",
                        "[dim]💡 Try: 'summarize this', 'what is this about?', or 'explain key points'[/dim]",
                        "[dim]💡 Use 'list' to see files, 'load <number>' to switch files[/dim]"
                    ]
                    import random
                    self.console.print(random.choice(empty_tips))
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    goodbye_panel = Panel(
                        "[bold cyan]👋 Thanks for using Markdown Chat![/bold cyan]\n" +
                        "[dim]Hope you found it helpful![/dim]",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                    self.console.print(goodbye_panel)
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.lower() == 'list':
                    self.console.print()  # Add spacing
                    self.list_content()
                elif user_input.lower() == 'show':
                    self.console.print()  # Add spacing
                    self.show_current_context()
                elif user_input.lower() == 'pwd':
                    self.console.print()  # Add spacing
                    self.show_current_directory()
                elif user_input.lower() == 'up':
                    self.go_up_directory()
                elif user_input.lower() in ['refresh', 'reload']:
                    self.console.print("[bold blue]🔄 Refreshing content...[/bold blue]")
                    self.discover_content()
                    self.list_content()
                elif user_input.lower().startswith('cd '):
                    try:
                        folder_num = int(user_input.split()[1])
                        self.change_directory(folder_num)
                    except (IndexError, ValueError):
                        error_panel = Panel(
                            "[bold red]Invalid command format[/bold red]\n\n" +
                            "[bold]Correct usage:[/bold] [bold cyan]cd <number>[/bold cyan]\n\n" +
                            "[dim]Examples:[/dim]\n" +
                            "[dim]• cd 1  (enter the first folder)[/dim]\n" +
                            "[dim]• cd 3  (enter the third folder)[/dim]\n\n" +
                            "[dim]Use 'list' to see folder numbers[/dim]",
                            title="⚠️  Usage Error",
                            border_style="red"
                        )
                        self.console.print(error_panel)
                elif user_input.lower().startswith('load '):
                    try:
                        item_num = int(user_input.split()[1])
                        self.load_markdown_file(item_num)
                    except (IndexError, ValueError):
                        error_panel = Panel(
                            "[bold red]Invalid command format[/bold red]\n\n" +
                            "[bold]Correct usage:[/bold] [bold cyan]load <number>[/bold cyan]\n\n" +
                            "[dim]Examples:[/dim]\n" +
                            "[dim]• load 4  (loads the 4th item if it's a file)[/dim]\n" +
                            "[dim]• load 7  (loads the 7th item if it's a file)[/dim]\n\n" +
                            "[dim]Note: Only markdown files can be loaded, not folders[/dim]\n" +
                            "[dim]Use 'list' to see item numbers and types[/dim]",
                            title="⚠️  Usage Error",
                            border_style="red"
                        )
                        self.console.print(error_panel)
                else:
                    # Chat with Claude
                    if CLAUDE_SDK_AVAILABLE:
                        await_result = asyncio.run(self.chat_with_claude(user_input))
                    else:
                        sdk_error_panel = Panel(
                            "[bold red]Claude Code SDK not available[/bold red]\n\n" +
                            "[bold]To enable AI chat:[/bold]\n" +
                            "[dim]1. Install the SDK:[/dim] [bold cyan]uv add claude-code-sdk[/bold cyan]\n" +
                            "[dim]2. Configure authentication (choose one):[/dim]\n" +
                            "[dim]   • API Key:[/dim] [bold cyan]export ANTHROPIC_API_KEY=your_key[/bold cyan]\n" +
                            "[dim]   • Pro/Max Plan:[/dim] [bold cyan]claude[/bold cyan] [dim](authenticate in CLI)[/dim]\n" +
                            "[dim]   • Bedrock:[/dim] [bold cyan]export CLAUDE_CODE_USE_BEDROCK=1[/bold cyan] [dim](+ AWS config)[/dim]\n" +
                            "[dim]3. Restart the app[/dim]\n\n" +
                            "[dim]You can still use file management commands (list, load, show)[/dim]",
                            title="⚠️  SDK Required",
                            border_style="red",
                            padding=(1, 2)
                        )
                        self.console.print(sdk_error_panel)
                        
            except KeyboardInterrupt:
                self.console.print("\n[bold cyan]👋 Goodbye![/bold cyan]")
                break
            except Exception as e:
                self.console.print(f"[bold red]❌ An error occurred:[/bold red] {e}")


def _detect_claude_config():
    """Detect which Claude Code SDK authentication method is configured."""
    config_info = {
        'has_valid_config': False,
        'status_message': 'No configuration detected',
        'method': None
    }
    
    # Method 1: Check for Anthropic API Key
    if os.getenv('ANTHROPIC_API_KEY'):
        config_info['has_valid_config'] = True
        config_info['status_message'] = 'Anthropic API Key configured'
        config_info['method'] = 'api_key'
        return config_info
    
    # Method 2: Check for Amazon Bedrock configuration
    if os.getenv('CLAUDE_CODE_USE_BEDROCK'):
        # Check for AWS credentials
        aws_configured = False
        
        # Check for AWS environment variables
        if (os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY')):
            aws_configured = True
        
        # Check for AWS CLI credentials (basic check)
        aws_config_path = os.path.expanduser('~/.aws/credentials')
        aws_config_dir = os.path.expanduser('~/.aws/config')
        if os.path.isfile(aws_config_path) or os.path.isfile(aws_config_dir):
            aws_configured = True
        
        if aws_configured:
            config_info['has_valid_config'] = True
            config_info['status_message'] = 'Amazon Bedrock configured'
            config_info['method'] = 'bedrock'
            return config_info
        else:
            config_info['has_valid_config'] = False
            config_info['status_message'] = 'Bedrock enabled but AWS credentials not found'
            return config_info
    
    # Method 3: Check for Pro/Max plan authentication
    # This is harder to detect programmatically, but we can check for Claude CLI presence
    # and attempt to infer if user might be authenticated
    
    # Check if claude CLI might be available (common installation paths)
    claude_cli_paths = [
        '/usr/local/bin/claude',
        '/opt/homebrew/bin/claude',
        os.path.expanduser('~/.local/bin/claude'),
    ]
    
    claude_cli_available = False
    for path in claude_cli_paths:
        if os.path.isfile(path):
            claude_cli_available = True
            break
    
    # Also check if claude is in PATH
    if not claude_cli_available:
        try:
            import subprocess
            result = subprocess.run(['which', 'claude'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0 and result.stdout.strip():
                claude_cli_available = True
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
    
    if claude_cli_available:
        # Claude CLI is available, user might be authenticated via Pro/Max plan
        # We can't easily check if they're actually logged in without running claude commands
        # So we'll be optimistic and assume they might have valid authentication
        config_info['has_valid_config'] = True
        config_info['status_message'] = 'Claude CLI detected - Pro/Max authentication possible'
        config_info['method'] = 'pro_max'
        return config_info
    
    # If none of the above, no valid configuration detected
    possible_reasons = []
    if not os.getenv('ANTHROPIC_API_KEY'):
        possible_reasons.append('No API key')
    if not os.getenv('CLAUDE_CODE_USE_BEDROCK'):
        possible_reasons.append('Bedrock not enabled')
    if not claude_cli_available:
        possible_reasons.append('Claude CLI not found')
    
    config_info['status_message'] = f"Missing: {', '.join(possible_reasons)}"
    return config_info


def main():
    """Entry point for the markdown chatbot."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Markdown Chat - Terminal chatbot with Claude Code SDK")
    parser.add_argument("--directory", "-d", default=".", 
                       help="Directory to search for markdown files (default: current directory)")
    
    args = parser.parse_args()
    
    # Initialize console for main function
    main_console = Console()
    
    # Verify the directory exists
    if not os.path.isdir(args.directory):
        main_console.print(f"[bold red]❌ Directory not found:[/bold red] {args.directory}")
        sys.exit(1)
    
    # Check Claude Code SDK configuration and show warnings only if no valid configuration is detected
    if CLAUDE_SDK_AVAILABLE:
        config_status = _detect_claude_config()
        if not config_status['has_valid_config']:
            config_warning_panel = Panel(
                "[bold yellow]⚠️  Claude Code SDK Configuration[/bold yellow]\n\n" +
                "No valid configuration detected. Claude Code SDK supports three authentication methods:\n\n" +
                "[bold]1. Anthropic API Key (Direct):[/bold]\n" +
                "[dim]   export ANTHROPIC_API_KEY=your_key_here[/dim]\n\n" +
                "[bold]2. Pro/Max Plan (Web Authentication):[/bold]\n" +
                "[dim]   Run 'claude' in terminal and authenticate with your Pro/Max account[/dim]\n" +
                "[dim]   Visit: https://support.anthropic.com/en/articles/11145838[/dim]\n\n" +
                "[bold]3. Amazon Bedrock (AWS):[/bold]\n" +
                "[dim]   export CLAUDE_CODE_USE_BEDROCK=1[/dim]\n" +
                "[dim]   Configure AWS credentials (aws configure or environment variables)[/dim]\n" +
                "[dim]   Visit: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock[/dim]\n\n" +
                f"[dim]Current status: {config_status['status_message']}[/dim]",
                title="[yellow]Authentication Required[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
            main_console.print(config_warning_panel)
    
    # Initialize and run the chatbot
    chatbot = MarkdownChatbot(working_directory=args.directory)
    chatbot.run()


if __name__ == "__main__":
    main()