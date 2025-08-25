# Claude Code Analyst - Documentation

## Available Guides

### [Article to Markdown Converter](article-to-md-guide.md)
Convert web articles into clean, well-formatted Markdown files with preserved images and metadata.
- Extract main article content
- Download and preserve images
- Add comprehensive metadata
- Respect robots.txt

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

### Generate Visualizations
```bash
/mermaid <markdown-file-path>
```

### Complete Workflow
```bash
# 1. Convert article to markdown
uv run python scripts/article_to_md.py https://example.com/article

# 2. Generate visualizations from markdown
/mermaid markdown/article-title/article.md
```

## Tool Integration
Both tools work together seamlessly:
1. Use Article to Markdown Converter to capture web content
2. Use Mermaid Visualization Generator to create diagrams from the content
3. Results are organized in separate folders for easy access

## Project Structure
```
claude-code-analyst/
├── scripts/              # Python scripts
│   └── article_to_md.py
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
    └── mermaid-visualization-guide.md
```

## Getting Started
1. Install dependencies: `uv sync`
2. Convert articles using the Python script
3. Generate visualizations using the Claude Code command
4. Review outputs in respective folders

For detailed instructions, see individual guides above.