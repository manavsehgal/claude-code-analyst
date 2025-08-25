#!/usr/bin/env python3

import argparse
import os
import re
import sys
import yaml
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any


def load_config(config_path: str = "config.yml") -> Dict[str, Any]:
    """Load configuration from YAML file with defaults."""
    default_config = {
        "output_dir": "visualizations",
        "image_format": "png",
        "width": 1920,
        "height": 1080,
        "dpi": 300,
        "background_color": "white",
        "theme": "default",
        "scale": 2,
        "timeout": 30000
    }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            # Merge with defaults
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except FileNotFoundError:
        print(f"Config file {config_path} not found, using defaults")
        return default_config


def extract_mermaid_blocks(markdown_content: str) -> List[str]:
    """Extract mermaid code blocks from markdown content."""
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    return [match.strip() for match in matches]


def infer_diagram_type(mermaid_code: str) -> str:
    """Infer the diagram type from mermaid code."""
    code_lines = [line.strip() for line in mermaid_code.split('\n') if line.strip()]
    
    if not code_lines:
        return "flowchart"
    
    first_line = code_lines[0].lower()
    
    # Check for explicit diagram types
    if first_line.startswith(('graph ', 'flowchart')):
        return "flowchart"
    elif first_line.startswith('sequencediagram'):
        return "sequence"
    elif first_line.startswith('classDiagram'):
        return "class"
    elif first_line.startswith('stateDiagram'):
        return "state"
    elif first_line.startswith('erdiagram'):
        return "er"
    elif first_line.startswith('userjourneydiagram'):
        return "user-journey"
    elif first_line.startswith('gantt'):
        return "gantt"
    elif first_line.startswith('pie'):
        return "pie"
    elif first_line.startswith('gitgraph'):
        return "gitgraph"
    elif first_line.startswith('mindmap'):
        return "mindmap"
    elif first_line.startswith('timeline'):
        return "timeline"
    elif first_line.startswith('c4context'):
        return "c4"
    elif first_line.startswith('journey'):
        return "journey"
    elif 'participant' in mermaid_code.lower() and ('->>' in mermaid_code or '-->' in mermaid_code):
        return "sequence"
    elif 'class ' in mermaid_code.lower() and ('-->' in mermaid_code or '|>' in mermaid_code):
        return "class"
    else:
        # Default to flowchart for unknown types
        return "flowchart"


def render_mermaid_with_mcp(mermaid_code: str, output_path: Path, config: Dict[str, Any]) -> None:
    """Render mermaid diagram using mermaid-mcp."""
    
    # Create temporary file with mermaid content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_file:
        temp_file.write(mermaid_code)
        temp_file_path = temp_file.name
    
    try:
        # Infer diagram type
        diagram_type = infer_diagram_type(mermaid_code)
        
        # Build mermaid-mcp command
        cmd = [
            'mermaid-mcp', 'cli', 'chart',
            diagram_type,
            temp_file_path,
            str(output_path)
        ]
        
        # Add format option
        if config["image_format"]:
            cmd.extend(['--format', config["image_format"]])
        
        # Add theme option
        if config["theme"] and config["theme"] != "default":
            cmd.extend(['--theme', config["theme"]])
        
        # Add background color
        if config["background_color"] and config["background_color"] != "white":
            cmd.extend(['--bgColor', config["background_color"]])
        
        # Add dimensions
        if config["width"]:
            cmd.extend(['--width', str(config["width"])])
        if config["height"]:
            cmd.extend(['--height', str(config["height"])])
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise Exception(f"mermaid-mcp failed with return code {result.returncode}: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise Exception("Mermaid rendering timed out after 30 seconds")
    except Exception as e:
        raise Exception(f"Error rendering diagram: {e}")
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file_path)
        except:
            pass


def create_output_directory(source_path: str, config: Dict[str, Any]) -> Path:
    """Create output directory structure based on source file location."""
    source_file = Path(source_path)
    
    # Get parent directory name for the source file
    parent_dir_name = source_file.parent.name
    
    # Create output directory structure
    output_base = Path(config["output_dir"])
    output_dir = output_base / parent_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def generate_filename(source_path: str, index: int, config: Dict[str, Any]) -> str:
    """Generate filename for the image based on source file and index."""
    source_file = Path(source_path)
    base_name = source_file.stem
    
    # Format: basename-01.png, basename-02.png, etc.
    suffix = f"{index:02d}"
    extension = config["image_format"]
    
    return f"{base_name}-{suffix}.{extension}"


