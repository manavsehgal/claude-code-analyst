# EC2 Instance Selection Decision Tree for LLM Workloads

## Context
This decision tree helps select the optimal EC2 instance type based on specific LLM workload requirements, incorporating the latest GPU and custom silicon options from AWS.

## Visualization

```mermaid
graph TD
    Start[LLM Workload<br/>Requirements] --> UseCase{Primary<br/>Use Case?}
    
    UseCase -->|Training| ModelScale{Model Scale?}
    UseCase -->|Inference| InfType{Inference Type?}
    UseCase -->|Development| Dev[C7i/C7g Instances<br/>Development & Testing]
    
    ModelScale -->|Frontier AI<br/>Trillion+ params| P6e[P6e-GB200 UltraServers<br/>72 Blackwell GPUs<br/>360 petaflops FP8<br/>13.4 TB HBM3e]
    ModelScale -->|Large Scale<br/>100B-1T params| CostPref{Cost vs Performance?}
    ModelScale -->|Standard<br/>10-100B params| Network{Network Requirements?}
    ModelScale -->|Small-Medium<br/>1-10B params| Budget{Budget Priority?}
    
    CostPref -->|Performance First| P6B[P6-B200 Instances<br/>8 Blackwell GPUs<br/>20x compute vs P5en]
    CostPref -->|Cost Optimized| Trn2U[Trn2 UltraServers<br/>64 Trainium2 chips<br/>30-40% cost advantage]
    
    Network -->|Ultra-High<br/>3.2 Tbps| P5en[P5en Instances<br/>H200 GPUs<br/>EFAv3 networking]
    Network -->|Standard| P5e[P5e Instances<br/>H200 GPUs<br/>40% lower cost]
    
    Budget -->|Performance| P5[P5 Instances<br/>H100 GPUs<br/>Proven performance]
    Budget -->|Value| P4d[P4d Instances<br/>A100 GPUs<br/>60% lower cost]
    Budget -->|Maximum Savings| Trn2S[Trn2 Standard<br/>16 Trainium2<br/>Best price-performance]
    
    InfType -->|Real-time<br/><100ms latency| RTScale{Throughput?}
    InfType -->|Batch<br/>High throughput| BatchOpt{Architecture?}
    InfType -->|Edge<br/>Low resource| Edge[C7g Graviton<br/>40% price-performance]
    
    RTScale -->|Ultra-High| P6BInf[P6-B200<br/>Next-gen inference<br/>2.25x TFLOPs]
    RTScale -->|High| P5eInf[P5e<br/>Real-time AI<br/>10x lower latency]
    RTScale -->|Standard| Inf2RT[Inf2<br/>Low latency<br/>Inferentia2]
    
    BatchOpt -->|MoE Models| Inf2MoE[Inf2 Instances<br/>Hardware sparsity<br/>3x Llama 405B throughput]
    BatchOpt -->|Standard Models| Inf2Std[Inf2 Standard<br/>4x throughput<br/>50% perf/watt]
    BatchOpt -->|Small Models| C7i[C7i Instances<br/>AMX acceleration<br/>CPU inference]
    
    style Start fill:#f9f
    style P6e fill:#ffd700
    style Trn2U fill:#90ee90
    style Inf2MoE fill:#87ceeb
    style P4d fill:#98fb98
```

## Key Insights
- Frontier models (trillion+ parameters) require P6e-GB200 with 72 GPUs
- Cost-optimized training achieves 30-40% savings with Trainium2
- Inference optimization through Inferentia2 delivers 4x throughput improvement
- Instance selection directly impacts total cost of ownership by 40-90%