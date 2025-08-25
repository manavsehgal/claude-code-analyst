# Robot Hardware Components and Supply Sources

## Context
The article provides detailed breakdown of robot components, their functions, and global supply concentration. This diagram maps the critical components, their suppliers, and the concerning concentration of supply sources.

```mermaid
mindmap
  root((Robot Components))
    Motion Systems
      Servo Motors
        Yaskawa Japan
        Panasonic Japan
        Bosch Germany
        KUKA China
        7% Rockwell USA
      Gearboxes 14% COGS
        60% Nabtesco Japan
        15% Harmonic Drive Japan
        Leaderdrive China 90% domestic
      Actuators
        Hydraulic
        Pneumatic
        Electric dominant
    Control Systems
      PLCs Factory Level
        Sequencing operations
        Production line control
      MCUs Robot Level
        Real-time tasks
        Sensor reading
        Motor control
      Drives Power Electronics
        MOSFETs/IGBTs
        AC-DC-AC conversion
        Voltage regulation
    Sensors & Vision
      Cameras
        2D Machine Vision
        3D Depth Intel RealSense
        LiDAR Hesai China
        Unitree proprietary
      Joint Encoders
        Position sensing
        Rotation speed
        Angle measurement
      Force/Torque Sensors
        Collision detection
        Pressure sensing
        Safety systems
    End Effectors
      Grippers
        Schunk Germany
        Zimmer Germany
        Festo Germany
      Tools
        Welding
        Cutting
        Assembly
      Hands emerging
        Limited dexterity
        Not widely deployed
    Power & Materials
      Batteries
        80% Chinese cells
        CATL 37% global
        BYD 16% global
        $127/kWh China vs $157+ West
      NdFeB Magnets
        90% China market
        93% China processing
        Jingci/JL MAG/Ningbo
      Rare Earths
        China 93% refining
        5-10 year catch-up
        MP Materials USA trying
```

## Key Insights
- Gearboxes represent the highest COGS at 14%, with Japan's Nabtesco controlling 60% of the market
- China controls critical materials: 90% of permanent magnets, 80% of batteries, 93% of rare earth processing
- US presence is minimal: only 7% in servo motors (Rockwell), attempting to build rare earth capacity