def process_markdown_file(source_path: str, config: Dict[str, Any]) -> List[Path]:
    """Process markdown file and generate images for all mermaid blocks."""
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise Exception(f"Source file not found: {source_path}")
    except Exception as e:
        raise Exception(f"Error reading source file: {e}")
    
    # Extract mermaid blocks
    mermaid_blocks = extract_mermaid_blocks(content)
    
    if not mermaid_blocks:
        print(f"No mermaid blocks found in {source_path}")
        return []
    
    print(f"Found {len(mermaid_blocks)} mermaid diagram(s) in {source_path}")
    
    # Create output directory
    output_dir = create_output_directory(source_path, config)
    
    generated_files = []
    
    # Process each mermaid block
    for i, mermaid_code in enumerate(mermaid_blocks, 1):
        try:
            print(f"Generating image {i} of {len(mermaid_blocks)}...")
            
            # Create filename
            filename = generate_filename(source_path, i, config)
            output_path = output_dir / filename
            
            # Generate image
            render_mermaid_with_mcp(mermaid_code, output_path, config)
            generated_files.append(output_path)
            
            print(f"✓ Generated: {output_path}")
            
        except Exception as e:
            print(f"✗ Error generating image {i}: {e}")
            continue
    
    return generated_files


def check_dependencies():
    """Check if required dependencies are available."""
    try:
        # Check if mmdc is available
        result = subprocess.run(['mmdc', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("mmdc command failed")
    except FileNotFoundError:
        raise Exception(
            "Mermaid CLI (mmdc) not found. Install it with:\n"
            "npm install -g @mermaid-js/mermaid-cli"
        )
    except Exception as e:
        raise Exception(f"Error checking mmdc: {e}")
    
    try:
        # Check if mermaid-mcp is available
        result = subprocess.run(['mermaid-mcp', '--help'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("mermaid-mcp command failed")
    except FileNotFoundError:
        raise Exception(
            "mermaid-mcp not found. Install it with:\n"
            "pip install mermaid-mcp"
        )
    except Exception as e:
        raise Exception(f"Error checking mermaid-mcp: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Mermaid diagrams in markdown files to high-quality images using official Mermaid CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mermaid_to_image.py diagram.md
  python mermaid_to_image.py diagram.md --config custom_config.yml
  python mermaid_to_image.py diagram.md --format svg --theme dark
  
Dependencies:
  - Mermaid CLI: npm install -g @mermaid-js/mermaid-cli
  - mermaid-mcp: pip install mermaid-mcp (already included in this project)
        """
    )
    
    parser.add_argument('source', nargs='?', help='Path to markdown file containing mermaid diagrams')
    parser.add_argument('--config', default='config.yml', help='Path to config file (default: config.yml)')
    parser.add_argument('--format', choices=['png', 'svg', 'pdf'], help='Output image format')
    parser.add_argument('--output-dir', help='Output directory for images')
    parser.add_argument('--width', type=int, help='Image width')
    parser.add_argument('--height', type=int, help='Image height')
    parser.add_argument('--theme', choices=['default', 'dark', 'forest', 'neutral', 'base'], 
                       help='Mermaid theme')
    parser.add_argument('--background', help='Background color (e.g., white, transparent, #F0F0F0)')
    parser.add_argument('--check-deps', action='store_true', help='Check if all dependencies are installed')
    
    args = parser.parse_args()
    
    try:
        # Check dependencies if requested
        if args.check_deps:
            print("Checking dependencies...")
            check_dependencies()
            print("✓ All dependencies are available")
            return
        
        # Validate source file is provided
        if not args.source:
            print("Error: Source file is required (unless using --check-deps)")
            sys.exit(1)
        
        # Check dependencies silently
        check_dependencies()
        
        # Load configuration
        config = load_config(args.config)
        
        # Override config with command line arguments
        if args.format:
            config['image_format'] = args.format
        if args.output_dir:
            config['output_dir'] = args.output_dir
        if args.width:
            config['width'] = args.width
        if args.height:
            config['height'] = args.height
        if args.theme:
            config['theme'] = args.theme
        if args.background:
            config['background_color'] = args.background
        
        # Validate source file
        if not os.path.exists(args.source):
            print(f"Error: Source file '{args.source}' not found")
            sys.exit(1)
        
        if not args.source.endswith('.md'):
            print(f"Warning: Source file '{args.source}' does not have .md extension")
        
        # Process the file
        print(f"Processing: {args.source}")
        print(f"Output directory: {config['output_dir']}")
        print(f"Format: {config['image_format']} ({config['width']}x{config['height']})")
        print(f"Theme: {config['theme']}, Background: {config['background_color']}")
        print()
        
        generated_files = process_markdown_file(args.source, config)
        
        if generated_files:
            print(f"\n✓ Successfully generated {len(generated_files)} image(s):")
            for file_path in generated_files:
                print(f"  - {file_path}")
        else:
            print("\n✗ No images were generated")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()