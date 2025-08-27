# Tool Design Principles for Agents

## Context
Good tool design is critical for agent success. The transcript emphasizes making tools that are clear, distinct, and usable by both humans and AI.

## Visualization

```mermaid
graph TD
    subgraph "Good Tool Design"
        Name["Simple, Accurate Name<br/>search_inventory"]
        Desc["Clear Description<br/>Human-readable"]
        Test["Well-tested<br/>Reliable behavior"]
        Distinct["Distinct Purpose<br/>No overlap"]
    end
    
    subgraph "Common Mistakes"
        Bad1["❌ Six similar search tools"]
        Bad2["❌ Ambiguous names"]
        Bad3["❌ Complex schemas"]
        Bad4["❌ Untested tools"]
    end
    
    subgraph "Tool Schema Example"
        direction LR
        Schema["Tool: search_database<br/>Description: Query inventory<br/>Params: {query: string,<br/>filters: object}"]
    end
    
    Name --> Schema
    Desc --> Schema
    Test --> Schema
    Distinct --> Schema
    
    Bad1 -->|"Fix: Combine into one"| Distinct
    Bad2 -->|"Fix: Clear naming"| Name
    Bad3 -->|"Fix: Simplify"| Desc
    Bad4 -->|"Fix: Test first"| Test
    
    subgraph "Testing Approach"
        Human["Would another engineer<br/>understand this function?"]
        Agent["Can the agent use it<br/>without confusion?"]
        Human --> Agent
    end
    
    Schema --> Human
    
    style Name fill:#c8e6c9
    style Bad1 fill:#ffccbc
    style Human fill:#e1f5fe
```

## Key Principle
"Imagine you give a function to another engineer on your team - would they understand this function and be able to use it? Ask the same question about the agent."