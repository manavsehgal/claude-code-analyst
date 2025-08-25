#!/usr/bin/env python
"""Convert web articles to markdown format with image preservation."""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple
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


def process_images(soup: BeautifulSoup, base_url: str, images_folder: Path) -> None:
    """Download images and update their references in the HTML."""
    images_folder.mkdir(parents=True, exist_ok=True)
    
    for img in soup.find_all('img'):
        img_src = img.get('src')
        if not img_src:
            continue
        
        img_url = urljoin(base_url, img_src)
        
        local_filename = download_image(img_url, images_folder)
        if local_filename:
            img['src'] = f"images/{local_filename}"
            
            if img.get('srcset'):
                del img['srcset']


def convert_to_markdown(html_content: str, base_url: str, dest_folder: Path) -> str:
    """Convert HTML to markdown with image processing."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    images_folder = dest_folder / "images"
    process_images(soup, base_url, images_folder)
    
    processed_html = str(soup)
    
    markdown_content = md(
        processed_html,
        heading_style="ATX",
        bullets="-",
        code_language="python",
        wrap=True,
        wrap_width=80
    )
    
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    return markdown_content.strip()


def fetch_article(url: str) -> Tuple[str, str]:
    """Fetch the article from the URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; article-to-md/1.0)'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    return response.text, response.url


def main():
    """Main function to convert web article to markdown."""
    parser = argparse.ArgumentParser(
        description="Convert web articles to markdown format"
    )
    parser.add_argument(
        "url",
        help="URL of the article to convert"
    )
    parser.add_argument(
        "--output-dir",
        default="markdown",
        help="Base output directory (default: markdown)"
    )
    
    args = parser.parse_args()
    
    if not check_robots_txt(args.url):
        print(f"Error: robots.txt disallows fetching {args.url}", file=sys.stderr)
        sys.exit(1)
    
    try:
        print(f"Fetching article from {args.url}...")
        html_content, final_url = fetch_article(args.url)
        
        if not validate_html(html_content):
            print("Error: Invalid HTML content", file=sys.stderr)
            sys.exit(1)
        
        print("Extracting article content...")
        article_html, title = extract_article(html_content, final_url)
        
        if not article_html:
            print("Error: Could not extract article content", file=sys.stderr)
            sys.exit(1)
        
        kebab_title = create_kebab_case(title)
        dest_folder = Path(args.output_dir) / kebab_title
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"Converting to markdown and downloading images...")
        markdown_content = convert_to_markdown(article_html, final_url, dest_folder)
        
        markdown_file = dest_folder / "article.md"
        markdown_file.write_text(markdown_content, encoding='utf-8')
        
        print(f"✓ Article saved to {markdown_file}")
        print(f"✓ Title: {title}")
        print(f"✓ Folder: {dest_folder}")
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()