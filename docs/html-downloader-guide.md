# HTML Page Downloader - User Guide

The HTML Page Downloader is a comprehensive tool for creating clean, self-contained HTML archives of web pages with preserved images and metadata. Perfect for research, documentation, and offline reading.

## 🚀 Quick Start

### Basic Usage
```bash
# Download a web page
uv run python scripts/html_downloader.py https://example.com/article

# Custom output directory
uv run python scripts/html_downloader.py https://example.com/article --output-dir my-archives

# Skip robots.txt check (use responsibly)
uv run python scripts/html_downloader.py https://example.com/article --skip-robots
```

### Output Structure
```
html/
└── kebab-case-article-title/
    ├── index.html          # Clean, self-contained HTML document
    └── images/             # All downloaded images
        ├── image1.png
        ├── image2.webp
        └── diagram.svg
```

## ✨ Key Features

### 🎯 Smart Content Extraction
- Uses advanced readability algorithms to identify main article content
- Automatically removes navigation, sidebars, ads, and other clutter
- Handles complex website layouts and modern frameworks
- Falls back to manual content detection for edge cases

### 📊 Comprehensive Metadata Preservation
- **Basic metadata**: Title, description, keywords, author
- **OpenGraph tags**: Social media preview information
- **Twitter Card data**: Twitter-specific metadata
- **Publication details**: Dates, source attribution
- **Archive information**: When and how the page was captured

### 🖼️ Intelligent Image Handling
- Detects all image types: PNG, JPG, SVG, WebP, GIF
- Handles Next.js optimized images and modern frameworks
- Downloads with proper HTTP headers to bypass basic protection
- Updates all image references to local files
- Preserves image quality and formats

### 🎨 Professional HTML Output
- Clean, well-formed HTML5 documents
- Embedded responsive CSS styling
- Optimized for reading and printing
- Source attribution and archive metadata
- Mobile-friendly design

## 📖 Detailed Usage

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `url` | **Required.** URL of the web page to download | `https://example.com/article` |
| `--output-dir` | Base output directory (default: `html`) | `--output-dir archives` |
| `--skip-robots` | Skip robots.txt compliance check | `--skip-robots` |

### Examples

#### Download Blog Article
```bash
uv run python scripts/html_downloader.py https://blog.example.com/best-practices-2024
```

#### Archive Documentation
```bash
uv run python scripts/html_downloader.py https://docs.example.com/api-reference --output-dir documentation
```

#### Research Paper (Skip Robots)
```bash
uv run python scripts/html_downloader.py https://academic-site.edu/paper.html --skip-robots
```

## 🛠️ Advanced Features

### Metadata Extraction
The tool extracts and preserves comprehensive metadata:

```html
<!-- Source metadata -->
<meta name="source-url" content="https://original-url.com">
<meta name="source-domain" content="example.com">
<meta name="date-scraped" content="2024-01-15 14:30:22">
<meta name="article-date" content="2024-01-10">

<!-- OpenGraph metadata -->
<meta property="og:title" content="Article Title">
<meta property="og:description" content="Article description">
<meta property="og:image" content="https://example.com/image.png">

<!-- Twitter Card metadata -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Article Title">
```

### Content Processing
1. **Primary extraction**: Uses Mozilla's Readability algorithm
2. **Fallback detection**: Searches for common content selectors:
   - `<main>`, `<article>`, `[role="main"]`
   - `.article-content`, `.post-content`, `.entry-content`
   - `#content`, `.main-content`, `.article-body`
3. **Content cleaning**: Removes scripts, styles, navigation, ads
4. **Quality validation**: Ensures meaningful content length

### Image Processing Pipeline
1. **Discovery**: Finds images in content, including:
   - Standard `<img>` tags with `src` attributes
   - Responsive images with `srcset` attributes
   - Next.js optimized images (`/_next/image?url=...`)
   - CSS background images in `style` attributes
2. **Download**: Uses proper HTTP headers:
   ```python
   headers = {
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
       'Referer': base_url,
       'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
   }
   ```
3. **Processing**: Handles filename generation, extension detection
4. **Update**: Modifies all image references to local paths

## 🔧 Troubleshooting

### Common Issues

#### "robots.txt disallows fetching"
**Problem**: The website's robots.txt file blocks automated access.
```
Error: robots.txt disallows fetching https://example.com/page
Use --skip-robots to override this check
```

**Solutions**:
1. **Respect the robots.txt**: Don't download if prohibited
2. **Override responsibly**: Use `--skip-robots` only for legitimate research/personal use
3. **Manual verification**: Check the robots.txt file yourself at `https://example.com/robots.txt`

#### "Could not extract meaningful content"
**Problem**: The tool couldn't identify the main content area.

**Solutions**:
1. **Check the URL**: Ensure it points to an actual article/content page
2. **JavaScript-heavy sites**: Some sites require JavaScript; try accessing the page manually first
3. **Login required**: The content might be behind authentication
4. **PDF or other formats**: The tool only works with HTML pages

#### Image Download Failures
**Problem**: Some images fail to download with 403/404 errors.

**Solutions**:
1. **Expected behavior**: Some images are protected and can't be downloaded
2. **Referrer headers**: The tool uses proper referrer headers, but some sites still block
3. **Broken links**: Original page might have broken image links
4. **CDN issues**: Content delivery networks might have temporary issues

#### Network Timeouts
**Problem**: Downloads fail with timeout errors.

