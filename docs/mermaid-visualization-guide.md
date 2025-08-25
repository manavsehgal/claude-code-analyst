# Mermaid Visualization Generator - User Guide

## Overview
The Mermaid Visualization Generator is a Claude Code custom command that automatically creates Mermaid.js diagrams from markdown content. It analyzes your markdown files to identify visualizable concepts and generates appropriate diagrams with contextual explanations.

## Quick Start
```bash
/mermaid <markdown-file-path>
```

### Example
```bash
/mermaid markdown/my-article/article.md
```

## Features
- **Automatic Analysis**: Identifies key concepts, relationships, and data in markdown
- **Multiple Diagram Types**: Creates flowcharts, timelines, mind maps, Sankey diagrams, and more
- **Contextual Output**: Each diagram includes relevant text from the source
- **Organized Structure**: Outputs to `mermaid/kebab-case-title/` folders
- **Comprehensive Coverage**: Generates multiple visualizations per document

## How It Works

### 1. Content Analysis
The command reads your markdown file and identifies:
- Topics and concepts
- Workflows and processes
- User journeys
- Timelines and sequences
- Hierarchies and relationships
- Data and statistics
- Decision flows

### 2. Visualization Selection
Based on content, it selects appropriate Mermaid.js diagram types:
- **Flowcharts**: For processes and workflows
- **Timelines**: For chronological events
- **Mind Maps**: For hierarchical concepts
- **Sankey Diagrams**: For flow relationships
- **Journey Maps**: For user experiences
- **Pie Charts**: For percentage breakdowns
- **Graph Diagrams**: For relationships and dependencies

### 3. Output Generation
Creates organized output structure:
```
mermaid/
└── article-title-kebab-case/
    ├── 01-timeline.md
    ├── 02-flowchart.md
    ├── 03-mindmap.md
    ├── 04-relationships.md
    └── README.md
```

## Output Format

Each generated file contains:
1. **Title**: Descriptive heading for the visualization
2. **Context**: Relevant excerpt from source material
3. **Mermaid Code Block**: The diagram code
4. **Key Insights**: Important takeaways from the visualization

### Example Output
```markdown
# Project Timeline

## Context
The article describes the evolution of the project from 2020 to 2025...

\```mermaid
timeline
    title Project Evolution
    
    2020 : Initial Concept
         : Research Phase
    
    2022 : Prototype Development
         : User Testing
    
    2024 : Production Release
         : Market Expansion
\```

## Key Insights
- Rapid acceleration after 2022
- 4-year development cycle
```

## Use Cases

### Technical Documentation
Convert technical specs into:
- Architecture diagrams
- Data flow charts
- System dependencies
- API workflows

### Project Planning
Transform project documents into:
- Gantt charts
- Task dependencies
- Resource allocation
- Timeline visualizations

### Business Analysis
Create visualizations for:
- Process flows
- Decision trees
- Organizational charts
- Market analysis

### Educational Content
Generate diagrams for:
- Concept maps
- Learning paths
- Topic relationships
- Progress tracking

## Best Practices

### 1. Source Content Quality
- **Well-structured markdown**: Use clear headings and sections
- **Include data**: Tables, lists, and statistics enhance visualizations
- **Clear relationships**: Explicitly state connections and dependencies

### 2. File Organization
- Keep source markdown in organized folders
- Use descriptive file names
- Group related content together

### 3. Review Generated Output
- Check diagram accuracy
- Verify relationships are correct
- Ensure context is relevant
- Validate data representations

## Examples

### Converting an Article
```bash
# First convert article to markdown
uv run python scripts/article_to_md.py https://example.com/article

# Then generate visualizations
/mermaid markdown/article-title/article.md
```

### Processing Multiple Documents
```bash
# Generate visualizations for project documentation
/mermaid docs/project-overview.md
/mermaid docs/technical-spec.md
/mermaid docs/user-guide.md
```

## Output Examples

### Timeline Visualization
From historical data → Creates chronological timeline

### Flowchart
From process description → Creates step-by-step flow diagram

### Mind Map
From hierarchical content → Creates branching concept map

### Sankey Diagram
From flow data → Creates proportional flow visualization

## Rendering Visualizations

### GitHub
- GitHub automatically renders Mermaid code blocks
- View directly in repository

### VS Code
- Install Mermaid preview extension
- Preview diagrams while editing

### Web Tools
- Use [Mermaid Live Editor](https://mermaid.live)
- Copy/paste generated code

### Documentation Sites
- Most modern doc generators support Mermaid
- Works with MkDocs, Docusaurus, etc.

## Tips and Tricks

### 1. Enhance Source Content
Add these elements to improve visualizations:
- Clear section headings
- Numbered lists for sequences
- Tables with data
- Explicit relationships ("leads to", "depends on", "causes")

### 2. Multiple Perspectives
The generator creates various diagram types to show:
- Different viewpoints of the same data
- Complementary visualizations
- Progressive detail levels

### 3. Customization
After generation, you can:
- Edit the Mermaid code directly
- Adjust styling and colors
- Combine multiple diagrams
- Add additional context

## Limitations

### Content Requirements
- Needs structured markdown input
- Works best with clear relationships
- Requires identifiable patterns

### Diagram Complexity
- Very complex relationships may need simplification
- Large datasets might need filtering
- Some concepts may not translate well to diagrams

### Technical Constraints
- Mermaid.js syntax limitations
- Browser rendering limits for large diagrams
- Some diagram types have size restrictions

## Troubleshooting

### No Output Generated
- Verify markdown file exists and is readable
- Check file contains substantial content
- Ensure proper markdown formatting

### Incomplete Visualizations
- Source may lack clear structure
- Content might be too abstract
- Try breaking into smaller sections

### Rendering Issues
- Check Mermaid syntax is valid
- Verify viewer supports Mermaid version
- Try simplifying complex diagrams

## Advanced Usage

### Combining with Article Converter
```bash
# Complete workflow
# 1. Convert article to markdown
uv run python scripts/article_to_md.py https://site.com/article

# 2. Generate visualizations
/mermaid markdown/article-title/article.md

# 3. Review in mermaid/article-title/
```

### Batch Processing
Process multiple related documents:
```bash
# Create comprehensive visualization set
/mermaid docs/overview.md
/mermaid docs/details.md
/mermaid docs/data.md
```

### Integration with Documentation
1. Generate visualizations
2. Copy relevant diagrams to docs
3. Include in project documentation
4. Update as source changes

## Support
For issues or enhancement requests, refer to the project documentation or CLAUDE.md configuration.