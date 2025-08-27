# EC2 Instance Selection Guide for LLM Workloads

This decision tree provides comprehensive guidance for selecting optimal EC2 instance types based on model size, workload requirements, and cost considerations, helping organizations choose the most suitable infrastructure for their LLM projects.

```mermaid
flowchart TD
    Start[LLM Workload Planning] --> WorkloadType{Workload Type?}
    
    WorkloadType -->|Training| TrainingPath[Training Workloads]
    WorkloadType -->|Inference| InferencePath[Inference Workloads]
    
    TrainingPath --> ModelSize{Model Size?}
    ModelSize -->|Trillion+ Parameters| FrontierTraining[Frontier Model Training]
    ModelSize -->|100B-1T Parameters| LargeTraining[Large Model Training]
    ModelSize -->|10B-100B Parameters| StandardTraining[Standard Training]
    ModelSize -->|1B-10B Parameters| SmallTraining[Small Model Training]
    
    FrontierTraining --> P6Ultra[P6e-GB200 UltraServers<br/>72 Blackwell GPUs<br/>360 petaflops FP8<br/>13.4 TB HBM3e]
    
    LargeTraining --> CostPriority{Cost Priority?}
    CostPriority -->|Performance| P6B200[P6-B200 instances<br/>20x compute vs P5en<br/>1,440 GB GPU memory]
    CostPriority -->|Balanced| Trn2Ultra[Trn2 UltraServers<br/>64 chips, 6 TiB HBM<br/>332 petaflops sparse]
    CostPriority -->|Cost Optimized| Trn2Standard[Trn2 standard<br/>30-40% cost advantage]
    
    StandardTraining --> HyperPodReq{Need HyperPod?}
    HyperPodReq -->|Yes| P5eHyperPod[P5e + HyperPod<br/>140 GB GPU memory<br/>Auto-recovery enabled]
    HyperPodReq -->|No| P5eStandard[P5e instances<br/>1.87x throughput vs P5<br/>40% cost reduction]
    
    SmallTraining --> BudgetFocus{Budget Focus?}
    BudgetFocus -->|Latest Performance| P5en[P5en instances<br/>3,200 Gbps EFAv3<br/>35% latency improvement]
    BudgetFocus -->|Cost Effective| P4d[P4d instances<br/>60% lower training cost<br/>2.5x performance vs P3]
    
    InferencePath --> InferenceType{Inference Type?}
    InferenceType -->|Ultra High Throughput| UltraInference[P6-B200 instances<br/>Blackwell architecture<br/>2.25x GPU TFLOPs]
    InferenceType -->|High Throughput| HighInference[Inf2 instances<br/>4x throughput<br/>3x Llama 405B performance]
    InferenceType -->|Low Latency| LowLatency[P5e instances<br/>Real-time applications<br/>10x lower latency]
    InferenceType -->|MoE Serving| MoEServing[Trn2 standard<br/>Hardware sparsity<br/>16:4 optimization]
    InferenceType -->|CPU-based| CPUInference[C7g Graviton<br/>40% price performance<br/>Small models]
    
    subgraph CostMatrix["Cost-Performance Matrix"]
        direction TB
        Premium[Premium Performance<br/>P6-B200, P5en]
        Balanced[Balanced Choice<br/>P5e, Trn2]
        CostOptimized[Cost Optimized<br/>P4d, C7g]
    end
    
    subgraph Considerations["Key Considerations"]
        Memory[Memory Requirements<br/>13.4TB - 80GB]
        Network[Network Bandwidth<br/>400 GBPS - 3.2 Tbps]
        Efficiency[Power Efficiency<br/>50% better perf/watt]
        Resilience[Auto-Recovery<br/>HyperPod integration]
    end

    style P6Ultra fill:#ff5722
    style P6B200 fill:#ff9800
    style Trn2Ultra fill:#4caf50
    style P5eHyperPod fill:#2196f3
    style InferenceType fill:#9c27b0
```

## Instance Selection Matrix

**Training Workloads:**
- **P6e-GB200 UltraServers**: Frontier AI training with 72 Blackwell GPUs and 360 petaflops
- **P6-B200**: Next-gen large models with 20x compute improvement over P5en
- **Trn2 UltraServers**: Massive scale with 30-40% cost advantage over GPU instances
- **P5e + HyperPod**: Resilient training with 40% faster completion times

**Inference Workloads:**
- **Inf2 instances**: 4x throughput improvement with 50% better performance/watt
- **P6-B200**: Ultra-high throughput for demanding real-time applications
- **Trn2**: Optimized for MoE architectures with hardware sparsity support
- **C7g Graviton**: Cost-effective CPU inference for smaller models

**Performance Metrics:**
- **P6e-GB200**: 13.4 TB HBM3e, 130 TB/s NVLink, 3.2 Tbps EFA
- **P6-B200**: 1,440 GB GPU memory, 20x compute vs P5en
- **Trn2**: 20.8 petaflops, 30-40% cost advantage
- **Inf2**: 4x throughput, 10x lower latency, 50% power efficiency