**Solutions**:
1. **Check connection**: Verify your internet connection
2. **Try later**: The target server might be temporarily overloaded
3. **Large images**: Very large images might timeout; this is normal

### Output Quality Issues

#### Missing Styling
**Problem**: The archived page looks different from the original.

**Explanation**: This is intentional! The tool:
- Removes external stylesheets (they require internet)
- Applies clean, readable styling
- Focuses on content over visual design
- Ensures consistent appearance across all archived pages

#### Text Formatting Issues
**Problem**: Some text appears incorrectly formatted.

**Solutions**:
1. **Complex layouts**: Very complex layouts might not convert perfectly
2. **Custom fonts**: Font families are normalized for readability
3. **JavaScript content**: Dynamic content might not be captured

## 📊 Performance Considerations

### File Sizes
- **Typical article**: 50-200KB HTML + 100KB-2MB images
- **Image-heavy pages**: Can reach 10MB+ total size
- **Text-only content**: Usually under 100KB

### Processing Time
- **Simple articles**: 5-15 seconds
- **Image-heavy pages**: 30-60 seconds
- **Large documents**: Up to 2 minutes

### Network Usage
- Downloads original page HTML (~100KB-1MB)
- Downloads all referenced images (varies widely)
- Respects rate limiting with proper delays

## 🎯 Use Cases

### 📚 Research and Documentation
```bash
# Archive academic papers
uv run python scripts/html_downloader.py https://arxiv.org/html/2301.00001 --output-dir research

# Save technical documentation
uv run python scripts/html_downloader.py https://docs.python.org/3/tutorial/ --output-dir documentation
```

### 📰 News and Articles
```bash
# Archive news articles
uv run python scripts/html_downloader.py https://news.example.com/breaking-story --output-dir news-archive

# Save blog posts
uv run python scripts/html_downloader.py https://techblog.example.com/new-framework --output-dir blog-archive
```

### 🏢 Business Intelligence
```bash
# Competitor analysis
uv run python scripts/html_downloader.py https://competitor.com/product-announcement --output-dir competitive-intel

# Market research
uv run python scripts/html_downloader.py https://industry-report.com/trends-2024 --output-dir market-research
```

### 📖 Personal Knowledge Management
```bash
# Build personal library
uv run python scripts/html_downloader.py https://interesting-article.com/deep-dive --output-dir personal-library

# Course materials
uv run python scripts/html_downloader.py https://course.example.edu/lecture-1 --output-dir course-materials
```

## 🔒 Ethical Considerations

### ✅ Appropriate Use
- **Personal research**: Saving articles for offline reading
- **Academic purposes**: Archiving sources for papers
- **Backup creation**: Preserving important content
- **Accessibility**: Making content available offline

### ⚠️ Responsible Usage
- **Respect robots.txt**: Don't override without good reason
- **Rate limiting**: Don't hammer servers with rapid requests
- **Copyright awareness**: Respect intellectual property rights
- **Attribution**: Keep source information intact

### ❌ Inappropriate Use
- **Content theft**: Republishing without permission
- **Commercial scraping**: Large-scale data extraction for profit
- **Server abuse**: Overloading websites with requests
- **Terms violation**: Ignoring website terms of service

## 🔄 Integration with Other Tools

### With Article to Markdown Converter
```bash
# Method 1: HTML archive for clean display
uv run python scripts/html_downloader.py https://example.com/article

# Method 2: Markdown for text processing
uv run python scripts/article_to_md.py https://example.com/article
```

### With Mermaid Visualization Generator
```bash
# 1. Download HTML version for reference
uv run python scripts/html_downloader.py https://technical-article.com/process-guide

# 2. Convert to markdown for visualization
uv run python scripts/article_to_md.py https://technical-article.com/process-guide

# 3. Generate diagrams
/mermaid markdown/process-guide/article.md
```

## 📈 Version History and Updates

### Current Features (v1.0)
- ✅ Smart content extraction
- ✅ Comprehensive metadata preservation
- ✅ Image downloading with proper headers
- ✅ Clean HTML5 output
- ✅ Responsive styling
- ✅ Progress reporting
- ✅ Error handling

### Future Enhancements
- 🔄 PDF export option
- 🔄 Batch processing multiple URLs
- 🔄 Custom CSS themes
- 🔄 Video/audio content handling
- 🔄 Archive format exports (ZIP, etc.)

## 🆘 Getting Help

### Debug Information
When reporting issues, include:
1. **Command used**: Exact command that failed
2. **URL**: The target URL (if shareable)
3. **Error message**: Complete error output
4. **System info**: OS, Python version
5. **Expected vs actual**: What you expected vs what happened

### Common Solutions
1. **Update dependencies**: `uv sync`
2. **Check URL accessibility**: Try opening in browser
3. **Verify network connection**: Ensure internet access
4. **Check disk space**: Ensure sufficient storage
5. **Try different URL**: Test with known-working site

### Contact and Support
- Check existing documentation first
- Review error messages for specific guidance
- Test with simple URLs to isolate issues
- Provide detailed information when seeking help

---

## 🎉 Happy Archiving!

The HTML Page Downloader makes it easy to preserve web content in a clean, professional format. Whether you're a researcher, student, journalist, or knowledge worker, this tool helps you build a reliable offline library of important web content.

**Quick Start Reminder:**
```bash
uv run python scripts/html_downloader.py https://your-target-url.com
```