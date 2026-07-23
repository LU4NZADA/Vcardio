# Estrutura Tecnica

```mermaid
graph TB
    APP[app.py] --> SVC[services/]
    SVC --> ANALYSIS[analysis/]
    SVC --> EPID[epidemiology/]
    SVC --> STATS[statistics/]
    SVC --> CHARTS[charts/]
    APP --> DATA[data/]
    DATA --> MODELS[models/]
    APP --> CONFIG[config/]