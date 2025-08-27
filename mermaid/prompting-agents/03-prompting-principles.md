# Core Prompting Principles for Agents

## Context
Jeremy emphasizes that prompting is "conceptual engineering" - not just about text, but about deciding what concepts the model should have and what behaviors it should follow.

## Visualization

```mermaid
mindmap
  root((Agent Prompting<br/>Principles))
    Think Like Your Agent
      Simulate their environment
      Understand tool limitations
      Mental model of process
      "If human can't understand,<br/>AI won't either"
    
    Reasonable Heuristics
      Concept of irreversibility
      When to stop searching
      Budget constraints
      "5 calls for simple,<br/>15 for complex"
      Managing new intern analogy
    
    Tool Selection
      100+ tools possible
      Clear context for each
      Company-specific defaults
      "Slack for company info"
      Distinct tool purposes
    
    Guide Thinking
      Plan search process
      Interleaved thinking
      Reflect on quality
      Verify sources
      Extended thinking usage
    
    Let Claude be Claude
      Start bare bones
      Don't over-prescribe
      Test first, prompt later
      Models are smarter<br/>than predicted
```

## Key Insight
"Prompting is not going away and will get more important, not less important as models get smarter" - because it's about conceptual engineering, not just text formatting.