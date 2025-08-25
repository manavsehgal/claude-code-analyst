# Article to Markdown Converter - User Guide

## Overview
The `article_to_md.py` script converts web articles into clean, well-formatted Markdown files while preserving images and respecting website policies.

## Features
- Extracts main article content, ignoring navigation, ads, and sidebars
- Downloads and preserves article images locally
- Respects robots.txt policies
- Creates organized folder structure for output
- Validates HTML content before processing
- Generates clean, readable Markdown

## Installation
Ensure dependencies are installed:
```bash
uv sync
```

## Basic Usage
```bash
uv run python scripts/article_to_md.py <URL>
```

### Example
```bash
uv run python scripts/article_to_md.py https://example.com/article
```

## Command-Line Options

### `url` (required)
The URL of the article to convert.

### `--output-dir` (optional)
Base directory for output files. Default: `markdown`
```bash
uv run python scripts/article_to_md.py <URL> --output-dir articles
```

## Output Structure
The script creates an organized folder structure:
```
markdown/
└── article-title-in-kebab-case/
    ├── article.md        # Converted markdown content
    └── images/           # Downloaded images
        ├── image1.jpg
        └── image2.png
```

## How It Works

### 1. URL Validation
- Checks robots.txt to ensure scraping is allowed
- Validates the URL is accessible

### 2. Content Extraction
- Uses Readability algorithm to extract main article content
- Automatically identifies and isolates the primary content
- Removes navigation, advertisements, and sidebars

### 3. Image Processing
- Downloads all images from the article
- Saves them to a local `images/` folder
- Updates image references to use relative paths

### 4. Markdown Conversion
- Converts HTML to clean Markdown format
- Preserves formatting like headings, lists, and code blocks
- Maintains proper line spacing and readability

## Examples

### Convert a Blog Post
```bash
uv run python scripts/article_to_md.py https://blog.example.com/my-post
```
Output: `markdown/my-post/article.md`

### Custom Output Directory
```bash
uv run python scripts/article_to_md.py https://news.site.com/article --output-dir saved-articles
```
Output: `saved-articles/article-title/article.md`

## Error Handling

### Common Issues

**robots.txt blocks access:**
```
Error: robots.txt disallows fetching <URL>
```
Solution: The website doesn't allow automated scraping. Try a different source.

**Invalid HTML:**
```
Error: Invalid HTML content
```
Solution: The page may require JavaScript or has malformed HTML.

**Network errors:**
```
Error fetching URL: <error details>
```
Solution: Check your internet connection and verify the URL is correct.

## Best Practices

1. **Respect Website Policies**: The script automatically checks robots.txt, but also respect rate limits and terms of service.

2. **Verify Output**: Always review the converted Markdown to ensure content was extracted correctly.

3. **Large Articles**: For very long articles, the script may take time to download all images. Be patient.

4. **Batch Processing**: To convert multiple articles, create a simple shell script:
```bash
#!/bin/bash
urls=(
    "https://site.com/article1"
    "https://site.com/article2"
)

for url in "${urls[@]}"; do
    uv run python scripts/article_to_md.py "$url"
done
```

## Limitations

- **JavaScript-rendered content**: Articles that require JavaScript to load content may not be extracted properly
- **Paywalled content**: Cannot access content behind paywalls or login requirements
- **Complex layouts**: Some complex article layouts may not convert perfectly
- **Video content**: Videos are not downloaded, only images

## Troubleshooting

### Script Not Found
Ensure you're running from the project root:
```bash
cd /path/to/claude-code-analyst
uv run python scripts/article_to_md.py <URL>
```

### Missing Dependencies
Install all required packages:
```bash
uv sync
```

### Permission Errors
Ensure you have write permissions in the output directory.

## Technical Details

### Dependencies
- `requests`: HTTP requests and web fetching
- `beautifulsoup4`: HTML parsing and manipulation
- `markdownify`: HTML to Markdown conversion
- `readability-lxml`: Article extraction algorithm

### File Naming
- Folder names use kebab-case derived from article title
- Special characters are removed from folder names
- Image files retain original names when possible

## Support
For issues or feature requests, please check the project repository or contact the maintainers.