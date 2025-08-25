# Claude Code Configuration

## Project Overview
This is a Python project for analyzing Claude Code interactions, managed by uv for dependency management and virtual environments.

## Common Commands

### Development Setup
```bash
# Install dependencies
uv sync

# Run main script
uv run python main.py

# Run tests
uv run pytest tests/
```

### Linting and Type Checking
```bash
# Run linters (when configured)
uv run ruff check .
uv run ruff format .

# Type checking (when mypy is added)
uv run mypy .
```

## Core Project Structure
- `scripts/` - Python scripts for analysis tasks
- `tests/` - Test files following pytest conventions
- `docs/` - User documentation and guides
- `backlog/` - Project backlog and task tracking
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
Convert web articles to clean markdown files with metadata and preserved images:

```bash
# Basic usage
uv run python scripts/article_to_md.py <URL>

# With custom output directory
uv run python scripts/article_to_md.py <URL> --output-dir <directory>
```

Features:
- Extracts main article content
- Downloads and preserves images
- Adds metadata (title, date, word count, etc.)
- Creates organized folder structure

For detailed usage, see [Article to Markdown Guide](docs/article-to-md-guide.md)

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