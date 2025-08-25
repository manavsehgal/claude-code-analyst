# Claude Code Analyst

A Python toolkit for analyzing and processing web content, designed to work seamlessly with Claude Code. The project provides utilities for converting web articles to clean, well-formatted Markdown files while preserving images and metadata.

## Features

### 🔧 Article to Markdown Converter
- **Smart Content Extraction**: Uses the Readability algorithm to extract main article content while ignoring navigation, ads, and sidebars
- **Image Preservation**: Downloads and saves article images locally with proper relative path references  
- **Metadata Enrichment**: Automatically extracts and includes article metadata (title, publication date, word count, image count)
- **Respectful Scraping**: Checks and respects robots.txt policies before processing
- **Clean Output**: Generates well-formatted Markdown with YAML frontmatter and organized folder structure

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Python 3.13+ is required.

```bash
# Clone the repository
git clone https://github.com/your-username/claude-code-analyst.git
cd claude-code-analyst

# Install dependencies
uv sync
```

## Quick Start

### Convert a Web Article to Markdown

```bash
# Basic usage
uv run python scripts/article_to_md.py https://example.com/article

# Custom output directory
uv run python scripts/article_to_md.py https://example.com/article --output-dir articles
```

This creates an organized structure:
```
markdown/
└── article-title-in-kebab-case/
    ├── article.md        # Markdown with metadata
    └── images/           # Downloaded images
        ├── image1.jpg
        └── image2.png
```

### Example Output

Each converted article includes rich metadata:

```markdown
---
title: "How to Build Better Software"
source_url: https://example.com/article
article_date: 2024-01-15
date_scraped: 2024-01-20
word_count: 1250
image_count: 3
---

# How to Build Better Software

Article content here with proper formatting...
```

## Project Structure

```
claude-code-analyst/
├── scripts/              # Python analysis tools
│   └── article_to_md.py  # Web article converter
├── docs/                 # User guides and documentation
│   └── article-to-md-guide.md
├── tests/                # Test files (pytest)
├── backlog/              # Project planning and tracking
│   └── active-backlog.md
├── main.py               # Main entry point
├── pyproject.toml        # Project configuration
└── CLAUDE.md             # Claude Code configuration
```

## Documentation

- **[Article to Markdown Guide](docs/article-to-md-guide.md)**: Complete usage guide with examples and troubleshooting
- **[CLAUDE.md](CLAUDE.md)**: Claude Code configuration and development guidelines

## Development

### Setup Development Environment

```bash
# Install dependencies
uv sync

# Run main script
uv run python main.py
```

### Testing

```bash
# Run tests
uv run pytest tests/
```

### Code Quality

```bash
# Linting and formatting
uv run ruff check .
uv run ruff format .

# Type checking (when mypy is configured)
uv run mypy .
```

## Dependencies

- **requests**: HTTP requests and web fetching
- **beautifulsoup4**: HTML parsing and manipulation  
- **markdownify**: HTML to Markdown conversion
- **readability-lxml**: Content extraction algorithm

## Use Cases

- **Content Archiving**: Save web articles in a clean, readable format
- **Research Documentation**: Convert online articles for offline research
- **Blog Migration**: Extract and convert articles from various platforms
- **Content Analysis**: Process web content for further analysis with Claude Code

## Contributing

1. Follow PEP 8 Python style guidelines
2. Use type hints for all function signatures
3. Write tests for new functionality
4. Update documentation for new features
5. Run tests and linting before submitting changes

## License

[Add license information]

## Support

For detailed usage instructions, see the [documentation](docs/). For issues or feature requests, please use the project's issue tracker.