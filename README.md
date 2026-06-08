# Course Group Repository

This private repository is for one student group.

## Project structure

This template uses service-based folders. Use branches to isolate parallel work.

```txt
/app
/mq
/db
/api
/docs
```

Recommended branch naming for parallel work: `issue-12-<ucid>-<short-topic>`.

## VM ownership guidance

Teams should assign individual VM ownership responsibilities (for example: `Student A = App_Dev + MQ_QA`).

Recommended approach:

1. Each team member owns at least one VM from each lane when applicable.
2. Recommended: VM ownership should rotate between lanes (for example: `Student A = App_Dev + MQ_QA`).
3. Include an approx uptime schedule
4. Each VM should have user accounts for each team member and allow ssh into them

Track current ownership and history in `docs/vm-ownership.md`.

## Required completion rule

An issue is complete only when:

- it has at least one `type:*` label selected from the GitHub label sidebar
- it is attached to the group project board
- a linked pull request has been approved
- required checks passed
- the pull request merged into `main`
- the issue closed through the merged pull request

See `CONTRIBUTING.md` for the full workflow.
