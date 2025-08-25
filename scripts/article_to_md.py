#!/usr/bin/env python
"""Convert web articles or local HTML files to markdown format with image preservation."""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from readability import Document


def check_robots_txt(url: str) -> bool:
    """Check if the URL is allowed according to robots.txt."""
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    
    try:
        rp.read()
        return rp.can_fetch("*", url)
    except Exception:
        return True


def validate_html(content: str) -> bool:
    """Validate if the content is valid HTML."""
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return bool(soup.find())
    except Exception:
        return False


def extract_article_date(html_content: str) -> Optional[str]:
    """Try to extract publication date from the HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Common meta tags for article dates
    date_meta_names = [
        'article:published_time', 'datePublished', 'publish_date',
        'DC.date.issued', 'date', 'pubdate', 'publication_date'
    ]
    
    for meta_name in date_meta_names:
        # Check property attribute
        meta = soup.find('meta', property=meta_name)
        if not meta:
            # Check name attribute
            meta = soup.find('meta', {'name': meta_name})
        
        if meta and meta.get('content'):
            try:
                # Try to parse the date
                date_str = meta.get('content')
                # Handle ISO 8601 format
                if 'T' in date_str:
                    date_str = date_str.split('T')[0]
                return date_str
            except:
                continue
    
    # Look for time tags with datetime attribute
    time_tag = soup.find('time', datetime=True)
    if time_tag:
        date_str = time_tag.get('datetime')
        if 'T' in date_str:
            date_str = date_str.split('T')[0]
        return date_str
    
    return None


def count_words(text: str) -> int:
    """Count words in the text content."""
    # Remove extra whitespace and count words
    words = text.split()
    return len(words)


def extract_article(html_content: str, url: str) -> Tuple[str, str]:
    """Extract the main article content and title from HTML."""
    doc = Document(html_content, url=url)
    article = doc.summary()
    title = doc.title()
    
    return article, title


def create_kebab_case(text: str) -> str:
    """Convert text to kebab-case format."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def download_image(img_url: str, dest_folder: Path) -> Optional[str]:
    """Download an image and return the local filename."""
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        
        parsed_url = urlparse(img_url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or '.' not in filename:
            filename = f"image_{hash(img_url)}.jpg"
        
        filepath = dest_folder / filename
        filepath.write_bytes(response.content)
        
        return filename
    except Exception as e:
        print(f"Failed to download image {img_url}: {e}", file=sys.stderr)
        return None


def copy_local_image(img_src: str, source_folder: Path, dest_folder: Path) -> Optional[str]:
    """Copy a local image file and return the local filename."""
    try:
        # Handle file:// URLs
        if img_src.startswith('file://'):
            img_path = Path(img_src[7:])  # Remove file:// prefix
        else:
            # Handle relative paths
            img_path = source_folder / img_src
        
        if not img_path.exists():
            print(f"Local image not found: {img_path}", file=sys.stderr)
            return None
        
        filename = img_path.name
        dest_path = dest_folder / filename
        
        # Copy the file
        shutil.copy2(img_path, dest_path)
        
        return filename
    except Exception as e:
        print(f"Failed to copy local image {img_src}: {e}", file=sys.stderr)
        return None


def process_images(soup: BeautifulSoup, base_url: str, images_folder: Path, is_local_source: bool = False, source_folder: Path = None) -> int:
    """Download or copy images and update their references in the HTML. Returns image count."""
    images_folder.mkdir(parents=True, exist_ok=True)
    
    image_count = 0
    for img in soup.find_all('img'):
        img_src = img.get('src')
        if not img_src:
            continue
        
        local_filename = None
        
        if is_local_source:
            # Handle local images
            local_filename = copy_local_image(img_src, source_folder, images_folder)
        else:
            # Handle remote images
            img_url = urljoin(base_url, img_src)
            local_filename = download_image(img_url, images_folder)
        
        if local_filename:
            img['src'] = f"images/{local_filename}"
            image_count += 1
            
            if img.get('srcset'):
                del img['srcset']
    
    return image_count


def convert_to_markdown(html_content: str, base_url: str, dest_folder: Path, is_local_source: bool = False, source_folder: Path = None) -> Tuple[str, int]:
    """Convert HTML to markdown with image processing. Returns markdown and image count."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    images_folder = dest_folder / "images"
    image_count = process_images(soup, base_url, images_folder, is_local_source, source_folder)
    
    processed_html = str(soup)
    
    markdown_content = md(
        processed_html,
        heading_style="ATX",
        bullets="-",
        code_language="python"
    )
    
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    return markdown_content.strip(), image_count


def format_metadata(metadata: Dict[str, any]) -> str:
    """Format metadata as markdown frontmatter."""
    lines = []
    lines.append("---")
    lines.append(f"title: \"{metadata['title']}\"")
    lines.append(f"source_url: {metadata['source_url']}")
    if metadata['article_date']:
        lines.append(f"article_date: {metadata['article_date']}")
    lines.append(f"date_scraped: {metadata['date_scraped']}")
    lines.append(f"word_count: {metadata['word_count']}")
    lines.append(f"image_count: {metadata['image_count']}")
    lines.append("---")
    return "\n".join(lines)


def is_url(source: str) -> bool:
    """Check if the source is a URL or a file path."""
    parsed = urlparse(source)
    return bool(parsed.scheme and parsed.netloc)


def fetch_article(url: str) -> Tuple[str, str]:
    """Fetch the article from the URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; article-to-md/1.0)'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    return response.text, response.url


