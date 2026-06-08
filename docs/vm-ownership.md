# VM Ownership And Rotation

Track individual VM role ownership for each milestone/sprint.

Rotation is recommended, not required.

## Anticipated Uptime Schedule

Document expected VM service availability windows, especially if the VM is not intended to run 24/7.

| VM Or Service | Primary Owner | Uptime Plan | Typical Downtime Window | Recovery/Restart Owner | Notes |
| --- | --- | --- | --- | --- | --- |
| APP VM |  | 24/7 or scheduled |  |  |  |
| DB VM |  | 24/7 or scheduled |  |  |  |
| MQ VM |  | 24/7 or scheduled |  |  |  |
| API VM |  | 24/7 or scheduled |  |  |  |

Use this section for operations planning and communication only. This tracks expected VM uptime, not individual attendance.

## Current Ownership

| Team Member | App Role | MQ Role | DB Role | API Role | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Rotation History

| Milestone Or Sprint | Team Member | Previous Role(s) | New Role(s) | Reason |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

## Role Definitions

- App_Dev: application-layer implementation and integration
- MQ_QA: message-queue verification, queue health checks, and message-flow testing
- DB_Dev: schema, migrations, persistence logic, and data validation
- API_QA: API contract checks, response validation, and integration test support
