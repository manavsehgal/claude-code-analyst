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
import yaml
from pathlib import Path
from typing import List, Optional, AsyncGenerator, Dict, Any

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
        self.current_folder = None  # Currently selected folder from config
        self.markdown_files = []
        self.configured_folders = []  # Folders from config
        self.current_context = None
        self.console = Console()
        self.config = self._load_config()
        self._initialize_folders()
        self.discover_content()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.yml file."""
        config_path = Path(__file__).parent / "config.yml"
        default_config = {
            'navigation': {
                'folders': [
                    {'name': 'projects', 'path': 'projects', 'description': 'Project files'},
                    {'name': 'transcripts', 'path': 'transcripts', 'description': 'Transcripts'},
                    {'name': 'markdown', 'path': 'markdown', 'description': 'Markdown documents'}
                ]
            },
            'display': {
                'show_file_sizes': True,
                'show_modification_dates': True,
                'recursive_search': True
            }
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    if loaded_config:
                        return loaded_config
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not load config.yml: {e}[/yellow]")
        
        return default_config
    
    def _initialize_folders(self) -> None:
        """Initialize configured folders that exist."""
        self.configured_folders = []
        for folder_config in self.config.get('navigation', {}).get('folders', []):
            folder_path = self.working_directory / folder_config['path']
            if folder_path.exists() and folder_path.is_dir():
                self.configured_folders.append({
                    'name': folder_config['name'],
                    'path': folder_path,
                    'description': folder_config.get('description', ''),
                    'config': folder_config
                })
    
    def discover_content(self) -> None:
        """Discover markdown files based on current navigation state."""
        with self.console.status("[bold blue]Discovering content...", spinner="dots"):
            if self.current_folder is None:
                # At root - just show configured folders
                self.markdown_files = []
            else:
                # In a folder - discover all markdown files recursively
                self._discover_markdown_files()
            
        # Enhanced discovery feedback
        if self.current_folder:
            total_files = len(self.markdown_files)
            folder_name = self.current_folder['name']
            if total_files > 0:
                self.console.print(
                    f"[bold green]✓ Found {total_files} markdown files[/bold green] "
                    f"in [dim]{folder_name}[/dim]"
                )
            else:
                self.console.print(f"[bold yellow]⚠️  No markdown files found[/bold yellow] in [dim]{folder_name}[/dim]")
        else:
            total_folders = len(self.configured_folders)
            if total_folders > 0:
                self.console.print(f"[bold green]✓ {total_folders} configured folders available[/bold green]")
            else:
                self.console.print("[bold yellow]⚠️  No configured folders found[/bold yellow]")
    
    def _discover_markdown_files(self) -> None:
        """Discover all markdown files recursively in current folder."""
        self.markdown_files = []
        
        if not self.current_folder:
            return
        
        folder_path = self.current_folder['path']
        
        # Find all markdown files recursively
        patterns = ["**/*.md", "**/*.markdown"]
        for pattern in patterns:
            files = glob.glob(str(folder_path / pattern), recursive=True)
            self.markdown_files.extend([Path(f) for f in files])
        
        # Sort files by relative path for better organization
        self.markdown_files.sort(key=lambda x: str(x.relative_to(folder_path)).lower())
    
    def list_content(self) -> None:
        """Display configured folders or markdown files based on navigation state."""
        if self.current_folder is None:
            # At root - show configured folders
            self._list_configured_folders()
        else:
            # In a folder - show all markdown files
            self._list_markdown_files()
    
    def _list_configured_folders(self) -> None:
        """Display configured folders from config.yml."""
        if not self.configured_folders:
            no_content_panel = Panel(
                "[bold yellow]No configured folders found[/bold yellow]\n\n" +
                "[dim]💡 Tips:[/dim]\n" +
                "[dim]• Check config.yml for folder configuration[/dim]\n" +
                "[dim]• Ensure configured folders exist in the working directory[/dim]",
                title="📁 Folder Configuration",
                border_style="yellow",
                padding=(1, 2)
            )
            self.console.print(no_content_panel)
            return
        
        # Show current location
        self.console.print("📂 [bold cyan]Navigation Root[/bold cyan]")
        
        # Create table for folders
        table = Table(title=f"📋 Configured Folders ({len(self.configured_folders)} available)", 
                     box=box.ROUNDED, title_style="bold cyan")
        table.add_column("#", style="bold blue", width=3, justify="right")
        table.add_column("Folder", style="bold yellow", min_width=20)
        table.add_column("Description", style="white", min_width=30)
        table.add_column("Files", style="dim", justify="right", width=15)
        
        for idx, folder in enumerate(self.configured_folders, 1):
            # Count markdown files in this folder
            file_count = len(glob.glob(str(folder['path'] / "**/*.md"), recursive=True)) + \
                        len(glob.glob(str(folder['path'] / "**/*.markdown"), recursive=True))
            
            table.add_row(
                str(idx), 
                f"📁 {folder['name']}", 
                folder['description'],
                f"{file_count} files"
            )
        
        self.console.print(table)
        self.console.print("[dim]💡 Enter folder number to view all markdown files in that folder[/dim]")
    
    def _list_markdown_files(self) -> None:
        """Display all markdown files in the current folder."""
        if not self.markdown_files:
            folder_name = self.current_folder['name'] if self.current_folder else "unknown"
            no_content_panel = Panel(
                f"[bold yellow]No markdown files found in {folder_name}[/bold yellow]\n\n" +
                "[dim]💡 Tips:[/dim]\n" +
                "[dim]• Use 'back' to return to folder selection[/dim]\n" +
                "[dim]• Create markdown files in this folder[/dim]",
                title="📄 File Discovery",
                border_style="yellow",
                padding=(1, 2)
            )
            self.console.print(no_content_panel)
            return
        
        # Show current folder
        folder_name = self.current_folder['name'] if self.current_folder else "unknown"
        self.console.print(f"📂 Current Folder: [bold cyan]{folder_name}[/bold cyan]")
        
        # Create table for files
        table = Table(title=f"📋 Markdown Files ({len(self.markdown_files)} files)", 
                     box=box.ROUNDED, title_style="bold cyan")
        table.add_column("#", style="bold blue", width=3, justify="right")
        table.add_column("File", style="green", min_width=40)
        table.add_column("Size", style="dim", justify="right", width=10)
        
        folder_path = self.current_folder['path']
        
        for idx, file_path in enumerate(self.markdown_files, 1):
            try:
                # Show relative path from the folder
                rel_path = file_path.relative_to(folder_path)
                stat = file_path.stat()
                size = stat.st_size
                
                # Format size nicely
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
            except (OSError, ValueError):
                rel_path = file_path.name
                size_str = "--"
            
            # Highlight currently loaded file
            if (self.current_context and 
                self.current_context['file_path'] == file_path):
                table.add_row(str(idx), f"📄 [bold cyan]{rel_path}[/bold cyan] ✓", size_str)
            else:
                table.add_row(str(idx), f"📄 {rel_path}", size_str)
        
        self.console.print(table)
        self.console.print("[dim]💡 Use 'load <number>' to load a file • Use 'back' to return to folders[/dim]")
    
    def load_markdown_file(self, item_index: int) -> Optional[str]:
        """Load content from a markdown file by index."""
        # Only works when we're in a folder viewing files
        if self.current_folder is None:
            self.console.print("[bold red]❌ Please select a folder first.[/bold red] Enter a folder number to view its files.")
            return None
        
        if not (1 <= item_index <= len(self.markdown_files)):
            self.console.print(f"[bold red]❌ Invalid file number.[/bold red] Choose between 1 and {len(self.markdown_files)}.")
            return None
        
        file_path = self.markdown_files[item_index - 1]
        try:
            with self.console.status(f"[bold blue]Loading file {item_index}...", spinner="dots"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            self.current_context = {
                'file_path': file_path,
                'content': content
            }
            
            # Show relative path from the folder
            folder_path = self.current_folder['path']
            rel_path = file_path.relative_to(folder_path)
            
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
    
    def enter_folder(self, folder_index: int) -> bool:
        """Enter a configured folder by index."""
        if self.current_folder is not None:
            self.console.print("[bold yellow]⚠️ Already in a folder.[/bold yellow] Use 'back' to return to folder selection.")
            return False
        
        if not (1 <= folder_index <= len(self.configured_folders)):
            self.console.print(f"[bold red]❌ Invalid folder number.[/bold red] Choose between 1 and {len(self.configured_folders)}.")
            return False
        
        self.current_folder = self.configured_folders[folder_index - 1]
        
        with self.console.status(f"[bold blue]Loading {self.current_folder['name']} files...", spinner="dots"):
            self.discover_content()
        
        self.console.print(f"[bold green]✓ Entered folder:[/bold green] [bold cyan]{self.current_folder['name']}[/bold cyan]")
        self.list_content()
        return True
    
    def go_back(self) -> bool:
        """Go back to folder selection."""
        if self.current_folder is None:
            self.console.print("[bold yellow]⚠️ Already at folder selection.[/bold yellow]")
            return False
        
        folder_name = self.current_folder['name']
        self.current_folder = None
        self.markdown_files = []
        
        self.console.print(f"[bold green]✓ Returned from:[/bold green] [bold cyan]{folder_name}[/bold cyan]")
        self.list_content()
        return True
    
    def show_help(self) -> None:
        """Display comprehensive help information with enhanced guidance."""
        # Create a comprehensive help table
        help_table = Table(title="🤖 Markdown Chat Commands", box=box.ROUNDED, title_style="bold cyan")
        help_table.add_column("Command", style="bold yellow", width=22)
        help_table.add_column("Description", style="white")
        help_table.add_column("Example", style="dim", width=15)
        
        # Navigation commands
        help_table.add_row("list", "Show current view (folders or files)", "list")
        help_table.add_row("<number>", "Enter a folder (when at root)", "1")
        help_table.add_row("back", "Return to folder selection", "back")
        help_table.add_row("load <number>", "Load a markdown file into context", "load 5")
        
        # Information commands
        help_table.add_row("show", "Display current file information", "show")
        help_table.add_row("refresh", "Refresh current listing", "refresh")
        
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
            "• Enter folder number to explore markdown files\n" +
            "• Use 'load <number>' to load files for AI conversation\n" +
            "• Use 'back' to return to folder selection\n" +
            "• Use 'show' to see current navigation state",
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
        """Show enhanced information about the currently loaded file and current navigation state."""
        # Show current navigation state
        if self.current_folder is None:
            location = "Folder Selection"
            details = f"📁 Available Folders: {len(self.configured_folders)}"
        else:
            location = f"{self.current_folder['name']}"
            details = f"📄 Files: {len(self.markdown_files)}"
        
        dir_info = Panel(
            f"[bold blue]📂 Current Location:[/bold blue] [bold cyan]{location}[/bold cyan]\n" +
            f"[dim]{details}[/dim]",
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
                "[dim]• Enter a [bold cyan]number[/bold cyan] to select folders or load files[/dim]\n" +
                "[dim]• Use [bold cyan]'load <number>'[/bold cyan] to load files for chat[/dim]",
                title="📁 Context Status",
                border_style="yellow",
                padding=(1, 2)
            )
            self.console.print(no_context_panel)
    
    
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
            
            # Claude Code SDK specific patterns
            '(subtype=', '(data=', 'duration_ms=', 'session_id=', 'usage={',
            'total_cost_usd=', 'output_tokens=', 'input_tokens=', 'is_error=',
            'num_turns=', 'cache_creation_input_tokens=', 'cache_read_input_tokens=',
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
            r'^\(subtype=.*\)$',  # Claude Code SDK message format
            r'^\(data=.*\)$',  # Claude Code SDK data format
            r'duration_ms=\d+',  # SDK timing information
            r'session_id=[\'\"][0-9a-f-]+[\'\"]',  # SDK session ID
            r'total_cost_usd=[\d\.]+',  # SDK cost information
            r'usage=\{.*\}',  # SDK usage statistics
            r'result=[\'\"].*[\'\"].*\)$',  # SDK result messages
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
        
        # Aggressive whitespace normalization to prevent excessive spacing
        # Remove excessive leading/trailing whitespace
        text = text.strip()
        
        # Normalize multiple consecutive newlines to maximum of 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove excessive leading whitespace at the beginning of content
        # This is specifically to fix table rendering with too much space before content
        text = re.sub(r'^\s*\n+', '', text)
        
        return text
    
    def _clean_content_for_display(self, text: str) -> str:
        """ULTRA-AGGRESSIVE content cleanup - zero tolerance for excessive whitespace."""
        if not text:
            return text
            
        # NUCLEAR OPTION: Strip all leading/trailing whitespace
        text = text.strip()
        
        # ELIMINATE multiple consecutive newlines completely - maximum 1 blank line
        text = re.sub(r'\n{2,}', '\n', text)
        
        # DESTROY any leading whitespace at the beginning
        text = re.sub(r'^\s*\n*', '', text)
        
        # OBLITERATE blank lines before table content
        text = re.sub(r'\n+\s*(?=\|)', '\n', text)
        
        # ANNIHILATE whitespace before any content that looks like a table
        text = re.sub(r'\n\s*\n+(?=\s*\w+.*\|)', '\n', text)
        
        # VAPORIZE space between sentences and tables
        text = re.sub(r'(\.)\s*\n+(?=\s*\w+.*\|)', r'\1\n', text)
        text = re.sub(r'(\.)\s*\n+(?=\s*\|)', r'\1\n', text)
        
        # ERADICATE any sequence of whitespace that could create visual gaps
        text = re.sub(r'\n\s*\n(?=\s)', '\n', text)
        
        # FINAL NUCLEAR STRIKE: Remove any remaining problematic whitespace patterns
        lines = text.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            # Skip completely empty lines unless they're between substantial content
            if not line.strip():
                # Only keep empty line if it's between two non-empty lines
                if (i > 0 and i < len(lines) - 1 and 
                    lines[i-1].strip() and lines[i+1].strip() and
                    not ('|' in lines[i+1])):
                    result_lines.append('')
            else:
                # Keep non-empty lines, but clean up internal spacing
                if '|' in line and line.count('|') >= 2:
                    # Table line - preserve formatting
                    result_lines.append(line)
                else:
                    # Regular text - clean up multiple spaces
                    cleaned = re.sub(r'\s{2,}', ' ', line.strip())
                    result_lines.append(cleaned)
        
        return '\n'.join(result_lines)
    
    def _is_substantial_content(self, text: str) -> bool:
        """STRICT quality check - only allow substantial, non-whitespace content."""
        if not text or len(text.strip()) < 10:
            return False
            
        # Count non-whitespace characters
        non_whitespace = len(re.sub(r'\s', '', text))
        total_length = len(text)
        
        # Require at least 30% non-whitespace content
        if total_length > 0 and (non_whitespace / total_length) < 0.3:
            return False
            
        # Must have actual words, not just punctuation and whitespace
        word_chars = len(re.findall(r'\w', text))
        if word_chars < 5:
            return False
            
        # Check for excessive newlines relative to content
        newline_count = text.count('\n')
        if newline_count > 5 and word_chars < newline_count * 3:
            return False
            
        return True
    
    def _nuclear_clean_content(self, text: str) -> str:
        """NUCLEAR OPTION: Destroy ALL whitespace that could cause spacing issues."""
        if not text:
            return text
        
        # COMPLETE WHITESPACE ANNIHILATION
        text = text.strip()
        
        # Remove ALL multiple newlines - only single newlines allowed
        text = re.sub(r'\n+', '\n', text)
        
        # Remove ALL leading whitespace from every line
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:  # Only keep non-empty lines
                cleaned_lines.append(stripped)
        
        # Join with single newlines only
        return '\n'.join(cleaned_lines)
    
    def _maximum_aggressive_clean(self, text: str) -> str:
        """MAXIMUM AGGRESSIVE cleaning - eliminate ALL possible spacing issues."""
        if not text:
            return text
        
        # Strip everything
        text = text.strip()
        
        # Split into lines for aggressive processing
        lines = text.split('\n')
        result_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()  # Remove trailing spaces
            
            # Skip completely empty lines
            if not line.strip():
                i += 1
                continue
                
            # Check if this starts a table (line contains pipes)
            if '|' in line and line.count('|') >= 2:
                # Found table start - ensure ZERO blank lines before it
                # Add the table line directly
                result_lines.append(line)
            else:
                # Regular content line
                result_lines.append(line)
            
            i += 1
        
        # Join with single newlines only - NO blank lines anywhere
        result = '\n'.join(result_lines)
        
        # Final aggressive cleanup - remove any remaining multiple newlines
        while '\n\n' in result:
            result = result.replace('\n\n', '\n')
            
        return result
    
    def _parse_markdown_tables(self, content: str) -> List[dict]:
        """Parse markdown tables from content and return structured data."""
        tables = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this looks like a table row
            if '|' in line and line.count('|') >= 2:
                # Found potential table start
                table_lines = []
                table_start = i
                
                # Collect all consecutive table lines
                while i < len(lines):
                    current_line = lines[i].strip()
                    if '|' in current_line and current_line:
                        table_lines.append(current_line)
                        i += 1
                    elif not current_line:  # Empty line, continue checking
                        i += 1
                    else:
                        break  # End of table
                
                if len(table_lines) >= 2:  # Valid table needs at least header + separator
                    # Parse table structure
                    headers = []
                    rows = []
                    separator_idx = -1
                    
                    for idx, table_line in enumerate(table_lines):
                        # Remove leading/trailing pipes and split
                        cells = [cell.strip() for cell in table_line.strip('|').split('|')]
                        
                        # Check if this is a separator line
                        if all(set(cell.strip()) <= set('-:| ') for cell in cells if cell.strip()):
                            separator_idx = idx
                        elif separator_idx == -1:  # Before separator = headers
                            if not headers:  # First row becomes headers
                                headers = cells
                        else:  # After separator = data rows
                            if cells and any(cell.strip() for cell in cells):  # Non-empty row
                                rows.append(cells)
                    
                    if headers and rows:
                        tables.append({
                            'headers': headers,
                            'rows': rows,
                            'start_line': table_start,
                            'end_line': i - 1
                        })
            else:
                i += 1
        
        return tables
    
    def _convert_markdown_to_rich(self, text: str) -> str:
        """Convert markdown formatting in text to Rich markup."""
        if not text or not isinstance(text, str):
            return str(text) if text is not None else ''
        
        # Convert common markdown patterns to Rich markup
        result = text
        
        # Headings: # H1 → [bold cyan]H1[/bold cyan]
        result = re.sub(r'^#{6}\s+(.+)$', r'[dim]\1[/dim]', result, flags=re.MULTILINE)  # H6
        result = re.sub(r'^#{5}\s+(.+)$', r'[italic]\1[/italic]', result, flags=re.MULTILINE)  # H5
        result = re.sub(r'^#{4}\s+(.+)$', r'[underline]\1[/underline]', result, flags=re.MULTILINE)  # H4
        result = re.sub(r'^#{3}\s+(.+)$', r'[bold yellow]\1[/bold yellow]', result, flags=re.MULTILINE)  # H3
        result = re.sub(r'^#{2}\s+(.+)$', r'[bold green]\1[/bold green]', result, flags=re.MULTILINE)  # H2
        result = re.sub(r'^#{1}\s+(.+)$', r'[bold cyan]\1[/bold cyan]', result, flags=re.MULTILINE)  # H1
        
        # Blockquotes: > text → [dim]▶ text[/dim]
        result = re.sub(r'^>\s*(.+)$', r'[dim]▶ \1[/dim]', result, flags=re.MULTILINE)
        
        # Horizontal rules: --- or *** → ────────────────
        result = re.sub(r'^(\*{3,}|-{3,}|_{3,})\s*$', r'[dim]────────────────[/dim]', result, flags=re.MULTILINE)
        
        # Unordered lists: - item → • item
        result = re.sub(r'^(\s*)([-*+])\s+(.+)$', r'\1[bold]•[/bold] \3', result, flags=re.MULTILINE)
        
        # Numbered lists: 1. item → 1. item (preserve but style number)
        result = re.sub(r'^(\s*)(\d+)\.\s+(.+)$', r'\1[bold cyan]\2.[/bold cyan] \3', result, flags=re.MULTILINE)
        
        # Code blocks: ```code``` → [dim]code[/dim] (simple handling for inline)
        result = re.sub(r'```([^`]+)```', r'[dim]\1[/dim]', result, flags=re.DOTALL)
        
        # Bold: **text** → [bold]text[/bold]
        result = re.sub(r'\*\*([^*]+)\*\*', r'[bold]\1[/bold]', result)
        
        # Italic: *text* → [italic]text[/italic] (but avoid matching **text**)
        result = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'[italic]\1[/italic]', result)
        
        # Inline code: `code` → [dim]code[/dim]
        result = re.sub(r'`([^`]+)`', r'[dim]\1[/dim]', result)
        
        # Links: [text](url) → [blue underline]text[/blue underline] (show styled link text)
        result = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'[blue underline]\1[/blue underline]', result)
        
        # Strikethrough: ~~text~~ → [strikethrough]text[/strikethrough]
        result = re.sub(r'~~([^~]+)~~', r'[strikethrough]\1[/strikethrough]', result)
        
        # Simple underlines: _text_ → [underline]text[/underline] (only if not part of file paths)
        result = re.sub(r'(?<![/\w])_([^_\s][^_]*[^_\s])_(?![/\w])', r'[underline]\1[/underline]', result)
        
        # Convert HTML line breaks to actual newlines for Rich rendering
        result = re.sub(r'<br\s*/?>', '\n', result, flags=re.IGNORECASE)
        
        return result.strip()
    
    def _render_rich_table(self, table_data: dict) -> Table:
        """Create a Rich Table widget from parsed table data with markdown formatting support."""
        # Create Rich table with clean styling
        rich_table = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="bold cyan",
            show_lines=False,
            pad_edge=False,
            collapse_padding=True
        )
        
        # Add columns with converted headers
        for header in table_data['headers']:
            formatted_header = self._convert_markdown_to_rich(header.strip())
            rich_table.add_column(formatted_header, overflow="fold")
        
        # Add rows with markdown conversion for each cell
        for row in table_data['rows']:
            # Ensure row has same number of cells as headers
            padded_row = row[:]
            while len(padded_row) < len(table_data['headers']):
                padded_row.append('')  # Fill missing cells
            
            # Convert each cell's markdown to Rich markup
            formatted_row = []
            for cell in padded_row[:len(table_data['headers'])]:
                formatted_cell = self._convert_markdown_to_rich(str(cell))
                formatted_row.append(formatted_cell)
            
            rich_table.add_row(*formatted_row)
        
        return rich_table
    
    def _display_clean_response(self, content: str) -> None:
        """Display response with proper table rendering using Rich Table widgets."""
        try:
            # Parse tables from content
            tables = self._parse_markdown_tables(content)
            
            if tables:
                # Content contains tables - render with proper formatting
                self.console.print(f"[bold green]🤖 Claude:[/bold green]")
                
                lines = content.split('\n')
                current_line = 0
                
                for table in tables:
                    # Print any content before this table
                    while current_line < table['start_line']:
                        line = lines[current_line].strip()
                        if line:
                            self.console.print(line)
                        current_line += 1
                    
                    # Render the table using Rich Table widget
                    rich_table = self._render_rich_table(table)
                    self.console.print(rich_table)
                    
                    # Skip the table lines
                    current_line = table['end_line'] + 1
                
                # Print any remaining content after last table
                while current_line < len(lines):
                    line = lines[current_line].strip()
                    if line:
                        self.console.print(line)
                    current_line += 1
            else:
                # No tables - use Rich markdown for better formatting
                if self._looks_like_markdown(content):
                    markdown_content = Markdown(content)
                    panel = Panel(
                        markdown_content,
                        title="[bold green]🤖 Claude[/bold green]",
                        border_style="green",
                        padding=(0, 1)  # Minimal padding
                    )
                    self.console.print(panel)
                else:
                    self.console.print(f"\n[bold green]🤖 Claude:[/bold green]")
                    self.console.print(content)
                    
        except Exception as e:
            # Fallback to simple display
            self.console.print(f"\n[bold green]🤖 Claude:[/bold green]")
            self.console.print(content)
    
    async def chat_with_claude(self, user_message: str) -> None:
        """Send a message to Claude - ULTRA SIMPLE: no streaming, just clean response."""
        if not CLAUDE_SDK_AVAILABLE:
            self.console.print("[bold red]❌ Claude Code SDK is not available.[/bold red] Please install it first.")
            return
        
        # Sanitize user input
        user_message = self._sanitize_text(user_message)
        if not user_message:
            self.console.print("[yellow]⚠️  Please enter a valid message.[/yellow]")
            return
        
        # Build prompt
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
        
        # Simple thinking indicator
        thinking_status = Status(
            "[bold blue]🤖 Claude is thinking...[/bold blue]",
            spinner="dots12"
        )
        
        response_received = False
        
        with thinking_status:
            try:
                # ULTRA SIMPLE: Just collect all content, no streaming whatsoever
                all_content = []
                
                async for message in query(prompt=prompt):
                    if hasattr(message, 'content'):
                        if isinstance(message.content, list):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    text = str(block.text)
                                    if text and not self._is_system_message(text):
                                        all_content.append(text)
                        elif hasattr(message.content, 'text'):
                            text = str(message.content.text)
                            if text and not self._is_system_message(text):
                                all_content.append(text)
                        elif message.content:
                            text = str(message.content)
                            if text and not self._is_system_message(text):
                                all_content.append(text)
                
                thinking_status.stop()
                
                # Process collected content
                if all_content:
                    # Take the longest content (most complete)
                    complete_response = max(all_content, key=len)
                    
                    # Clean and display ONCE - MAXIMUM AGGRESSIVE
                    cleaned_response = self._maximum_aggressive_clean(complete_response)
                    
                    if cleaned_response and len(cleaned_response.strip()) > 10:
                        self._display_clean_response(cleaned_response)
                        response_received = True
                        
            except Exception as e:
                thinking_status.stop()
                self.console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
        
        # Show tips if we got a response
        if response_received:
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
        """Show enhanced helpful tips after each response with better formatting."""
        tips = [
            "💡 Ask follow-up questions about the content",
            "💡 Try 'load <number>' to switch to a different file",
            "💡 Use 'list' to see all available files", 
            "💡 Type 'help' to see all commands",
            "💡 Enter folder number to explore its files",
            "💡 Use 'show' to see current file details"
        ]
        
        # Enhanced tips panel with better visual design
        import random
        tip = random.choice(tips)
        
        tip_panel = Panel(
            tip,
            border_style="dim",
            padding=(0, 1),
            box=box.ROUNDED
        )
        self.console.print(f"\n")
        self.console.print(tip_panel)
    
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
                elif user_input.lower() == 'back':
                    self.go_back()
                elif user_input.lower() in ['refresh', 'reload']:
                    self.console.print("[bold blue]🔄 Refreshing content...[/bold blue]")
                    self.discover_content()
                    self.list_content()
                elif user_input.isdigit():
                    # Handle direct number input for folder navigation
                    folder_num = int(user_input)
                    if self.current_folder is None:
                        # At root - enter folder
                        self.enter_folder(folder_num)
                    else:
                        # In folder - treat as file load
                        self.load_markdown_file(folder_num)
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