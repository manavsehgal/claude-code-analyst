# Mixture-of-Experts (MoE) Architecture Benefits

## Context
This visualization demonstrates the revolutionary impact of MoE architecture on LLM efficiency, showing how sparse activation patterns enable massive models with manageable inference costs.

## Visualization

```mermaid
graph LR
    subgraph "Traditional Dense Model"
        Input1[Input Token] --> Dense[All 671B Parameters<br/>Active]
        Dense --> Output1[Output Token]
        Dense -.->|High Cost| Cost1[100% Parameter Usage<br/>High Memory<br/>High Compute]
    end
    
    subgraph "MoE Sparse Model (DeepSeek-V3)"
        Input2[Input Token] --> Router[Expert Router]
        Router -->|Select 9 of 256| Active[37B Active Parameters<br/>9 Experts × 4.1B each]
        Router -.->|Skip 247| Inactive[634B Inactive Parameters<br/>247 Experts dormant]
        Active --> Output2[Output Token]
        Active -.->|Low Cost| Cost2[5.5% Parameter Usage<br/>85% Cost Reduction<br/>40-60% Memory Savings]
    end
    
    subgraph "Performance Comparison"
        Metric1[Training Throughput<br/>2.8x improvement]
        Metric2[Inference Latency<br/>120ms first token<br/>vs 250ms dense]
        Metric3[Memory Usage<br/>45% HBM utilization<br/>vs 85% dense]
        Metric4[Cost per Token<br/>$0.0052 MoE<br/>vs $0.0125 dense]
    end
    
    style Active fill:#90ee90
    style Inactive fill:#ffcccc,stroke-dasharray: 5 5
    style Cost2 fill:#ffd700
    style Router fill:#87ceeb
```

## Key Insights
- MoE enables 671B parameter models with only 37B active parameters per token
- 85% reduction in inference costs through sparse activation
- Expert routing adds minimal latency while dramatically reducing compute
- AWS Trainium2 provides hardware sparsity support for optimal MoE performance