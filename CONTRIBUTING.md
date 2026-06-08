# Course Repository Workflow

Every completed code change must flow through an issue and a pull request.

## Repository Structure

This repository is structured by service:

1. `/app`
2. `/mq`
3. `/db`
4. `/api`
5. `/docs`

Use branches to isolate parallel work. It is normal for one feature branch to touch multiple service folders when implementing end-to-end behavior.

## VM Ownership And Rotation

Ownership is tracked at the individual VM role level.

Example assignment:

1. Student A: `App_Dev` and `MQ_QA`
2. Student B: `DB_Dev` and `API_QA`

Guidelines:

1. Assign each VM role to an individual owner.
2. Rotation between lanes is recommended to distribute knowledge.
3. Rotation is not required.
4. Keep role ownership updates in `docs/vm-ownership.md`.
5. Include anticipated VM uptime windows (service availability) if systems are not running 24/7.

## What Is Automatically Enforced By GitHub Actions

Pull requests are blocked unless all of the following are true:

1. PR body links an issue with a closing keyword like `Closes #12`.
2. PR has at least one label.
3. PR has at least one assignee.
4. PR requests review from someone who is not assigned to the PR.
5. After review, PR has approval from someone who is not assigned to the PR.
6. Branch name includes a valid UCID.
7. At least one commit message starts with a valid UCID prefix.

Issue closure is automatically rejected (issue reopened) unless all of the following are true:

1. Issue has at least one `type:*` label, such as `type:feature`, `type:bug`, `type:task`, or `type:documentation`.
2. Issue is attached to the configured project board.
3. Issue has at least one assigned user.
4. Issue was closed by a merged PR linked with a closing keyword.

If an issue is closed too early, automation reopens it, applies `status:needs-fix`, and comments with required fixes.

## What Is Recommended But Not Enforced

1. Issue body includes `Claimed by UCID: <ucid>` for extra ownership metadata.
2. UCID ownership comments in source code when they add real context.
3. Keep service changes scoped to the issue and branch intent.
4. Rotate VM role ownership across lanes when practical.

## Manual Setup Required In Each New Repo

These steps are required for project-board enforcement:

1. Go to `Repo Settings > Secrets and variables > Actions`.
2. Confirm variables:
	`COURSE_PROJECT_OWNER=<instructor GitHub username>`
	`COURSE_PROJECT_NUMBER=<project number>`
3. Optional but recommended for project automation, confirm secret:
	`COURSE_PROJECT_TOKEN=<token with project access>`
4. Ensure each student accepted the repo collaborator invitation. Add project-board collaborators manually only if students need direct board editing.

If the repo was created with the setup script, the variables may already be configured automatically. The token is configured only when the instructor passed token flags during setup.

## Student Workflow

1. Create or claim an issue.
2. Assign the issue owner.
3. Add acceptance criteria.
4. Select the matching GitHub `type:*` label from the issue label sidebar.
5. Create a branch that includes your UCID.
6. Make sure at least one commit message starts with your UCID.
7. Open PR with `Closes #issueNumber`.
8. Assign yourself to the PR.
9. Request review from someone who is not assigned to the PR.
10. Merge only after a non-assigned reviewer approves and required checks pass.

## Async Team Collaboration Artifacts

The following project artifacts should be kept in `/docs` for transparent async collaboration:

1. Meeting minutes (`docs/meeting-minutes.md`)
2. Voting log (`docs/voting-log.md`)
3. Decision log (`docs/decision-log.md`)
4. Outcomes log (`docs/outcomes-log.md`)
5. VM ownership map (`docs/vm-ownership.md`)
6. Project proposal (`docs/project-proposal-template.md`)
7. Project change log (`docs/project-change-log-template.md`)

Use these files to track:

1. What was discussed and who attended
2. What options were voted on and final vote results
3. Decisions made and their rationale
4. Outcomes delivered and whether acceptance criteria were met

When opening PRs for significant work, reference the relevant decision or outcome entry.

## UCID Pattern

Use your official NJIT UCID. The configured pattern is intentionally flexible:

```regex
[a-z]{2,4}[0-9]{0,4}
```

Common workflow words such as `fix`, `docs`, and `test` are rejected so generic branch names and commit messages do not accidentally satisfy the UCID checks.

Examples:

```txt
mt85
abcd
abc123
abcd1234
```

## Branch And Commit Examples

```txt
issue-12-mt85-login-form
feature/abc123-scoreboard
bugfix/abcd1234-navbar-layout
```

```txt
mt85: add login form validation
abc123: fix scoreboard ordering
abcd1234: update README instructions
```

## Optional Local Hook

The commit-msg hook is an optional warning before push.
Server-side GitHub Actions remain the source of truth.

UCID format is intentionally flexible: use your official NJIT UCID, such as `mt85` or another official UCID with 2-4 letters and optional digits.

Install from repo root:

```bash
mkdir -p .git/hooks
cp hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```
