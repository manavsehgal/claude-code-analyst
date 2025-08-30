#!/usr/bin/env python
"""Extract technology-relevant sections from company 10-K SEC filings."""

import argparse
import json
import os
import re
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from readability import Document


class SEC10KExtractor:
    """Extract and process technology-relevant sections from 10-K SEC filings."""
    
    def __init__(self, config_path: str = "config.yml"):
        """Initialize with configuration."""
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config['sec_10k']['api']['user_agent'],
            'Accept-Encoding': 'gzip, deflate'
        })
        self.rate_limit_delay = 1.0 / self.config['sec_10k']['api']['rate_limit']
        self.last_request_time = 0.0
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
    
    def _rate_limit(self) -> None:
        """Enforce SEC API rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_api_request(self, url: str) -> requests.Response:
        """Make rate-limited API request to SEC."""
        self._rate_limit()
        try:
            response = self.session.get(
                url, 
                timeout=self.config['sec_10k']['api']['timeout']
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed for {url}: {e}")
    
    def find_company_cik(self, company_name: str) -> Optional[str]:
        """Find CIK number for a company by name or ticker symbol."""
        print(f"🔍 Looking up CIK for: {company_name}")
        
        # Get company tickers mapping
        tickers_url = "https://www.sec.gov/files/company_tickers.json"
        response = self._make_api_request(tickers_url)
        tickers_data = response.json()
        
        # Search by ticker symbol first (exact match)
        company_upper = company_name.upper().strip()
        for entry in tickers_data.values():
            if entry['ticker'].upper() == company_upper:
                cik = str(entry['cik_str']).zfill(10)
                print(f"✓ Found by ticker: {entry['title']} (CIK: {cik})")
                return cik
        
        # Search by company name (fuzzy match)
        company_lower = company_name.lower().strip()
        for entry in tickers_data.values():
            title_lower = entry['title'].lower()
            if (company_lower in title_lower or 
                title_lower in company_lower or
                any(word in title_lower for word in company_lower.split() if len(word) > 3)):
                cik = str(entry['cik_str']).zfill(10)
                print(f"✓ Found by name: {entry['title']} (CIK: {cik})")
                return cik
        
        print(f"❌ No CIK found for: {company_name}")
        return None
    
    def get_latest_10k_filing(self, cik: str) -> Optional[Tuple[str, str, str]]:
        """Get the latest 10-K filing URL and details for a company."""
        print(f"📋 Fetching filing history for CIK: {cik}")
        
        submissions_url = f"{self.config['sec_10k']['api']['base_url']}/submissions/CIK{cik}.json"
        response = self._make_api_request(submissions_url)
        submissions_data = response.json()
        
        # Look for 10-K filings
        filings = submissions_data.get('filings', {}).get('recent', {})
        forms = filings.get('form', [])
        accession_numbers = filings.get('accessionNumber', [])
        filing_dates = filings.get('filingDate', [])
        primary_documents = filings.get('primaryDocument', [])
        
        for i, form in enumerate(forms):
            if form == '10-K':
                accession_with_dashes = accession_numbers[i]
                accession_no_dashes = accession_with_dashes.replace('-', '')
                filing_date = filing_dates[i]
                primary_doc = primary_documents[i]
                
                # Construct filing URL (directory uses no dashes, but keep original for reference)
                filing_url = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}"
                             f"/{accession_no_dashes}/{primary_doc}")
                
                print(f"✓ Found latest 10-K: {filing_date}")
                return filing_url, filing_date, accession_with_dashes
        
        print("❌ No 10-K filings found")
        return None
    
    def download_filing_html(self, filing_url: str) -> str:
        """Download 10-K filing HTML content."""
        print(f"⬇️  Downloading filing from: {filing_url}")
        
        try:
            # Use different session for SEC document downloads
            doc_session = requests.Session()
            doc_session.headers.update({
                'User-Agent': self.config['sec_10k']['api']['user_agent'],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            })
            
            self._rate_limit()
            response = doc_session.get(filing_url, timeout=60)
            response.raise_for_status()
            
            print(f"✓ Downloaded {len(response.text):,} characters")
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download filing: {e}")
    
    def extract_sections(self, html_content: str) -> Dict[str, Dict]:
        """Extract configured sections from 10-K HTML."""
        print("🔍 Extracting technology-relevant sections...")
        
        # Clean HTML using readability
        doc = Document(html_content)
        clean_html = doc.content()
        soup = BeautifulSoup(clean_html, 'html.parser')
        text = soup.get_text()
        
        sections = {}
        for section_config in self.config['sec_10k']['sections']:
            item = section_config['item']
            title = section_config['title']
            patterns = section_config['patterns']
            description = section_config['description']
            
            print(f"   Searching for Item {item}: {title}")
            section_content = self._extract_section_by_patterns(text, patterns)
            
            if section_content:
                word_count = len(section_content.split())
                min_length = self.config['sec_10k']['filtering']['min_section_length']
                max_length = self.config['sec_10k']['filtering']['max_section_length']
                
                if min_length <= word_count <= max_length:
                    sections[item] = {
                        'title': title,
                        'content': section_content,
                        'word_count': word_count,
                        'description': description
                    }
                    print(f"     ✓ Extracted ({word_count:,} words)")
                else:
                    print(f"     ⚠️  Skipped (length: {word_count:,} words)")
            else:
                print(f"     ❌ Not found")
        
        return sections
    
    def _extract_section_by_patterns(self, text: str, patterns: List[str]) -> Optional[str]:
        """Extract section content using regex patterns."""
        text_lower = text.lower()
        
        for pattern in patterns:
            # Find section start
            start_matches = list(re.finditer(pattern, text_lower, re.IGNORECASE | re.MULTILINE))
            
            if start_matches:
                # Use the match that gives us the cleanest start (typically the second one)
                match_to_use = start_matches[-1] if len(start_matches) > 1 else start_matches[0]
                start_pos = match_to_use.end()
                
                # Find next major section (Item X) to determine end
                # Look for next item, being more flexible with formatting
                next_item_patterns = [
                    r'item\s+\d+[a-z]*\s*\.?\s*\w+',  # "Item 1A. Risk" or "Item 2 Properties"
                    r'part\s+[iv]+.*?item\s+\d+[a-z]*',  # "Part II Item 5"
                    r'\n\s*item\s+\d+[a-z]*[\s\.:]*\w+',  # Line starting with Item
                ]
                
                end_pos = len(text)  # Default to end of document
                
                for next_pattern in next_item_patterns:
                    next_item_matches = list(re.finditer(next_pattern, text_lower[start_pos:], 
                                                       re.IGNORECASE | re.MULTILINE))
                    if next_item_matches:
                        # Find the closest next item that's actually a different item
                        for next_match in next_item_matches:
                            potential_end = start_pos + next_match.start()
                            # Make sure it's far enough from start to be meaningful content
                            if potential_end - start_pos > 500:  # At least 500 characters
                                end_pos = potential_end
                                break
                        if end_pos != len(text):  # Found a good end position
                            break
                
                # If no next section found, take a reasonable chunk (20,000 chars max)
                if end_pos == len(text):
                    end_pos = min(start_pos + 20000, len(text))
                
                section_text = text[start_pos:end_pos].strip()
                
                # Clean up section text - remove excessive whitespace and control characters
                section_text = re.sub(r'\s+', ' ', section_text)
                section_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', section_text)
                
                if len(section_text) > 100:  # Must have substantial content
                    return section_text
        
        return None
    
    def sections_to_markdown(self, sections: Dict[str, Dict], company_name: str, 
                           filing_date: str, filing_url: str) -> str:
        """Convert extracted sections to markdown format."""
        print("📝 Converting sections to markdown...")
        
        # Create metadata
        metadata = {
            'title': f"{company_name} 10-K Technology Analysis",
            'company': company_name,
            'filing_date': filing_date,
            'filing_year': filing_date[:4],
            'source_url': filing_url,
            'extraction_date': datetime.now().strftime('%Y-%m-%d'),
            'sections_extracted': list(sections.keys()),
            'total_word_count': sum(s['word_count'] for s in sections.values()),
            'extracted_by': 'Claude Code Analyst'
        }
        
        # Build markdown content
        lines = ['---']
        for key, value in metadata.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        lines.extend(['---', ''])
        
        # Add title
        lines.append(f"# {metadata['title']}")
        lines.append('')
        
        # Add summary
        lines.extend([
            '## Executive Summary',
            '',
            f'Technology analysis of {company_name} based on their {filing_date[:4]} 10-K SEC filing. ',
            f'This document extracts {len(sections)} key sections containing {metadata["total_word_count"]:,} words ',
            'focused on technology strategy, infrastructure, risks, and business operations.',
            '',
            f'**Filing Date**: {filing_date}  ',
            f'**Source**: [SEC EDGAR Filing]({filing_url})',
            ''
        ])
        
        # Add table of contents
        lines.extend(['## Table of Contents', ''])
        for item, section in sections.items():
            lines.append(f'- [Item {item}: {section["title"]}](#item-{item.lower().replace("a", "a")}-{section["title"].lower().replace(" ", "-").replace("&", "and").replace("'", "")})') 
            
        lines.append('')
        
        # Add sections
        for item, section in sections.items():
            lines.extend([
                f'## Item {item}: {section["title"]}',
                '',
                f'*{section["description"]}*',
                '',
                f'**Word Count**: {section["word_count"]:,}',
                '',
                section['content'],
                '',
                '---',
                ''
            ])
        
        return '\n'.join(lines)
    
    def save_markdown(self, content: str, company_name: str, filing_year: str) -> str:
        """Save markdown content to appropriate directory structure."""
        # Create company directory name (kebab-case)
        company_dir = re.sub(r'[^\w\s-]', '', company_name.lower()).strip()
        company_dir = re.sub(r'[-\s]+', '-', company_dir)
        
        # Create output directory structure
        output_base = Path(self.config['sec_10k']['output_dir'])
        company_path = output_base / company_dir
        company_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        filename = f"10k-{filing_year}.md"
        file_path = company_path / filename
        
        # Save markdown file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Saved to: {file_path}")
        return str(file_path)
    
    def process_company(self, company_name: str) -> Optional[str]:
        """Complete workflow to process a company's latest 10-K filing."""
        try:
            # Step 1: Find CIK
            cik = self.find_company_cik(company_name)
            if not cik:
                return None
            
            # Step 2: Get latest 10-K filing
            filing_info = self.get_latest_10k_filing(cik)
            if not filing_info:
                return None
            
            filing_url, filing_date, accession = filing_info
            
            # Step 3: Download HTML content
            html_content = self.download_filing_html(filing_url)
            
            # Step 4: Extract sections
            sections = self.extract_sections(html_content)
            if not sections:
                print("❌ No relevant sections found")
                return None
            
            # Step 5: Convert to markdown
            markdown_content = self.sections_to_markdown(
                sections, company_name, filing_date, filing_url
            )
            
            # Step 6: Save file
            output_path = self.save_markdown(markdown_content, company_name, filing_date[:4])
            
            print(f"\n✅ Successfully processed {company_name}")
            print(f"📊 Extracted {len(sections)} sections with {sum(s['word_count'] for s in sections.values()):,} words")
            print(f"📄 Output: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error processing {company_name}: {e}")
            return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract technology-relevant sections from company 10-K SEC filings"
    )
    parser.add_argument(
        "company",
        help="Company name or ticker symbol (e.g., 'Apple', 'AAPL', 'Microsoft Corporation')"
    )
    parser.add_argument(
        "--config",
        default="config.yml",
        help="Path to configuration file (default: config.yml)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.config):
        print(f"❌ Configuration file not found: {args.config}")
        return 1
    
    print(f"🚀 Starting 10-K technology analysis for: {args.company}")
    print()
    
    extractor = SEC10KExtractor(args.config)
    result = extractor.process_company(args.company)
    
    if result:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())