# Managing Unintended Side Effects in Agent Prompts

## Context
The transcript warns that "agents are more unpredictable than workflows" and most prompt changes will have unintended side effects due to autonomous operation.

## Visualization

```mermaid
flowchart LR
    subgraph "Prompt Intent"
        Intent["Keep searching until<br/>you find the perfect source"]
    end
    
    subgraph "Unintended Consequence"
        Loop["Agent searches forever<br/>if perfect source doesn't exist"]
        Context["Hits context window<br/>Task fails"]
        Loop --> Context
    end
    
    subgraph "Fix Applied"
        Better["If perfect source not found,<br/>stop after few attempts"]
        Fallback["Use best available<br/>with disclaimer"]
        Better --> Fallback
    end
    
    Intent -->|"Causes"| Loop
    Loop -->|"Solution"| Better
    
    subgraph "Other Examples"
    
        Ex1["Be eager and agentic"]
        Side1["Does too much,<br/>unexpected actions"]
        Fix1["Add boundaries<br/>and constraints"]
        
        Ex2["Always verify sources"]
        Side2["Excessive verification<br/>loops"]
        Fix2["Set verification<br/>budget"]
        
        Ex3["Be thorough"]
        Side3["Uses all context<br/>on minor details"]
        Fix3["Prioritize important<br/>information"]
        
        Ex1 -->|"→"| Side1
        Side1 -->|"→"| Fix1
        
        Ex2 -->|"→"| Side2
        Side2 -->|"→"| Fix2
        
        Ex3 -->|"→"| Side3
        Side3 -->|"→"| Fix3
    end
    
    style Intent fill:#fff9c4
    style Loop fill:#ffccbc
    style Better fill:#c8e6c9
    style Side1 fill:#ffe0b2
    style Fix1 fill:#e8f5e9
```

## Key Lesson
Test prompts in realistic scenarios and watch for edge cases. The autonomous nature of agents amplifies any ambiguity in instructions.