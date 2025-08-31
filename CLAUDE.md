# Claude Code Configuration

## Project Overview
This is a Python project for analyzing Claude Code interactions, managed by uv for dependency management and virtual environments.

## Common Commands

### Development Setup
```bash
# Install dependencies
uv sync

# Install development dependencies
uv sync --dev

# Run main script
uv run python main.py

# Run tests
uv run pytest tests/

# Run tests with timeout (default 300s per test)
uv run pytest tests/ --timeout=60
```

### Code Quality Tools
```bash
# Linting - Check code quality issues
uv run ruff check .
uv run ruff check --fix .  # Auto-fix issues

# Formatting - Format code with Black
uv run black .  # Format all Python files
uv run black --check .  # Check formatting without changes

# Type Checking - Static type analysis
uv run mypy .
uv run mypy scripts/ --ignore-missing-imports

# All-in-one quality check
uv run ruff check . && uv run black --check . && uv run mypy .
```

### Development Tools
The project includes these pre-configured development tools:

- **ruff** (v0.8.4+): Fast Python linter with 120-char line length, targets Python 3.13
- **black** (v24.11.0+): Code formatter with 120-char line length, ensures consistent style
- **mypy** (v1.14.1+): Static type checker for Python code
- **pytest** (v8.3.5+): Testing framework with automatic test discovery
- **pytest-timeout** (v2.3.1+): Prevents hanging tests (300s default timeout)
- **ipdb** (v0.13.13+): Interactive Python debugger for troubleshooting

## Core Project Structure
- `scripts/` - Python scripts for analysis tasks
- `tests/` - Test files following pytest conventions
- `docs/` - User documentation and guides
- `backlog/` - Project backlog and task tracking
- `apps/` - Streamlit applications with Claude Code SDK integration
- `apps/agent/` - Reusable agent capabilities package
- `main.py` - Main entry point

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use type hints for all function signatures
- Keep functions focused and testable
- Document complex logic with clear docstrings

## Testing Instructions
- Write tests in `tests/` directory
- Use pytest for test execution
- Follow test naming convention: `test_*.py`
- Aim for high test coverage on core functionality

## Repository Etiquette
- Never commit directly unless explicitly requested
- Always run tests before marking tasks complete
- Check for existing implementations before creating new files
- Prefer editing existing files over creating new ones

## Developer Environment
- Python >=3.13 required
- Uses uv for package management
- Virtual environment managed automatically by uv

## Available Tools

### Article to Markdown Converter
Convert web articles or local HTML files to clean markdown files with metadata and preserved images:

```bash
# Basic usage with web URL
uv run python scripts/article_to_md.py <URL>

# Basic usage with local HTML file
uv run python scripts/article_to_md.py <path-to-html-file>

# With custom output directory
uv run python scripts/article_to_md.py <URL-or-file-path> --output-dir <directory>
```

Features:
- Works with both web URLs and local HTML files
- Extracts main article content using readability algorithms
- Downloads and preserves images (for web sources) or handles local images
- Adds comprehensive metadata (title, date, word count, image count, etc.)
- Creates organized folder structure with kebab-case naming
- Automatically detects input type (URL vs local file path)

For detailed usage, see [Article to Markdown Guide](docs/article-to-md-guide.md)

### HTML Page Downloader
Download complete web pages as clean HTML archives with preserved images and metadata:

```bash
# Basic usage
uv run python scripts/html_downloader.py <URL>

# With custom output directory
uv run python scripts/html_downloader.py <URL> --output-dir <directory>

# Skip robots.txt check (use responsibly)
uv run python scripts/html_downloader.py <URL> --skip-robots
```

Features:
- Smart content extraction using readability algorithms
- Comprehensive metadata preservation (title, description, OpenGraph, Twitter cards, dates, authors)
- Intelligent image handling with proper HTTP headers for protected content
- Clean, well-formed HTML5 output with embedded responsive styling
- Source attribution and archive information
- Robust error handling and progress feedback

Output structure:
- `html/kebab-case-title/index.html` - Complete HTML document
- `html/kebab-case-title/images/` - All downloaded images referenced locally

The tool creates self-contained HTML archives perfect for offline reading, research, and documentation.

For detailed usage, see [HTML Page Downloader - User Guide](docs/html-downloader-guide.md)

### Mermaid Visualization Generator (Custom Command)
Create intuitive Mermaid.js visualizations from markdown content:

