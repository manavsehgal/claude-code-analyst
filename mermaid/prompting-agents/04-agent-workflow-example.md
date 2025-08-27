# Agent Workflow Example: Research Process

## Context
The transcript demonstrates a concrete example of an agent researching "How many bananas can fit in a Rivian R1S?" showing the iterative tool use and thinking process.

## Visualization

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Think as Thinking
    participant Web as Web Search
    participant Calc as Calculator
    
    User->>Agent: "How many bananas fit in Rivian R1S?"
    
    Note over Agent,Think: Planning Phase
    Agent->>Think: Break down request
    Think-->>Agent: Need: vehicle specs, banana dimensions
    
    Note over Agent,Web: Parallel Search Phase
    Agent->>+Web: Search "Rivian R1S cargo capacity"
    Agent->>+Web: Search "average banana dimensions"
    Web-->>-Agent: 1,000L cargo + 623L frunk
    Web-->>-Agent: USDA: 7-8 inches long
    
    Note over Agent,Think: Reflection Phase
    Agent->>Think: Evaluate results quality
    Think-->>Agent: Need unit conversions
    
    Note over Agent,Web: Additional Search
    Agent->>Web: Convert measurements
    Web-->>Agent: Volume conversions
    
    Note over Agent,Calc: Calculation Phase
    Agent->>Calc: Calculate packing efficiency
    Calc-->>Agent: ~48,000 bananas estimate
    
    Agent->>User: Final answer with sources
    
```

## Key Pattern
Notice the interleaved thinking between tool calls - a new capability in Claude 4 models that allows reflection and planning between actions.