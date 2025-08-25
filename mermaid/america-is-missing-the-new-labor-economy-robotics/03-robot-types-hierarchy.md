# Robot Types and Applications Hierarchy

## Context
The article categorizes robots into industrial and mobile categories, each with distinct characteristics, applications, and trade-offs. This hierarchy shows the progression from rigid industrial robots to flexible humanoids, highlighting the evolution toward general-purpose systems.

```mermaid
graph TD
    Robots[Robotics Systems]
    
    Robots --> Industrial[Industrial Robots]
    Robots --> Mobile[Mobile Robots]
    
    Industrial --> Trad[Traditional Industrial<br/>90% of shipments]
    Industrial --> Cobots[Collaborative Cobots<br/>10% of shipments]
    
    Trad --> TradChar[High Speed<br/>High Precision<br/>High Payload<br/>Isolated Cells<br/>Static Tasks]
    
    Cobots --> CobotChar[Human Safe<br/>Flexible<br/>Programmable<br/>Lower Payload<br/>Force Sensors]
    
    Mobile --> AGV[AGVs<br/>Warehouse Transport]
    Mobile --> MM[Mobile Manipulators<br/>Factory Floor]
    Mobile --> Quad[Quadrupeds<br/>Inspection]
    Mobile --> Human[Humanoids<br/>General Purpose]
    
    AGV --> AGVApp[Amazon Fulfillment<br/>Fixed Paths<br/>Package Transport]
    
    MM --> MMApp[Station-to-Station<br/>Material Handling<br/>Flat Floors Only]
    
    Quad --> QuadApp[Construction Sites<br/>Rough Terrain<br/>Still Prototyping]
    
    Human --> HumanApp[Any Environment<br/>Human Tasks<br/>$16K-$200K<br/>Mass Production 2025]
    
    style Trad fill:#e6f3ff
    style Cobots fill:#ffe6e6
    style Human fill:#ffffe6
    
    TradChar --> Auto[Automotive<br/>Spot Welding]
    TradChar --> Elec[Electronics<br/>Assembly]
    
    CobotChar --> CNC[CNC Support<br/>Quality Check]
    CobotChar --> Pack[Packaging<br/>Sorting]
```

## Key Insights
- Traditional industrial robots still dominate at 90% of shipments but are limited to structured environments
- Cobots represent the bridge between rigid automation and flexible systems, growing at 10% share
- Humanoids promise general-purpose capability but face the challenge of reducing costs from $100-200K to competitive levels (Unitree achieved $16K)