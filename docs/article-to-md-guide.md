# Article to Markdown Converter - User Guide

## Overview
The `article_to_md.py` script converts web articles or local HTML files into clean, well-formatted Markdown files while preserving images and respecting website policies.

## Features
- Works with both web URLs and local HTML files
- Extracts main article content, ignoring navigation, ads, and sidebars
- Downloads and preserves images (for web sources) or handles local images
- Respects robots.txt policies (for web sources only)
- Creates organized folder structure for output
- Validates HTML content before processing
- Generates clean, readable Markdown with YAML frontmatter metadata
- Extracts article publication date when available
- Tracks word count and image statistics
- Automatically detects input type (URL vs local file path)

## Installation
Ensure dependencies are installed:
```bash
uv sync
```

## Basic Usage

### With Web URL
```bash
uv run python scripts/article_to_md.py <URL>
```

### With Local HTML File
```bash
uv run python scripts/article_to_md.py <path-to-html-file>
```

### Examples
```bash
# Convert web article
uv run python scripts/article_to_md.py https://example.com/article

# Convert local HTML file
uv run python scripts/article_to_md.py /path/to/article.html

# Convert HTML file from html_downloader.py output
uv run python scripts/article_to_md.py html/article-title/index.html
```

## Command-Line Options

### `source` (required)
The source to convert - either a web URL or path to a local HTML file.

### `--output-dir` (optional)
Base directory for output files. Default: `markdown`
```bash
# With web URL
uv run python scripts/article_to_md.py <URL> --output-dir articles

# With local file
uv run python scripts/article_to_md.py <file-path> --output-dir articles
```

## Output Structure
The script creates an organized folder structure:
```
markdown/
└── article-title-in-kebab-case/
    ├── article.md        # Converted markdown with metadata
    └── images/           # Downloaded images
        ├── image1.jpg
        └── image2.png
```

### Metadata Format
Each article includes YAML frontmatter with:
- **title**: Article title
- **source_url**: Original source (URL or file path)
- **article_date**: Publication date (if available)
- **date_scraped**: Date when converted
- **word_count**: Total words in article
- **image_count**: Number of images processed

Example article.md from web source:
```markdown
---
title: "Article Title"
source_url: https://example.com/article
article_date: 2024-01-15
date_scraped: 2024-01-20
word_count: 1250
image_count: 3
---

# Article Title

Article content here...
```

Example article.md from local HTML file:
```markdown
---
title: "Article Title"
source_url: /path/to/article.html
article_date: 2024-01-15
date_scraped: 2024-01-20
word_count: 1250
image_count: 2
---

# Article Title

Article content here...
```

## How It Works

### 1. Input Detection and Validation
- Automatically detects whether input is a URL or local file path
- For URLs: Checks robots.txt to ensure scraping is allowed
- For local files: Validates file exists and is readable
- Validates HTML content before processing

### 2. Content Retrieval
- **Web URLs**: Fetches content via HTTP request with proper headers
- **Local files**: Reads HTML content directly from disk
- Handles both relative and absolute file paths

### 3. Content Extraction
- Uses Readability algorithm to extract main article content
- Automatically identifies and isolates the primary content
- Removes navigation, advertisements, and sidebars

### 4. Image Processing
- **Web sources**: Downloads all images from the article to local `images/` folder
- **Local sources**: Handles existing local images with proper referencing
- Updates image references to use relative paths
- Counts total images processed

### 5. Markdown Conversion
- Converts HTML to clean Markdown format
- Preserves formatting like headings, lists, and code blocks
- Maintains proper line spacing and readability

## Examples

### Convert a Web Article
```bash
uv run python scripts/article_to_md.py https://blog.example.com/my-post
```
Output: `markdown/my-post/article.md`

### Convert Local HTML File
```bash
uv run python scripts/article_to_md.py article.html
```
Output: `markdown/article-title/article.md`

