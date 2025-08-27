# SageMaker HyperPod Infrastructure Architecture

This detailed diagram illustrates the comprehensive SageMaker HyperPod infrastructure, showcasing its resilient architecture, auto-healing capabilities, and performance optimization features that enable 40% faster training with zero-downtime recovery.

```mermaid
graph TB
    subgraph HyperPod["SageMaker HyperPod Core"]
        ClusterMgmt[Cluster Management<br/>10-15 min deployment]
        FlexPlan[Flexible Training Plans<br/>Automated capacity]
        TaskGov[Task Governance<br/>>90% utilization]
        
        subgraph Resilience["Resilience Layer"]
            HealthCheck[Deep Health Checks<br/>NVIDIA DCGM]
            AutoReplace[Auto Node Replacement<br/>AWS spare pool]
            AutoResume[Training Auto-Resume<br/>Checkpoint recovery]
        end
    end

    subgraph Hardware["Hardware Infrastructure"]
        subgraph Compute["Compute Resources"]
            P5e[P5e Instances<br/>H200 140GB GPU]
            P6[P6-B200<br/>Blackwell GPUs]
            Trn2[Trainium2<br/>20.8 petaflops]
        end
        
        subgraph Network["Networking"]
            EFA[EFA 400 GBPS<br/>Libfabric bypass]
            GPUDirect[NVIDIA GPUDirect<br/>RDMA between GPUs]
            Spine[Same Spine/AZ<br/>Low latency]
        end
        
        subgraph Storage["Storage"]
            FSx[FSx for Lustre<br/>Sub-ms latency]
            EBS[EBS gp3<br/>Checkpoints]
            S3[S3 Intelligent Tiering<br/>Archive]
        end
    end

    subgraph Orchestration["Orchestration Options"]
        Slurm[Slurm HPC<br/>Traditional scheduling]
        EKS[Amazon EKS<br/>Kubernetes native]
        CLI[HyperPod CLI<br/>Simplified submission]
    end

    subgraph Monitoring["Monitoring & Diagnostics"]
        DCGM[NVIDIA DCGM<br/>GPU diagnostics]
        SMI[NVIDIA SMI<br/>Temperature/Power]
        CPU[CPU Health<br/>100% utilization test]
        NetTest[Network Testing<br/>Inter-node comm]
        
        subgraph Observability["Observability"]
            Grafana[Grafana Dashboards]
            Prometheus[Prometheus Metrics]
            ContainerInsights[Container Insights]
        end
    end

    ClusterMgmt --> Hardware
    FlexPlan --> ClusterMgmt
    TaskGov --> ClusterMgmt
    
    HealthCheck --> DCGM
    HealthCheck --> SMI
    HealthCheck --> CPU
    HealthCheck --> NetTest
    
    AutoReplace --> HealthCheck
    AutoResume --> FSx
    
    P5e --> EFA
    P6 --> EFA
    Trn2 --> EFA
    EFA --> GPUDirect
    GPUDirect --> Spine
    
    FSx --> P5e
    FSx --> P6
    FSx --> Trn2
    
    ClusterMgmt --> Slurm
    ClusterMgmt --> EKS
    CLI --> EKS
    CLI --> Slurm
    
    DCGM --> Grafana
    SMI --> Prometheus
    EKS --> ContainerInsights

    style HyperPod fill:#e3f2fd
    style Resilience fill:#ffebee
    style Network fill:#f3e5f5
    style Observability fill:#e8f5e9
```

## HyperPod Key Features

**Infrastructure Management:**
- **Cluster Creation**: 10-15 minutes for full deployment
- **Heterogeneous Clusters**: Multiple instance groups for training and inference
- **Warm Pools**: Low-latency job startup reducing idle time

**Resilience & Recovery:**
- **Deep Health Checks**: GPU pressure testing before deployment
- **Auto-Recovery**: Automatic restart from last checkpoint after hardware failure
- **Industry Context**: Meta's LLaMA training experienced 1 GPU failure every 3 hours - HyperPod handles automatically

**Performance Optimization:**
- **Resource Utilization**: >90% accelerated compute utilization across projects
- **Dynamic Allocation**: Automated prioritization across inference, training, and fine-tuning
- **Cost Reduction**: Up to 40% through dynamic resource allocation