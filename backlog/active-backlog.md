# Active Backlog

[x] Scaffold a minimal Python project structure with scripts/ folder where Python scripts will reside, tests/ folder for tests, docs/ folder for user guides. The project is managed by [uv](https://docs.astral.sh/uv/) for Python virtual environment and dependencies management
    **Completed**: Initialized uv project with `pyproject.toml` configured for claude-code-analyst (Python >=3.13). Created required directory structure: scripts/, tests/, docs/. Project now has proper Python project scaffolding with uv managing virtual environment and dependencies.

[x] Read [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) and write a minimal CLAUDE.md file for the project
    **Completed**: Reviewed Claude Code best practices from the official documentation. Created CLAUDE.md file with essential configuration including: common commands (development setup, linting, type checking), project structure overview, code style guidelines following PEP 8, testing instructions using pytest, repository etiquette, and developer environment setup requirements (Python >=3.13, uv package management).

[x] Create an article_to_md Python script to perform following actions: 
1. take a HTML web page url as input and scrapes the main article
2. check this is a valid HTML and respect robots.txt when scraping
3. ignore everything else including navigation, sidebar, footer, ads
4. create a destination folder markdown/kebab-case-title/
5. convert the scraped article as valid markdown which is well-formatted like original source 
6. save the markdown in the destination folder
7. download images within the article, save in images/ folder wihin destination folder
8. embed the relative references to the images within the markdown in same place as in the original source
    **Completed**: Created `scripts/article_to_md.py` script with full functionality for converting web articles to markdown. Implemented using readability-lxml for article extraction, beautifulsoup4 for HTML parsing, markdownify for markdown conversion, and requests for web scraping. The script respects robots.txt, validates HTML, extracts main article content, creates kebab-case directories, downloads images to an images/ subfolder, and properly embeds relative image references in the markdown. Added necessary dependencies to pyproject.toml: requests, beautifulsoup4, markdownify, and readability-lxml. Script tested successfully with example.com.

[x] Update article_to_md script to add metadata to markdown including article date if available, date scraped, article length in words, number of images, source url, article title. Article should have a level 1 heading matching the title.
    **Completed**: Enhanced scripts/article_to_md.py to include comprehensive metadata in YAML frontmatter format. Added extract_article_date() function that checks multiple meta tags (article:published_time, datePublished, etc.) and time tags for publication dates. Implemented word counting functionality with count_words(). Modified process_images() to return image count. Updated main function to collect all metadata (title, source URL, article date if available, scraping date, word count, image count) and format it as YAML frontmatter at the top of the markdown file. Added the article title as a level 1 heading after the metadata. Enhanced console output to display word count and image count statistics. Tested successfully with example.com.

[x] Make the article_to_md script available as a tool use for Claude Code by updating CLAUDE.md crisply and referencing docs/article-to-md-guide.md if required.
    **Completed**: Added "Available Tools" section to CLAUDE.md with comprehensive documentation for the article_to_md script. Updated docs/article-to-md-guide.md to include new metadata features (YAML frontmatter with title, source URL, article date, scrape date, word count, and image count). The tool is now properly documented and available for Claude Code usage with clear usage examples and reference to the detailed guide.