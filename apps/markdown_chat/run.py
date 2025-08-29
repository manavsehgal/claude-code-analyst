#!/usr/bin/env python3
"""
Markdown Chat - A terminal UI chatbot powered by Claude Code SDK
that can navigate and discuss markdown files in the current directory.
"""

import os
import sys
import glob
import asyncio
from pathlib import Path
from typing import List, Optional

# Add a graceful fallback for the claude-code-sdk import
try:
    from claude_code_sdk import query
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    print("Warning: claude-code-sdk not available. Install with: uv add claude-code-sdk")
    CLAUDE_SDK_AVAILABLE = False


class MarkdownChatbot:
    """A terminal-based chatbot that can navigate and discuss markdown files."""
    
    def __init__(self, working_directory: str = "."):
        self.working_directory = Path(working_directory).resolve()
        self.markdown_files = []
        self.current_context = None
        self.discover_markdown_files()
    
    def discover_markdown_files(self) -> None:
        """Discover all markdown files in the working directory and subdirectories."""
        patterns = ["**/*.md", "**/*.markdown"]
        self.markdown_files = []
        
        for pattern in patterns:
            files = glob.glob(str(self.working_directory / pattern), recursive=True)
            self.markdown_files.extend([Path(f) for f in files])
        
        # Sort files by name for consistent ordering
        self.markdown_files.sort(key=lambda x: x.name.lower())
        
        print(f"📁 Discovered {len(self.markdown_files)} markdown files in {self.working_directory}")
    
    def list_markdown_files(self) -> None:
        """Display all discovered markdown files with numbers for easy selection."""
        if not self.markdown_files:
            print("No markdown files found in the current directory.")
            return
        
        print("\n📄 Available Markdown Files:")
        print("-" * 50)
        for i, file_path in enumerate(self.markdown_files, 1):
            rel_path = file_path.relative_to(self.working_directory)
            print(f"{i:2}. {rel_path}")
        print("-" * 50)
    
    def load_markdown_file(self, file_index: int) -> Optional[str]:
        """Load content from a markdown file by index."""
        if 1 <= file_index <= len(self.markdown_files):
            file_path = self.markdown_files[file_index - 1]
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.current_context = {
                    'file_path': file_path,
                    'content': content
                }
                rel_path = file_path.relative_to(self.working_directory)
                print(f"✅ Loaded: {rel_path} ({len(content)} characters)")
                return content
            except Exception as e:
                print(f"❌ Error loading file: {e}")
                return None
        else:
            print("❌ Invalid file number. Use 'list' to see available files.")
            return None
    
    def show_help(self) -> None:
        """Display help information."""
        help_text = """
🤖 Markdown Chat Commands:
  
  list                  - Show all available markdown files
  load <number>         - Load a specific markdown file by number
  show                  - Display currently loaded file info
  help                  - Show this help message
  quit, exit, q         - Exit the chatbot
  
  📝 Chat with Claude:
  Just type any question or message to chat with Claude about the loaded markdown file!
  
  Examples:
    load 1              - Load the first markdown file
    summarize this      - Ask Claude to summarize the loaded file
    what is this about? - Ask Claude about the content
"""
        print(help_text)
    
    def show_current_context(self) -> None:
        """Show information about the currently loaded file."""
        if self.current_context:
            rel_path = self.current_context['file_path'].relative_to(self.working_directory)
            content_length = len(self.current_context['content'])
            lines = self.current_context['content'].count('\n') + 1
            print(f"📄 Current file: {rel_path}")
            print(f"📊 Size: {content_length} characters, {lines} lines")
        else:
            print("❌ No file currently loaded. Use 'load <number>' to load a file.")
    
    async def chat_with_claude(self, user_message: str) -> None:
        """Send a message to Claude with current context."""
        if not CLAUDE_SDK_AVAILABLE:
            print("❌ Claude Code SDK is not available. Please install it first.")
            return
        
        # Build the full prompt with context
        if self.current_context:
            rel_path = self.current_context['file_path'].relative_to(self.working_directory)
            prompt = f"""
I have loaded a markdown file called '{rel_path}' with the following content:

---
{self.current_context['content']}
---

User question: {user_message}
"""
        else:
            prompt = f"""
I'm using a markdown chatbot, but no specific file is currently loaded. 
Here's my question: {user_message}
"""
        
        print("🤖 Claude is thinking...")
        
        try:
            async for message in query(prompt=prompt):
                if hasattr(message, 'content'):
                    # Handle different message types from the Claude Code SDK
                    if isinstance(message.content, list):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                print(block.text)
                    elif hasattr(message.content, 'text'):
                        print(message.content.text)
                    else:
                        print(str(message.content))
                else:
                    print(str(message))
        except Exception as e:
            print(f"❌ Error communicating with Claude: {e}")
    
    def run(self) -> None:
        """Main chatbot loop."""
        print("🤖 Welcome to Markdown Chat!")
        print("A terminal chatbot powered by Claude Code SDK")
        print("Type 'help' for commands or 'quit' to exit.")
        
        self.list_markdown_files()
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.lower() == 'list':
                    self.list_markdown_files()
                elif user_input.lower() == 'show':
                    self.show_current_context()
                elif user_input.lower().startswith('load '):
                    try:
                        file_num = int(user_input.split()[1])
                        self.load_markdown_file(file_num)
                    except (IndexError, ValueError):
                        print("❌ Usage: load <number>")
                else:
                    # Chat with Claude
                    if CLAUDE_SDK_AVAILABLE:
                        asyncio.run(self.chat_with_claude(user_input))
                    else:
                        print("❌ Claude Code SDK not available. Install with: uv add claude-code-sdk")
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")


def main():
    """Entry point for the markdown chatbot."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Markdown Chat - Terminal chatbot with Claude Code SDK")
    parser.add_argument("--directory", "-d", default=".", 
                       help="Directory to search for markdown files (default: current directory)")
    
    args = parser.parse_args()
    
    # Verify the directory exists
    if not os.path.isdir(args.directory):
        print(f"❌ Directory not found: {args.directory}")
        sys.exit(1)
    
    # Check for ANTHROPIC_API_KEY environment variable
    if not os.getenv('ANTHROPIC_API_KEY') and CLAUDE_SDK_AVAILABLE:
        print("⚠️  Warning: ANTHROPIC_API_KEY environment variable not set.")
        print("   You may need to set this for Claude Code SDK to work properly.")
    
    # Initialize and run the chatbot
    chatbot = MarkdownChatbot(working_directory=args.directory)
    chatbot.run()


if __name__ == "__main__":
    main()