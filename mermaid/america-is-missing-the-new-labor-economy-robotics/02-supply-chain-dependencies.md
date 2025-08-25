# Global Robotics Supply Chain Dependencies

## Context
The article reveals alarming dependencies on China for critical robotics components. Even products labeled "Made in USA" rely heavily on Chinese materials and processing. This flowchart maps the complex supply chain showing how raw materials flow through processing to final robot assembly.

```mermaid
flowchart TD
    subgraph "Raw Materials Sources"
        Chile[Chile/Peru<br/>Copper Ore]
        Congo[DRC<br/>80% Cobalt]
        Indo[Indonesia<br/>Nickel]
        Various[Various Countries<br/>Rare Earths]
    end

    subgraph "Processing & Refining"
        ChinaProc[China Processing<br/>93% Rare Earths<br/>90% Magnets<br/>80% Battery Cells]
        style ChinaProc fill:#ff9999
    end

    subgraph "Component Manufacturing"
        Motors[Servo Motors<br/>Japan/Germany/China]
        Gearbox[Gearboxes<br/>60% Nabtesco Japan]
        Batteries[Batteries<br/>80% Chinese]
        Magnets[NdFeB Magnets<br/>90% China]
        Controllers[Controllers/MCUs<br/>Mixed Sources]
    end

    subgraph "Robot Assembly"
        USRobot[US Robot<br/>2.2x China Cost]
        ChinaRobot[China Robot<br/>Base Cost]
        JapanRobot[Japan Robot<br/>Big 4 Players]
        EuroRobot[EU Robot<br/>Declining Share]
    end

    Chile --> ChinaProc
    Congo --> ChinaProc
    Indo --> ChinaProc
    Various --> ChinaProc

    ChinaProc --> Motors
    ChinaProc --> Batteries
    ChinaProc --> Magnets

    Motors --> USRobot
    Motors --> ChinaRobot
    Motors --> JapanRobot
    Motors --> EuroRobot

    Gearbox --> USRobot
    Gearbox --> ChinaRobot
    Gearbox --> JapanRobot
    Gearbox --> EuroRobot

    Batteries --> USRobot
    Batteries --> ChinaRobot

    Magnets --> Motors
    Controllers --> USRobot
    Controllers --> ChinaRobot

    USRobot -.->|"Made in USA"<br/>But China-dependent| Market[Global Market]
    ChinaRobot -->|Lowest Cost<br/>Highest Volume| Market
    JapanRobot -->|Premium Quality<br/>Limited Scale| Market
    EuroRobot -->|KUKA to China<br/>Declining| Market
```

## Key Insights
- China controls critical processing nodes, creating bottlenecks even for "Made in USA" products
- The 2.2x cost differential between US and Chinese robot manufacturing stems from supply chain control
- Western dependency extends beyond final assembly to fundamental materials processing