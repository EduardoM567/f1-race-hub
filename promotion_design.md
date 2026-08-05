# Milestone 3 Promotion Design

## Promotion Workflow

App:
Development App → QA App → Production App

DB:
Development DB → QA DB → Production DB

API:
Development API → QA API → Production API

MQ:
A RabbitMQ VM is required in Development, QA, and Production.

## Promotion Method

SSH will be used to move approved files between environments.

## Guardrails

- Development can promote to QA.
- QA can promote to Production.
- Development cannot promote directly to Production.
- Passwords and secrets are not stored in the inventory file.

## Promotion Workflow

```mermaid
flowchart LR
    subgraph DEV[Development Lane]
        DA[App Dev]
        DD[DB Dev]
        DM[MQ Dev]
        DI[API Dev]
    end

    subgraph QA[QA Lane]
        QA1[App QA]
        QD[DB QA]
        QM[MQ QA]
        QI[API QA]
    end

    subgraph PROD[Production Lane]
        PA[App Production]
        PD[DB Production]
        PM[MQ Production]
        PI[API Production]
    end

    DA --> QA1 --> PA
    DD --> QD --> PD
    DI --> QI --> PI

    DM -. supports .-> DA
    DM -. supports .-> DI
    QM -. supports .-> QA1
    QM -. supports .-> QI
    PM -. supports .-> PA
    PM -. supports .-> PI
```