```bash
# Usage as Claude Code custom command
/mermaid <markdown-file-path>
```

Features:
- Analyzes markdown content to identify visualizable concepts
- Creates multiple Mermaid.js diagrams (flowcharts, timelines, mindmaps, etc.)
- Generates organized output in `mermaid/kebab-case-title/` folder
- Includes contextual text with each visualization
- Supports topics, workflows, processes, user journeys, timelines, and more

The command automatically:
1. Reads the specified markdown source file
2. Identifies key concepts and relationships
3. Creates appropriate Mermaid.js visualizations
4. Saves each diagram in a separate markdown file with context
5. Organizes output in a dedicated folder structure

For detailed usage, see [Mermaid Visualization Generator - User Guide](docs/mermaid-visualization-guide.md)

### Mermaid to Image Converter
Convert Mermaid diagrams in markdown files to high-quality images using the official Mermaid CLI:

```bash
# Basic usage
uv run python scripts/mermaid_to_image.py <markdown-file-path>

# Custom format and theme
uv run python scripts/mermaid_to_image.py <markdown-file-path> --format svg --theme dark

# Custom dimensions and output directory
uv run python scripts/mermaid_to_image.py <markdown-file-path> --width 2560 --height 1440 --output-dir custom_images

# Check dependencies
uv run python scripts/mermaid_to_image.py --check-deps
```

Features:
- Uses official Mermaid CLI (mmdc) for professional-grade rendering
- Supports PNG, SVG, and PDF output formats
- Intelligent diagram type inference (flowcharts, timelines, sequence, class, etc.)
- Multiple themes: default, dark, forest, neutral, base
- Configurable dimensions, background colors, and output settings
- Organized output structure: `visualizations/parent-folder-name/`
- Sequential naming: `basename-01.png, basename-02.svg, etc.`
- Comprehensive dependency checking and error handling

**Dependencies:**
- Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`
- Python package: `mermaid-mcp` (included in project)

The tool processes markdown files containing ```mermaid code blocks and generates professional-quality images suitable for documentation, presentations, and publications.


### Claude Code SDK Apps
Build AI-powered Streamlit applications using the headless Claude Code SDK:

```bash
# Run chat application
uv run streamlit run apps/chat.py
```

**Agent Package Components:**

The `apps/agent/` package provides reusable capabilities for building Claude Code integrations:

- **ClaudeAgent**: Core client for headless Claude Code interactions
- **AuthManager**: Authentication method detection and configuration
- **SessionManager**: Persistent conversation session management
- **ToolManager**: Tool permission profiles (read_only, code_analysis, code_editing, full_access, etc.)
- **MCPServer**: Model Context Protocol server connections
- **SubAgentManager**: Specialized subagent delegation

**Example Usage:**
```python
from apps.agent import ClaudeAgent, AgentConfig, AuthManager, ToolManager

# Configure agent with authentication
auth_manager = AuthManager()
config = AgentConfig(
    system_prompt="You are a code review assistant",
    permission_mode=PermissionMode.DEFAULT
)

# Apply tool profile
tools = ToolManager()
tools.apply_profile("code_analysis")

# Execute query with automatic auth detection
agent = ClaudeAgent(config, auth_manager=auth_manager)
response = await agent.query_sync("Review this function")

# Check authentication status
auth_status = auth_manager.detect_auth_method()
print(f"Using {auth_status.method.value}: {'✅' if auth_status.is_authenticated else '❌'}")
```

**Built-in Subagents:**
- `code_reviewer`: Code quality and security review
- `debugger`: Error analysis and debugging
- `test_writer`: Test creation and coverage
- `documentation_writer`: Technical documentation
- `performance_optimizer`: Performance improvements
- `security_auditor`: Security vulnerability detection

**Authentication Options:**
Claude Code supports three authentication methods (automatically detected):

1. **Anthropic API**: Set `ANTHROPIC_API_KEY` environment variable
2. **Amazon Bedrock**: Configure AWS credentials + `CLAUDE_CODE_USE_BEDROCK=1`
3. **Claude Account**: Run `claude login` with Pro/Max subscription

The Streamlit app displays current authentication status in the sidebar with configuration instructions.

**Requirements:**
- Install Claude Code SDK: `npm install -g @anthropic-ai/claude-code`
- Python claude-code-sdk package (included in dependencies)
- Streamlit for web interface

For complete documentation and examples, see [apps/README.md](apps/README.md)


