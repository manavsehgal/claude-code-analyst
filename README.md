# Claude Code Analyst

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-package%20manager-green)](https://docs.astral.sh/uv/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-purple)](https://claude.ai/code)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Transform web content into structured knowledge with AI-powered analysis tools**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

## 📋 Overview

Claude Code Analyst is a comprehensive toolkit for capturing, converting, and visualizing web content with AI-powered analysis capabilities. Built specifically for [Claude Code](https://claude.ai/code) integration, it provides powerful utilities to transform unstructured web content into clean Markdown documents, preserve complete HTML archives, generate insightful Mermaid.js visualizations, and interact with content through an intelligent terminal-based chatbot.

### Why Claude Code Analyst?

- **🌐 Complete Content Capture**: Convert web articles to Markdown OR preserve as clean HTML archives
- **📊 Content Intelligence**: Extract structured data with comprehensive metadata preservation
- **🎨 Visual Understanding**: Automatically generate diagrams from text to reveal hidden patterns and relationships
- **🤖 AI-Powered Chat**: Interactive terminal chatbot for intelligent markdown content analysis
- **⚙️ User Configurable**: Customize AI behavior, system prompts, and chat settings via YAML configuration
- **🚀 Production Quality**: Respects robots.txt, handles edge cases, and produces clean, consistent output

## ✨ Features

### 🔄 Article to Markdown Converter
Transform web articles into clean, portable Markdown files:

- **Smart Extraction**: Uses Mozilla's Readability algorithm to extract main content while filtering out ads, navigation, and clutter
- **Image Preservation**: Downloads and organizes images with proper relative path references
- **Rich Metadata**: Captures title, publication date, word count, and source attribution in YAML frontmatter
- **Dual Input Support**: Works with both web URLs and local HTML files
- **Respectful Scraping**: Checks robots.txt before processing any URL
- **Clean Output**: Generates well-formatted Markdown with preserved text flow

### 🌐 HTML Page Downloader
Create self-contained HTML archives of web pages:

- **Complete Preservation**: Downloads entire web pages as clean, readable HTML documents
- **Smart Content Extraction**: Uses advanced algorithms to identify and extract main content
- **Image Archiving**: Downloads all referenced images with proper HTTP headers to bypass basic protection
- **Enhanced Substack Support**: Properly handles Substack articles with anchor-wrapped images
- **Comprehensive Metadata**: Preserves OpenGraph, Twitter cards, publication dates, and source attribution
- **Professional Styling**: Generates clean HTML5 output with embedded responsive CSS
- **Offline Ready**: Creates fully self-contained archives perfect for offline reading and research

### 📊 Mermaid Visualization Generator
Create intelligent visualizations from Markdown content:

- **Auto-Analysis**: Identifies concepts, workflows, timelines, and relationships from text
- **Multiple Diagram Types**: Generates flowcharts, timelines, mind maps, Sankey diagrams, and more
- **Contextual Output**: Each visualization includes relevant source text and explanations
- **Batch Processing**: Creates comprehensive visualization sets from single documents
- **Claude Code Integration**: Available as a custom `/mermaid` command

### 🖼️ Mermaid to Image Converter
Convert Mermaid diagrams to high-quality images:

- **Professional Quality**: Uses official Mermaid CLI for production-grade rendering
- **Multiple Formats**: Export as PNG, SVG, or PDF with configurable themes and dimensions
- **Batch Processing**: Convert multiple diagrams from a single markdown file
- **Organized Output**: Sequential naming and proper folder structure
- **Theme Support**: Default, dark, forest, neutral, and base themes available
- **Custom Configuration**: Configurable via `config.yml` for dimensions, themes, and output settings

### 🤖 Enhanced Markdown Chat App
Advanced terminal-based AI chatbot for intelligent markdown content analysis:

#### Core Features
- **Smart File Discovery**: Automatically finds and organizes markdown files with folder navigation
- **Rich Terminal UI**: Beautiful, responsive terminal interface with streaming responses and progress indicators
- **Context Management**: Load any markdown file into conversation context with file preview and metadata
- **Advanced Markdown Rendering**: Comprehensive support for tables, headings, lists, blockquotes, code blocks, and more
- **Table Excellence**: Professional table rendering with markdown formatting preserved in cells

#### AI Integration & Configuration
- **Modern Claude Code SDK**: Uses latest SDK with async resource management and proper error handling
- **User-Configurable AI**: Customize Claude's behavior via `config.yml` including:
  - System prompts and AI personality
  - Model selection and performance settings
  - Thinking tokens and conversation limits
  - Permission modes and safety settings
- **Multi-Authentication Support**: Supports three authentication methods:
  - Direct API key (`ANTHROPIC_API_KEY`)
  - Claude Pro/Max plan authentication
  - Amazon Bedrock integration
- **Intelligent Error Handling**: Graceful fallbacks and detailed error messages

#### Navigation & Commands
- **Folder Navigation**: Browse configured project folders with file counts and descriptions
- **File Management**: List, load, show, and refresh commands with rich metadata display
- **Interactive Help**: Comprehensive help system with examples and pro tips
- **Smart Context**: File preview, word counts, structure analysis, and content insights

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Claude Code SDK (for chat features)
- Optional: [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) for image conversion

### Installation

```bash
# Clone the repository
git clone https://github.com/manavsehgal/claude-code-analyst.git
cd claude-code-analyst

# Install dependencies with uv
uv sync

# For chat features, ensure Claude Code SDK is available
uv add claude-code-sdk
```

### Basic Usage

#### 1️⃣ Convert Web Article to Markdown

```bash
# Convert any web article
uv run python scripts/article_to_md.py https://example.com/article

# Convert local HTML file
uv run python scripts/article_to_md.py /path/to/local/file.html

# Specify custom output directory
uv run python scripts/article_to_md.py https://example.com/article --output-dir my-articles
```

**Output Structure:**
```
markdown/
└── article-title-kebab-case/
    ├── article.md        # Clean Markdown with YAML frontmatter
    └── images/           # Preserved images
        ├── image1.jpg
        └── image2.png
```

#### 2️⃣ Download HTML Archive

```bash
# Download complete HTML archive
uv run python scripts/html_downloader.py https://example.com/article

# Custom output directory
uv run python scripts/html_downloader.py https://example.com/article --output-dir archives

# Skip robots.txt check (use responsibly)
uv run python scripts/html_downloader.py https://example.com/article --skip-robots
```

**Output Structure:**
```
html/
└── article-title-kebab-case/
    ├── index.html        # Self-contained HTML document
    └── images/           # All downloaded images
        ├── diagram1.png
        └── chart2.svg
```

#### 3️⃣ Generate Visualizations (Claude Code)

```bash
# In Claude Code, use the custom command
/mermaid markdown/article-title/article.md
```

**Output Structure:**
```
mermaid/
└── article-title/
    ├── 01-timeline.md
    ├── 02-flowchart.md
    ├── 03-relationships.md
    └── README.md
```

#### 4️⃣ Convert Visualizations to Images

```bash
# Convert Mermaid diagrams to high-quality images
uv run python scripts/mermaid_to_image.py mermaid/article-title/01-timeline.md --format png --theme dark

# Batch convert all diagrams in a file
uv run python scripts/mermaid_to_image.py mermaid/article-title/workflow.md --format svg
```

**Output Structure:**
```
visualizations/
└── article-title/
    ├── 01-timeline-01.png
    ├── 02-flowchart-01.svg
    └── 03-relationships-01.pdf
```

#### 5️⃣ Interactive AI Chat with Markdown Content

```bash
# Run the enhanced markdown chat application
uv run python apps/markdown_chat/run.py

# Chat with specific directory content
uv run python apps/markdown_chat/run.py --directory /path/to/markdown/files
```

**Chat Features:**
- 📁 **Smart Navigation**: Browse configured folders (Projects, Transcripts, Markdown)
- 📄 **File Management**: List, load, and analyze any markdown file
- 🤖 **AI Conversations**: Discuss content with Claude using customizable system prompts
- 🎨 **Rich UI**: Beautiful terminal interface with table rendering and streaming responses
- ⚙️ **Configurable**: Customize AI behavior via `apps/markdown_chat/config.yml`

**Sample Configuration (`apps/markdown_chat/config.yml`)**:
```yaml
claude:
  model: "claude-sonnet-4"
  max_thinking_tokens: 5000
  max_turns: 10
  system_prompt: |
    You are a helpful AI assistant specialized in analyzing markdown documents. 
    Provide clear, concise responses about the content with proper formatting.
```

### 🔗 Complete Workflow Examples

#### Research & Analysis Workflow
```bash
# Step 1: Create HTML archive for clean reading
uv run python scripts/html_downloader.py https://research-paper.com/ai-study

# Step 2: Create Markdown for text analysis  
uv run python scripts/article_to_md.py https://research-paper.com/ai-study

# Step 3: Generate visualizations (in Claude Code)
/mermaid markdown/ai-study/article.md

# Step 4: Convert diagrams to presentation-ready images
uv run python scripts/mermaid_to_image.py mermaid/ai-study/01-workflow.md --format png --theme dark

# Step 5: Interactive analysis with AI
uv run python apps/markdown_chat/run.py
# Navigate to the processed content and discuss with AI

# Result: Complete research package with readable archive, processable text, 
# visual insights, presentation-ready images, and AI-powered analysis
```

#### Documentation Preservation
```bash
# For offline documentation that preserves original styling
uv run python scripts/html_downloader.py https://docs.example.com/api-guide --output-dir documentation

# For portable markdown documentation
uv run python scripts/article_to_md.py https://docs.example.com/api-guide --output-dir documentation
```

## 📚 Documentation

| Guide | Description |
|-------|------------|
| [Article Converter Guide](docs/article-to-md-guide.md) | Complete guide for Markdown conversion tool |
| [HTML Downloader Guide](docs/html-downloader-guide.md) | Comprehensive HTML archiving tool documentation |
| [Mermaid Generator Guide](docs/mermaid-visualization-guide.md) | Creating visualizations with Claude Code |
| [CLAUDE.md](CLAUDE.md) | Claude Code configuration and development settings |
| [Documentation Index](docs/README.md) | All available documentation |

## 🎯 Examples

### Enhanced Chat App Experience

```bash
$ uv run python apps/markdown_chat/run.py

╭─────────────── Markdown Chat v3.0 ────────────────╮
│  🤖 Welcome to Enhanced Markdown Chat!             │
│  Status: ✓ Ready for AI chat (Pro/Max)            │
│  Files: 15 markdown files discovered              │
╰────────────────────────────────────────────────────╯

📂 Navigation Root
╭─────┬───────────────┬─────────────────────────┬─────────╮
│   # │ Folder        │ Description             │   Files │
├─────┼───────────────┼─────────────────────────┼─────────┤
│   1 │ 📁 Projects   │ Analysis projects       │ 6 files │
│   2 │ 📁 Transcripts│ Video transcripts       │ 4 files │
│   3 │ 📁 Markdown   │ Converted articles      │ 5 files │
╰─────┴───────────────┴─────────────────────────┴─────────╯

💬 You: 1

📂 Current Folder: Projects
╭─────┬─────────────────────────────────────────┬─────────────╮
│   # │ File                                    │        Size │
├─────┼─────────────────────────────────────────┼─────────────┤
│   1 │ 📄 llm-architectures-aws/report-03.md  │      47.1 KB│
│   2 │ 📄 robotics-analysis/industry-study.md │      32.4 KB│
╰─────┴─────────────────────────────────────────┴─────────────╯

💬 You: load 1

✅ File Loaded: llm-architectures-aws/report-03.md
📊 48,258 characters, 812 lines

💬 You (report-03.md): summarize the key findings

🤖 Claude is analyzing...

📊 Key Findings from LLM Architecture Analysis

| Architecture | Training Efficiency | Inference Speed | Memory Usage |
|--------------|-------------------|-----------------|--------------|
| Transformer  | ⭐⭐⭐           | ⭐⭐            | ⭐⭐⭐       |
| MoE         | ⭐⭐⭐⭐⭐        | ⭐⭐⭐          | ⭐⭐         |
| State Space | ⭐⭐⭐⭐          | ⭐⭐⭐⭐⭐       | ⭐⭐⭐⭐      |

### Main Insights:
• **Mixture of Experts (MoE)** models show 5x training efficiency gains
• **State Space Models** achieve linear scaling with sequence length  
• **Hybrid architectures** balance performance and computational costs

💡 Ask follow-up questions about the content
```

### Article Metadata Output (Markdown)

```yaml
---
title: "Understanding Neural Networks"
source_url: https://example.com/neural-networks
article_date: 2024-12-15
date_scraped: 2024-12-20
word_count: 2847
image_count: 12
---

# Understanding Neural Networks

Article content with preserved formatting and ![relative image links](images/diagram.png)...
```

### HTML Archive Features

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Comprehensive metadata preservation -->
    <meta name="source-url" content="https://original-url.com">
    <meta property="og:title" content="Article Title">
    <meta name="twitter:card" content="summary_large_image">
    
    <!-- Embedded responsive styling -->
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI'... }
        img { max-width: 100%; height: auto; }
    </style>
</head>
<body>
    <!-- Clean, readable content with local image references -->
    <img src="images/local-diagram.png" alt="Diagram">
</body>
</html>
```

### Generated Mermaid Visualization

```mermaid
timeline
    title Evolution of AI Models
    
    2017 : Transformer Architecture
         : Attention Mechanism
    
    2020 : GPT-3 Release
         : 175B Parameters
    
    2023 : ChatGPT Launch
         : Consumer AI Era
```

## 🏗️ Project Structure

```
claude-code-analyst/
├── scripts/                    # Python tools and utilities
│   ├── article_to_md.py       # Web article to Markdown converter
│   ├── html_downloader.py     # HTML page archiving tool
│   └── mermaid_to_image.py    # Mermaid diagram to image converter
├── apps/                       # Interactive applications
│   └── markdown_chat/         # AI-powered markdown chat interface
│       ├── run.py             # Terminal-based chatbot
│       └── config.yml         # User-configurable AI settings
├── docs/                       # User guides and documentation
│   ├── README.md              # Documentation index
│   ├── article-to-md-guide.md
│   ├── html-downloader-guide.md
│   └── mermaid-visualization-guide.md
├── html/                       # HTML archives (generated)
│   └── article-title/
│       ├── index.html
│       └── images/
├── markdown/                   # Converted articles (generated)
│   └── article-title/
│       ├── article.md
│       └── images/
├── mermaid/                   # Visualizations (generated)
│   └── article-title/
│       └── *.md
├── visualizations/            # Generated images (from mermaid_to_image.py)
│   └── article-title/
│       ├── diagram-01.png
│       ├── chart-02.svg
│       └── flow-03.pdf
├── projects/                  # Analysis projects
├── transcripts/              # Video transcripts
├── backlog/                  # Project planning
│   └── active-backlog.md
├── tests/                    # Test suite
├── .claude/                  # Claude Code custom commands
│   └── commands/
│       ├── mermaid.md        # Mermaid visualization generator
│       └── readme.md         # README generation command
├── CLAUDE.md                 # Claude Code configuration
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install all dependencies
uv sync

# Install development dependencies
uv sync --dev

# Run tests
uv run pytest tests/

# Code quality checks
uv run ruff check .
uv run black .
uv run mypy .
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Maintain test coverage
- Respect robots.txt and website terms of service

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | Web fetching and HTTP handling |
| `beautifulsoup4` | HTML parsing and manipulation |
| `markdownify` | HTML to Markdown conversion |
| `readability-lxml` | Article content extraction |
| `mermaid-mcp` | Mermaid diagram processing and image conversion |
| `claude-code-sdk` | AI-powered chat and analysis features |
| `rich` | Enhanced terminal UI and formatting |
| `pyyaml` | Configuration file handling |
| `ruff` | Fast Python linting |
| `black` | Code formatting |
| `mypy` | Static type checking |
| `pytest` | Testing framework |

## 🎯 Use Cases

### 📚 Research & Academia
- **Academic Papers**: Archive research papers as HTML for citation and clean Markdown for analysis
- **Literature Reviews**: Convert multiple sources to consistent formats for comparative analysis
- **Reference Management**: Build structured knowledge bases with metadata preservation
- **AI-Assisted Analysis**: Discuss research findings with Claude through the chat interface

### 📖 Documentation & Knowledge Management
- **Technical Documentation**: Convert API docs to portable Markdown or preserve as styled HTML
- **Team Knowledge Base**: Archive important articles and resources for offline access with AI-powered search
- **Competitive Intelligence**: Analyze competitor content and track changes over time
- **Interactive Exploration**: Navigate and discuss documentation with AI assistance

### 📰 Content Analysis & Journalism
- **News Archiving**: Preserve news articles before they change or disappear
- **Content Migration**: Move content between platforms while maintaining formatting
- **Fact Checking**: Create timestamped archives of web content for verification
- **AI-Powered Insights**: Extract patterns and insights from content using chat interface

### 🏢 Business Intelligence
- **Market Research**: Archive industry reports and analysis with AI-powered summarization
- **Competitive Analysis**: Track competitor announcements and strategy documents
- **Compliance**: Maintain records of regulatory content and policy changes
- **Strategic Planning**: Visualize business processes and strategies from archived content

## 🚦 Roadmap

### Completed Features ✅
- [x] Article to Markdown conversion with metadata (web URLs and local HTML files)
- [x] HTML page archiving with image preservation and enhanced Substack support
- [x] Mermaid visualization generation (Claude Code integration)
- [x] Mermaid to image conversion (PNG, SVG, PDF export)
- [x] Enhanced interactive markdown chat application with AI integration
- [x] Modern Claude Code SDK integration with async resource management
- [x] User-configurable AI behavior via YAML configuration
- [x] Advanced terminal UI with comprehensive markdown rendering
- [x] Rich table rendering with formatting preservation
- [x] Multi-authentication support (API key, Pro/Max plan, Bedrock)
- [x] Smart folder navigation and file management
- [x] Professional error handling and performance optimization
- [x] Comprehensive documentation and user guides

### Planned Enhancements 🔄
- [ ] PDF article processing support
- [ ] Batch processing multiple URLs with progress tracking
- [ ] Custom CSS themes for HTML archives
- [ ] Export to additional formats (JSON, CSV, EPUB)
- [ ] Enhanced metadata extraction (author detection, category classification)
- [ ] API endpoint for programmatic access
- [ ] Video/audio content transcription and processing
- [ ] Archive compression (ZIP/TAR formats)
- [ ] Integration with more visualization formats beyond Mermaid
- [ ] Advanced chat features (conversation history, bookmarks, search)
- [ ] Multi-model support (different AI providers)
- [ ] Collaborative features (shared workspaces, annotations)

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow PEP 8** and add comprehensive type hints
3. **Write tests** for new functionality (aim for >80% coverage)
4. **Update documentation** for any user-facing changes
5. **Respect ethical guidelines** - ensure tools are used responsibly
6. **Test thoroughly** with various website types and edge cases

### Development Workflow

```bash
# 1. Setup development environment
git clone https://github.com/manavsehgal/claude-code-analyst.git
cd claude-code-analyst
uv sync

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes and test
uv run pytest tests/
uv run ruff check .

# 4. Commit and push
git commit -m 'Add amazing feature'
git push origin feature/amazing-feature

# 5. Open Pull Request
```

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Ethical Usage

This toolkit is designed for legitimate research, documentation, and analysis purposes. Please use responsibly:

- **Respect robots.txt** and website terms of service
- **Don't overload servers** - use reasonable delays between requests
- **Respect copyright** - maintain proper attribution and don't republish without permission
- **Be transparent** - the tools identify themselves with appropriate User-Agent strings

## 🙏 Acknowledgments

- [Mozilla Readability](https://github.com/mozilla/readability) for content extraction algorithms
- [Mermaid.js](https://mermaid.js.org/) for beautiful diagram rendering
- [Claude Code](https://claude.ai/code) for AI-powered development capabilities
- [uv](https://docs.astral.sh/uv/) for modern Python package management
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for robust HTML parsing
- [Rich](https://rich.readthedocs.io/) for beautiful terminal interfaces

## 📮 Support

- 📖 **Documentation**: Check the comprehensive [guides](docs/) for detailed instructions
- 🐛 **Bug Reports**: Use the [GitHub issue tracker](https://github.com/manavsehgal/claude-code-analyst/issues)
- 💡 **Feature Requests**: Join discussions in the [community forum](https://github.com/manavsehgal/claude-code-analyst/discussions)
- 🚀 **Claude Code**: Integrated custom commands for seamless workflow

---

<div align="center">

**Built with ❤️ for the Claude Code community**

[⬆ Back to Top](#claude-code-analyst)

</div>