### Convert HTML from html_downloader.py
```bash
# First download with html_downloader.py
uv run python scripts/html_downloader.py https://example.com/article

# Then convert the downloaded HTML to markdown
uv run python scripts/article_to_md.py html/article-title/index.html
```
Output: `markdown/article-title/article.md`

### Custom Output Directory
```bash
# With web URL
uv run python scripts/article_to_md.py https://news.site.com/article --output-dir saved-articles

# With local file
uv run python scripts/article_to_md.py /path/to/article.html --output-dir saved-articles
```
Output: `saved-articles/article-title/article.md`

## Working with Local HTML Files

The script seamlessly handles local HTML files, making it perfect for converting downloaded articles or archived content.

### Use Cases
- Converting HTML files downloaded with `html_downloader.py`
- Processing archived web content
- Converting HTML documents created offline
- Batch processing local HTML collections

### File Path Handling
- **Relative paths**: `article.html`, `docs/article.html`
- **Absolute paths**: `/full/path/to/article.html`
- **Cross-platform compatibility**: Works on Windows, macOS, and Linux

### Image Handling for Local Files
When processing local HTML files:
- Images referenced with relative paths are resolved relative to the HTML file location
- Absolute local paths are preserved where possible
- Web URLs in local files are downloaded (if accessible)
- Local image references are updated to maintain relative paths in output

### Integration with html_downloader.py
Perfect workflow for comprehensive article archiving:
1. Download complete HTML with images: `html_downloader.py <URL>`
2. Convert to markdown: `article_to_md.py html/article-title/index.html`
3. Result: Both HTML archive and clean markdown version

## Error Handling

### Common Issues

**robots.txt blocks access (web URLs only):**
```
Error: robots.txt disallows fetching <URL>
```
Solution: The website doesn't allow automated scraping. Try a different source.

**File not found (local files):**
```
Error: File not found: <file-path>
```
Solution: Check the file path is correct and the file exists.

**Invalid file path (local files):**
```
Error: Path is not a file: <path>
```
Solution: Ensure you're pointing to a file, not a directory.

**Invalid HTML:**
```
Error: Invalid HTML content
```
Solution: The page may require JavaScript, has malformed HTML, or the file is not valid HTML.

**Network errors (web URLs only):**
```
Error: <error details>
```
Solution: Check your internet connection and verify the URL is correct.

## Best Practices

1. **Respect Website Policies**: The script automatically checks robots.txt, but also respect rate limits and terms of service.

2. **Verify Output**: Always review the converted Markdown to ensure content was extracted correctly.

3. **Large Articles**: For very long articles, the script may take time to download all images. Be patient.

4. **Batch Processing**: To convert multiple articles, create a simple shell script:

**For web URLs:**
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

**For local HTML files:**
```bash
#!/bin/bash
for file in html/*/index.html; do
    uv run python scripts/article_to_md.py "$file"
done
```

**For mixed sources:**
```bash
#!/bin/bash
sources=(
    "https://site.com/article1"
    "html/downloaded-article/index.html"
    "/path/to/local/article.html"
)

for source in "${sources[@]}"; do
    uv run python scripts/article_to_md.py "$source"
done
```

## Limitations

**General limitations:**
- **JavaScript-rendered content**: Articles that require JavaScript to load content may not be extracted properly
- **Complex layouts**: Some complex article layouts may not convert perfectly
- **Video content**: Videos are not downloaded, only images

**Web URL specific limitations:**
- **Paywalled content**: Cannot access content behind paywalls or login requirements
- **Rate limiting**: Some sites may block requests if too frequent
- **Dynamic content**: Content loaded via AJAX may not be captured

**Local file specific limitations:**
- **Missing dependencies**: Local HTML files may reference external CSS/JS that affects rendering
- **Relative paths**: Complex relative path structures might not resolve correctly
- **Embedded content**: Local files with embedded iframes or external content may not process completely

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