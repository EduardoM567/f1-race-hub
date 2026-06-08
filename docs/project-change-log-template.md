# IT490 Project Change Log Template

Use this template near the end of the semester to summarize the final project state. The change log should help the instructor trace what changed, who contributed, how the system evolved, and what evidence supports the final demo.

This is a final synthesis, not a dump of every weekly update. Link the clearest evidence for important project decisions, implementation work, testing, deployment, and limitations.

## Timing For This Document

Complete this change log after all major project features are complete and team communication about implementation and troubleshooting has finished. It may be easier to keep it up to date as you go.

## Communication Collection (Required)

Collect all class-related project communication and include it in a shared folder.

Unrelated private messages, credentials, secrets, and non-course content may be redacted. Do not include passwords, tokens, private keys, or personal content that is not related to the course project.

Include communication from channels such as:

- WhatsApp
- Discord
- Email
- Text messages
- Meeting minutes or voice-chat notes
- GitHub issues, PR discussions, and reviews
- Any other class-related coordination channel

Collection requirements:

1. Capture all meaningful project communication, including planning, decisions, blockers, troubleshooting, and resolution.
2. Preserve clear team-member identity for each message. If usernames are unclear, annotate to real first names.
3. Keep records chronological when possible. Organize by module/week if helpful for searching.
4. Exports are preferred; chronological screenshots are acceptable when export is not available.
5. Store all evidence in one shared Google Drive folder used by the entire group.
6. Ensure folder access is granted to the instructor or required NJIT group before submission.
7. One team member submits the shared folder link on behalf of the group.

If the shared folder is inaccessible, grading may be impacted.

## Communication Collection Index

Use this index to show what was collected and where it is located:

NOTE: If you're correctly using my Discord server, I should be able to provide text-based channel/thread exports for you upon request.

| Source | Date Range | Export Method | Collected By | Location In Shared Folder | Notes |
| --- | --- | --- | --- | --- | --- |
| Discord |  | Export / screenshots |  |  |  |
| WhatsApp |  | Export / screenshots |  |  |  |
| Email |  | Export / screenshots |  |  |  |
| GitHub |  | Native links / exports |  |  |  |
| Voice chat notes |  | Minutes / transcript |  |  |  |
| Other |  |  |  |  |  |

## Shared Folder Submission

- Shared folder URL:
- Access granted to:
- Submitted by:
- Submission date/time:

## Communication Quality Reflection

Briefly summarize communication quality for the term. Address:

- Quantity and consistency of communication
- Quality and professionalism (including code of conduct)
- How communication supported collaboration, issue resolution, and delivery
- Any notable improvements made over the semester

## Submission Links

- Team repository:
- Main branch:
- Final demo branch or tag:
- Final deployment URL:
- Final presentation or recording URL, if required:
- Project board:
- Architecture diagram:
- Main README:
- Server or deployment documentation:

## Final Project Summary

Briefly summarize the final system.

Include:

- What the system does
- Who uses it
- What external API or service data is used
- What team-owned data is stored
- What the final demo should prove

## Final Architecture Snapshot

Summarize the final system architecture at a high level. Include the required course services and any additional services the team used.

| Service | Final Responsibility | Host, URL, Or Location | Best Evidence |
| --- | --- | --- | --- |
| APP | User-facing application and business logic |  |  |
| DB | Team-owned stored data |  |  |
| RabbitMQ | Cross-server communication |  |  |
| API | External API requests and response handling |  |  |
| Other, if used |  |  |  |

Do not include passwords, tokens, private keys, or secret connection strings.

## Change Summary

Summarize the most important changes since the proposal and MVP milestone.

1. [Major change 1]
2. [Major change 2]
3. [Major change 3]

Focus on meaningful system changes, not every small commit. Good entries explain what changed, why it mattered, and where the supporting evidence lives.

## Team Contributions

Each team member should have visible contribution evidence. Use the strongest links for each person rather than listing every commit.

| Team Member | Main Contributions | Related Issues | Related Pull Requests Or Commits | Demo Area |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

Contribution notes should connect work to behavior, not only file names.

## Milestone And Demo History

List the major checkpoints and what was working at each one. If a checkpoint did not apply or was replaced by another course requirement, note that briefly.

| Checkpoint | Required Focus | Working Behavior Demoed | Evidence Link | Follow-Up Needed |
| --- | --- | --- | --- | --- |
| Proposal | Approved project direction |  |  |  |
| Milestone 1 |  |  |  |  |
| Milestone 2 |  |  |  |  |
| Midterm MVP | Minimal viable product |  |  |  |
| Milestone 3 |  |  |  |  |
| Final Demo | Final project behavior |  |  |  |

## GitHub Evidence

List important GitHub artifacts. Choose evidence that helps the instructor verify planning, implementation, review, bug fixing, documentation, and team coordination.

| Type | Link | Why It Matters |
| --- | --- | --- |
| Issue |  |  |
| Pull request |  |  |
| Commit |  |  |
| Review comment |  |  |
| Project board item |  |  |

Do not list every commit. Prefer the most useful issues, pull requests, commits, review comments, project board items, or documentation links.

## Architecture And Service Changes

Document major architecture or service changes. Focus on changes that affected how the system was built, deployed, connected, secured, or demonstrated.

| Change | Reason | Impact | Evidence |
| --- | --- | --- | --- |
|  |  |  |  |

Examples:

- Added or removed a VM or service
- Changed frontend/backend communication
- Changed message queue behavior
- Changed database schema
- Added logging, monitoring, failover, or deployment automation
- Changed API usage or caching strategy

## Data And API Changes

Document changes to external API usage and stored data.

| Change | Reason | Affected Feature | Evidence |
| --- | --- | --- | --- |
|  |  |  |  |

Include:

- External API fields added or removed
- Database tables or fields added or changed
- User-data associations added or changed
- CRUD behavior added, changed, or removed
- Validation, authorization, or ownership changes

## Deployment And Server Evidence

Record deployment and server evidence needed for grading. Include the required services and any environments or supporting services used for the final demo.

| Server, Environment, Or Service | URL Or Host | Purpose | Current Status | Evidence |
| --- | --- | --- | --- | --- |
| APP |  |  |  |  |
| DB |  |  |  |  |
| RabbitMQ |  |  |  |  |
| API |  |  |  |  |
| Deployment environment, if separate |  |  |  |  |
| Logging or monitoring, if used |  |  |  |  |

Do not paste real passwords, private keys, tokens, or secret values.

## Bugs Fixed

List meaningful bugs fixed during the project.

| Bug | Root Cause | Fix | Evidence |
| --- | --- | --- | --- |
|  |  |  |  |

Good bug notes include the symptom, what caused it, and how the team verified the fix.

## Known Limitations

List known limitations honestly.

| Limitation | Impact | Workaround Or Future Fix |
| --- | --- | --- |
|  |  |  |

Limitations are not automatically failures. Undocumented limitations are usually worse than clearly explained ones.

## Final Demo Checklist

Before the final demo, confirm:

- The deployment URL works
- Required APP, DB, RabbitMQ, and API services are running or documented if intentionally unavailable
- The external API behavior can be shown
- User login or user identity behavior works when required
- User-owned data can be demonstrated
- CRUD behavior can be demonstrated
- Logs, diagrams, screenshots, and documentation are available
- Each team member can explain their contribution
- Known limitations are documented

## AI Disclosure

Disclose any meaningful AI help used for the project, change log, code, troubleshooting, documentation, or presentation. Include what AI helped with, what the team changed, and how the result was verified. If no meaningful AI assistance was used, write "No meaningful AI assistance used."