def read_local_html(file_path: str) -> Tuple[str, Path]:
    """Read HTML content from a local file."""
    path = Path(file_path).resolve()  # Convert to absolute path
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    html_content = path.read_text(encoding='utf-8')
    # Return content and the parent folder for image handling
    return html_content, path.parent


def main():
    """Main function to convert web article or local HTML file to markdown."""
    parser = argparse.ArgumentParser(
        description="Convert web articles or local HTML files to markdown format"
    )
    parser.add_argument(
        "source",
        help="URL of the article to convert or path to local HTML file"
    )
    parser.add_argument(
        "--output-dir",
        default="markdown",
        help="Base output directory (default: markdown)"
    )
    
    args = parser.parse_args()
    
    is_source_url = is_url(args.source)
    
    # Only check robots.txt for URLs
    if is_source_url and not check_robots_txt(args.source):
        print(f"Error: robots.txt disallows fetching {args.source}", file=sys.stderr)
        sys.exit(1)
    
    try:
        if is_source_url:
            print(f"Fetching article from {args.source}...")
            html_content, final_url = fetch_article(args.source)
            source_folder = None
        else:
            print(f"Reading HTML file from {args.source}...")
            html_content, source_folder = read_local_html(args.source)
            final_url = args.source  # Use the file path as the source URL for metadata
        
        if not validate_html(html_content):
            print("Error: Invalid HTML content", file=sys.stderr)
            sys.exit(1)
        
        print("Extracting article content...")
        article_html, title = extract_article(html_content, final_url if is_source_url else "")
        
        if not article_html:
            print("Error: Could not extract article content", file=sys.stderr)
            sys.exit(1)
        
        # Extract article date
        article_date = extract_article_date(html_content)
        
        kebab_title = create_kebab_case(title)
        dest_folder = Path(args.output_dir) / kebab_title
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        if is_source_url:
            print(f"Converting to markdown and downloading images...")
            markdown_content, image_count = convert_to_markdown(article_html, final_url, dest_folder)
        else:
            print(f"Converting to markdown and copying images...")
            markdown_content, image_count = convert_to_markdown(article_html, "", dest_folder, True, source_folder)
        
        # Extract text for word count (strip HTML tags)
        text_soup = BeautifulSoup(article_html, 'html.parser')
        text_content = text_soup.get_text()
        word_count = count_words(text_content)
        
        # Prepare metadata
        metadata = {
            'title': title,
            'source_url': args.source,
            'article_date': article_date,
            'date_scraped': datetime.now().strftime('%Y-%m-%d'),
            'word_count': word_count,
            'image_count': image_count
        }
        
        # Format the final markdown with metadata and title
        metadata_text = format_metadata(metadata)
        final_markdown = f"{metadata_text}\n\n# {title}\n\n{markdown_content}"
        
        markdown_file = dest_folder / "article.md"
        markdown_file.write_text(final_markdown, encoding='utf-8')
        
        print(f"✓ Article saved to {markdown_file}")
        print(f"✓ Title: {title}")
        print(f"✓ Word count: {word_count}")
        print(f"✓ Images: {image_count}")
        print(f"✓ Folder: {dest_folder}")
        
    except (requests.RequestException, FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()