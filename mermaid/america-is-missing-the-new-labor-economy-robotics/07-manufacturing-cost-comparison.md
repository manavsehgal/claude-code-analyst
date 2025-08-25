# Manufacturing Cost Comparison: US vs China

## Context
The article reveals that building an identical robot arm (modeled after UR5e) in the US is approximately 2.2x more expensive than in China. This cost structure analysis shows where the disadvantages compound.

```mermaid
graph LR
    subgraph "Cost Structure Comparison"
        subgraph "China Manufacturing"
            CMat[Materials/Components<br/>Base Cost 100]
            CLabor[Labor<br/>Competitive]
            CInfra[Infrastructure<br/>Optimized]
            CIter[Iteration Speed<br/>Hours]
            CScale[Scale Benefits<br/>Massive]
            CTax[Gov Support<br/>$230B subsidies]
            CTotal[Total Cost Index<br/>100]
        end
        
        subgraph "US Manufacturing"
            UMat[Materials/Components<br/>Imported +30%]
            ULabor[Labor<br/>Higher Cost]
            UInfra[Infrastructure<br/>Limited]
            UIter[Iteration Speed<br/>Weeks]
            UScale[Scale Benefits<br/>Minimal]
            UTax[Gov Support<br/>$73B IRA]
            UTotal[Total Cost Index<br/>220]
        end
    end
    
    CMat --> CTotal
    CLabor --> CTotal
    CInfra --> CTotal
    CIter --> CTotal
    CScale --> CTotal
    CTax --> CTotal
    
    UMat --> UTotal
    ULabor --> UTotal
    UInfra --> UTotal
    UIter --> UTotal
    UScale --> UTotal
    UTax --> UTotal
    
    style CTotal fill:#99ff99
    style UTotal fill:#ff9999
```

## Detailed Cost Drivers

```mermaid
pie title "Factors Contributing to 2.2x Cost Differential"
    "Supply Chain Control" : 35
    "Manufacturing Scale" : 25
    "Government Subsidies" : 20
    "Iteration Speed" : 10
    "Labor & Infrastructure" : 10
```

## Real-World Examples
- **Battery Costs:** China $127/kWh vs North America $157/kWh (24% higher)
- **Factory Construction:** US plants cost 46% more per GWh than Chinese counterparts
- **Iteration Speed:** DJI in Shenzhen could get parts in hours; GoPro needed weeks for shipping
- **Result:** GoPro Karma drone failed against DJI despite similar pricing ($999 vs $1,099)