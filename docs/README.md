# Claude Code Analyst - Documentation

## Available Guides

### [Article to Markdown Converter](article-to-md-guide.md)
Convert web articles into clean, well-formatted Markdown files with preserved images and metadata.
- Extract main article content
- Download and preserve images
- Add comprehensive metadata
- Respect robots.txt

### [HTML Page Downloader](html-downloader-guide.md)
Download complete web pages as clean, self-contained HTML archives with preserved images and metadata.
- Smart content extraction using readability algorithms
- Comprehensive metadata preservation (OpenGraph, Twitter cards, dates, authors)
- Intelligent image downloading with proper HTTP headers
- Clean HTML5 output with responsive styling

### [Mermaid Visualization Generator](mermaid-visualization-guide.md)
Create intuitive Mermaid.js visualizations from markdown content using Claude Code custom commands.
- Analyze markdown for visualizable concepts
- Generate multiple diagram types
- Include contextual explanations
- Organize output systematically

## Quick Reference

### Convert Web Article
```bash
uv run python scripts/article_to_md.py <URL>
```

### Download HTML Archive
```bash
uv run python scripts/html_downloader.py <URL>
```

### Generate Visualizations
```bash
/mermaid <markdown-file-path>
```

### Complete Workflow
```bash
# Option 1: HTML archive for clean display
uv run python scripts/html_downloader.py https://example.com/article

# Option 2: Markdown for text processing + visualizations
uv run python scripts/article_to_md.py https://example.com/article
/mermaid markdown/article-title/article.md
```

## Tool Integration
All three tools work together seamlessly:
1. Use **HTML Page Downloader** for clean, self-contained archives
2. Use **Article to Markdown Converter** for text processing and analysis
3. Use **Mermaid Visualization Generator** to create diagrams from markdown content
4. Results are organized in separate folders for easy access

## Project Structure
```
claude-code-analyst/
├── scripts/              # Python scripts
│   ├── article_to_md.py
│   └── html_downloader.py
├── html/                 # HTML archives
│   └── article-title/
│       ├── index.html
│       └── images/
├── markdown/             # Converted articles
│   └── article-title/
│       ├── article.md
│       └── images/
├── mermaid/             # Generated visualizations
│   └── article-title/
│       ├── 01-diagram.md
│       └── README.md
└── docs/                # User guides
    ├── README.md
    ├── article-to-md-guide.md
    ├── html-downloader-guide.md
    └── mermaid-visualization-guide.md
```

## Getting Started
1. Install dependencies: `uv sync`
2. Choose your conversion method:
   - **HTML archives**: Use `html_downloader.py` for clean, self-contained pages
   - **Markdown files**: Use `article_to_md.py` for text processing
3. Generate visualizations using the Claude Code command: `/mermaid`
4. Review outputs in respective folders (`html/`, `markdown/`, `mermaid/`)

For detailed instructions, see individual guides above.