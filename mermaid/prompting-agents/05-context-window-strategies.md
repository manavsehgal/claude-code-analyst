# Context Window Management Strategies

## Context
With a 200k token context window, agents need strategies to handle long-running tasks effectively. The transcript describes several approaches used in production.

## Visualization

```mermaid
graph LR
    subgraph "Context Window Challenge"
        Start["Agent Task"]
        Window["200k Token Limit"]
        Start --> Window
    end
    
    subgraph "Strategy 1: Compaction"
        Compact["Auto-trigger at 190k"]
        Summary["Dense summary created"]
        NewInstance["New Claude instance"]
        Compact --> Summary
        Summary --> NewInstance
        NewInstance -->|"Continues with summary"| Infinite["∞ Infinite runtime"]
    end
    
    subgraph "Strategy 2: External Memory"
        WriteFile["Write to file"]
        ReadFile["Read when needed"]
        Persist["Persistent storage"]
        WriteFile --> Persist
        Persist --> ReadFile
    end
    
    subgraph "Strategy 3: Sub-Agents"
        Lead["Lead Agent"]
        Sub1["Search Agent 1"]
        Sub2["Search Agent 2"]
        Compress["Compressed results"]
        
        Lead -->|"Delegates"| Sub1
        Lead -->|"Delegates"| Sub2
        Sub1 -->|"Returns"| Compress
        Sub2 -->|"Returns"| Compress
        Compress -->|"Dense form"| Lead
    end
    
    Window -->|"Solution"| Compact
    Window -->|"Solution"| WriteFile
    Window -->|"Solution"| Lead
    
    style Window fill:#ffccbc
    style Infinite fill:#c8e6c9
    style Persist fill:#e1f5fe
    style Lead fill:#fff9c4
```

## Production Example
Claude Code uses compaction to run "infinitely" - automatically summarizing context at ~190k tokens and passing to a fresh instance.