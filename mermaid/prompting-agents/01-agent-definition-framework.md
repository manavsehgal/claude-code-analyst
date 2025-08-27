# Agent Definition Framework

## Context
From the transcript, agents at Anthropic are defined as "models using tools in a loop" - a simple yet powerful concept that forms the foundation of their approach.

## Visualization

```mermaid
graph TB
    subgraph "Agent Core Components"
        Task["Task<br/>Complex goal to accomplish"]
        Model["Model<br/>Claude or other LLM"]
        Tools["Tools<br/>Functions/APIs available"]
        Loop["Loop<br/>Continuous iteration"]
    end
    
    subgraph "Environment"
        System["System Prompt<br/>Instructions & guidelines"]
        Context["Context Window<br/>~200k tokens"]
        Responses["Tool Responses<br/>Feedback from actions"]
    end
    
    Task --> Model
    Model -->|"Uses"| Tools
    Tools -->|"Returns"| Responses
    Responses -->|"Updates decisions"| Model
    Model -->|"Continues until complete"| Loop
    Loop -->|"Next iteration"| Model
    
    System -.->|"Guides"| Model
    Context -.->|"Constrains"| Model
    
    style Task fill:#e1f5fe
    style Model fill:#fff9c4
    style Tools fill:#f3e5f5
    style Loop fill:#e8f5e9
```

## Key Insight
The simplicity of this definition - "models using tools in a loop" - belies the complexity of implementation. The agent operates independently, making decisions based on tool responses and continuing until task completion.