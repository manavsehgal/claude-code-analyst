# China's Strategic Robotics Dominance Cycle

## Context
The article describes how China has created a self-reinforcing cycle of robotics dominance through strategic investments, manufacturing scale, and rapid iteration. This diagram illustrates the flywheel effect that makes it increasingly difficult for competitors to catch up.

```mermaid
graph TB
    subgraph "Government Strategy"
        MIC[Made in China 2025<br/>40% → 70% localization]
        Subsidies[$230B+ Subsidies<br/>vs US $73B]
        Plan2023[2023 Humanoid Plan<br/>Strategic Engine]
    end
    
    subgraph "Manufacturing Base"
        Scale[Massive Scale<br/>276K units/year<br/>51% global share]
        Lights[Lights-Out Factories<br/>24/7 Autonomous<br/>1 phone/second]
        Supply[Control Supply Chain<br/>90% magnets<br/>80% batteries]
    end
    
    subgraph "Innovation Speed"
        Iteration[Rapid Iteration<br/>Hours vs Weeks<br/>Shenzhen Advantage]
        Cost[Cost Reduction<br/>$16K Humanoid<br/>vs $100-200K]
        Local[Local Champions<br/>Estun, Efort<br/>Siasun, Unitree]
    end
    
    subgraph "Market Capture"
        Oversupply[Oversupply Strategy<br/>Drive Out Competition]
        Quality[Quality Improvement<br/>Match Western<br/>at Lower Cost]
        Export[Global Dominance<br/>DJI: 90% US drones<br/>KUKA acquisition]
    end
    
    MIC --> Scale
    Subsidies --> Scale
    Plan2023 --> Local
    
    Scale --> Iteration
    Supply --> Cost
    Lights --> Scale
    
    Iteration --> Quality
    Cost --> Oversupply
    Local --> Iteration
    
    Quality --> Export
    Oversupply --> Export
    Export --> More[More Revenue]
    
    More --> Scale
    More --> Iteration
    
    style Scale fill:#ff9999
    style Export fill:#99ff99
    style More fill:#ffff99
```

## Key Insights
- China's strategy creates a self-reinforcing cycle where success breeds more success
- The combination of government support ($230B vs US $73B) and manufacturing scale creates insurmountable advantages
- The DJI drone example (90% US market share) shows how this playbook works in robotics-adjacent markets