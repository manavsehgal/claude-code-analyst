# Agent Evaluation Framework

## Context
Evaluating agents is more complex than traditional classification tasks. The transcript provides a practical framework for building effective evaluations.

## Visualization

```mermaid
flowchart TB
    subgraph "Evaluation Principles"
        Effect["Large Effect Size =<br/>Small Sample Needed"]
        Realistic["Use Realistic Tasks<br/>Not arbitrary tests"]
        Manual["Nothing replaces<br/>human evaluation"]
    end
    
    subgraph "Evaluation Methods"
        Answer["Answer Accuracy"]
        ToolUse["Tool Use Accuracy"]
        FinalState["Final State Check"]
        
        Answer -->|"LLM as Judge"| Rubric1["Check against rubric<br/>Robust to variations"]
        ToolUse -->|"Programmatic"| Check1["Did it use web search 5x?<br/>Did it call search_flights?"]
        FinalState -->|"Database/Files"| Check2["Was flight changed?<br/>Was file modified?"]
    end
    
    subgraph "Anti-Patterns"
        Wrong1["❌ Starting with huge eval"]
        Wrong2["❌ Competitive programming<br/>for real coding"]
        Wrong3["❌ Checking exact string match"]
    end
    
    subgraph "Best Practices"
        Right1["✅ Start small, iterate"]
        Right2["✅ Real-world tasks"]
        Right3["✅ LLM judge with rubric"]
    end
    
    Effect --> Answer
    Realistic --> ToolUse
    Manual --> FinalState
    
    Wrong1 -.->|"Avoid"| Right1
    Wrong2 -.->|"Avoid"| Right2
    Wrong3 -.->|"Avoid"| Right3
    
    style Effect fill:#e1f5fe
    style Answer fill:#c8e6c9
    style Wrong1 fill:#ffccbc
    style Right1 fill:#c8e6c9
```

## Key Quote
"Very quickly, you'll notice that it's difficult to really make progress on a prompt if you don't have an eval that tells you meaningfully whether your prompt is getting better."