# IT490 Project Proposal Template

Use this template to define the project before implementation. The proposal should focus on what the team wants to build, what users can do, what data the system may need, and what should be realistic for the MVP and final demo.

Do not delete prompt text, examples, or headings. Add your team content only inside the annotated response blocks.

## Planning Workflow (Recommended)

You may draft this proposal in a shared Google Doc for collaboration.

Required workflow:

1. Keep one shared planning Google Doc for your team.
2. Include the Google Doc link in this proposal Markdown file under Project Summary (or a clearly labeled planning link line).
3. During planning and template completion, reach out to the instructor to review your proposal (Drop the link in your Discord thread and @ them).
4. Once approved, export the Google Doc to Markdown.
5. Carefully review the exported Markdown and fix any formatting issues (headings, lists, tables, and links).
6. Commit the approved Markdown file to the repository as the final submitted proposal.

## Submission Coverage (Required)

A submission-ready proposal should include:

1. Core User Stories with feature-complete scope for the project (recommended 5-8 stories, minimum 5).
2. Story coverage across the full user journey (onboarding, core actions, data lifecycle, error handling, and review/reporting where relevant).
3. At least one admin user story covering maintenance functionality (user management, role assignment, or app data management).
4. MVP goals mapped to a subset of those stories.
5. Final demo goals mapped to the remaining or expanded stories.
6. External API usage clearly defined (all projects require external APIs).
7. Enough supporting detail so another team member can understand what will be built.

## Course Architecture Note

All approved projects will eventually use the course's required multi-server architecture: APP, DB, RabbitMQ, and API. You do not need to design the full communication layer in this proposal. Focus on the project goal, user workflows, external data needs, stored data needs, and realistic MVP scope.

The detailed architecture, communication layer, deployment, and milestone requirements will be introduced separately. Do not replace those requirements with a custom deployment plan unless the instructor asks for one.

## Required Project Features

Every project must include these features regardless of project theme. Plan for all of them when writing user stories.

**Authentication and accounts:**

1. **Registration**: Users must be able to register for an account.
2. **Login and logout**: Users must be able to log in and log out. Sessions must be properly destroyed on logout.
3. **Profile management**: Users must be able to update their own profile information.
4. **Password security**: Passwords must not be stored in plaintext.

**Roles and permissions:**

5. **General user baseline**: General users have no role by default. Roles exist only to grant permissions above the general user level.
6. **Admin role with maintenance pages**: An admin role is required. Admins must have working maintenance pages in the web UI to manage user accounts, user roles, and application data (records from external APIs or team-created data).

**Data and integration:**

7. **External API integration**: At least one external API must be meaningfully integrated into the project workflow. See the External API Data section.

Include at least one user story for authentication flows and at least one user story for the admin role's maintenance functionality.

## Project Summary

STUDENT RESPONSE START

- Team name:
- Repository URL:
- Proposed project name:
- One-sentence project summary:
- Target users:
- Problem or need the project addresses:

STUDENT RESPONSE END

## Project Objective

Describe what the system is trying to accomplish and who it is for.

Include:

- The real user problem or scenario
- The primary outcome users should get from the system
- Why this project needs saved data, user interaction, and system integration instead of being a static page

STUDENT RESPONSE START

[Write 1-3 short paragraphs here.]

STUDENT RESPONSE END

## Core User Stories

Write user stories in this format:

- As a [user role], I want [behavior] so that [outcome/value].

For each story, add acceptance criteria.

Copy this block for each story (should have full project coverage):

Recommended story count for final submission: 5-8 stories.

Before submitting, make sure the full set of stories covers the required gradable behaviors below. You do not need one story per bullet, but every bullet should be clearly visible in at least one story, acceptance criterion, workflow, or data note:

- Account access: registration, login, logout, profile update, and password security.
- General user behavior: what a normal user can create, view, update, save, or delete.
- Admin maintenance behavior: how an admin manages users, roles, or application data.
- External API behavior: what outside data is requested and how it affects the user workflow.
- Stored data behavior: what team-owned data is saved and how it is connected to users.
- Ownership and authorization: how the system prevents one user from changing another user's data.
- Error or unavailable-service behavior: what users see when data, validation, or an API request fails.
- Course service evidence: where APP, DB, RabbitMQ, and API are expected to appear at a high level by MVP or final demo.

STUDENT RESPONSE START

Story ID: US-01
User story: As a [role], I want [behavior] so that [outcome].

Acceptance criteria:
- [ ] AC1:
- [ ] AC2:
- [ ] AC3:

Data needed:
- User-created data:
- External API data:

Service touchpoints (high-level):
- APP: [One sentence: what this story does in APP]
- DB: [One sentence: what data this story creates/reads/updates]
- RabbitMQ: [One sentence: what event/message this story publishes or consumes]
- API: [One sentence: which external API call or data this story uses]

How to answer touchpoints:

1. Keep each touchpoint to 1-2 plain-language sentences.
2. Use action words: receives, validates, stores, publishes, consumes, requests, returns.
3. If something is not used for this story yet, write `Not used in this story`.

Optional detail (add only if useful now):
- APP detail:
- DB detail:
- RabbitMQ detail:
- API detail:
- Notes for later implementation:

STUDENT RESPONSE END

## Core User Workflows

Use short workflow bullets that map to your user stories.

Example:

- US-01 workflow: User searches for item -> selects item -> saves item -> sees saved item in dashboard.

STUDENT RESPONSE START

- US-__ workflow:
- US-__ workflow:
- US-__ workflow:
- US-__ workflow:
- US-__ workflow:

STUDENT RESPONSE END

## External API Data

This section is required. All projects must use at least one external API.

Keep this section high-level. Identify a realistic data source and explain why it matters to the project. Include how the data will be used or stored and what should happen when the API is unavailable. Exact request formats and implementation details can be refined later.

STUDENT RESPONSE START

API 1:
- Name:
- Documentation link:
- Fields needed:
- How used in user stories:
- Fetch/cache/storage plan:
- Failure handling plan:

API 2 (optional):
- Name:
- Documentation link:
- Fields needed:
- How used in user stories:
- Fetch/cache/storage plan:
- Failure handling plan:

STUDENT RESPONSE END

## Stored Data Model

Keep this section high-level. You can refine names/fields later.

Describe the project-specific data stored in the team's own database.

Include expected tables or collections such as:

- Users or user profile data
- External API records saved locally
- User-owned records
- Relationship or association tables
- Audit, log, status, or history records when relevant

STUDENT RESPONSE START

Data entity 1:
- Name:
- Purpose:
- Important fields:
- Created by:
- Updated by:

Data entity 2:
- Name:
- Purpose:
- Important fields:
- Created by:
- Updated by:

STUDENT RESPONSE END

## User Data Associations

Keep this simple: explain who owns what data and who can change it.

Include:

- Which records belong to a specific user
- Which records are shared across users
- Which records are admin-only or team-managed
- How the system prevents one user from changing another user's data

STUDENT RESPONSE START

Association 1:
- User action:
- Stored association:
- Access rule:

Association 2:
- User action:
- Stored association:
- Access rule:

STUDENT RESPONSE END

## Cross-Domain Feature Ownership

Students are expected to work cross-domain. If a feature touches APP, API, RabbitMQ, and DB, the feature owner should be responsible for the full slice.

Recommended team practice:

1. Break larger features into smaller linked tasks so teammates can help.
2. Trade task ownership when useful for learning and workload balance.
3. Keep one clear owner per feature while allowing collaborators on subtasks.
4. Keep excessive collaborators on each issue/PR to a minimum (the whole team should not be collectively assigned to every feature).

STUDENT RESPONSE START

Feature slice ownership plan:

- Feature/story US-__:
	- Primary owner:
	- Cross-domain touchpoints: APP / API / RabbitMQ / DB
	- Planned subtasks for collaboration:

- Feature/story US-__:
	- Primary owner:
	- Cross-domain touchpoints: APP / API / RabbitMQ / DB
	- Planned subtasks for collaboration:

STUDENT RESPONSE END

## Team Members And Responsibilities

List each team member's expected responsibilities. Responsibilities can overlap, but each person should have visible ownership.

STUDENT RESPONSE START

Team member 1:
- Name:
- Primary responsibilities:
- Services/features touched:


Team member 2:
- Name:
- Primary responsibilities:
- Services/features touched:


STUDENT RESPONSE END

## MVP Goals

The MVP is the minimum useful version of the project that should be ready for the midterm milestone.

List the required MVP behaviors and reference story IDs.

Use this format:

1. [MVP item title] -> Story IDs: US-__ [, US-__] -> Required ACs: US-__ AC__
2. [MVP item title] -> Story IDs: US-__ [, US-__] -> Required ACs: US-__ AC__
3. [MVP item title] -> Story IDs: US-__ [, US-__] -> Required ACs: US-__ AC__

Use plain language for each item. You are describing goals, not implementation steps.

The MVP should be demo-ready. It should show working behavior, not only plans or screenshots.

STUDENT RESPONSE START

1. [MVP item] -> Story IDs: US-__ -> Required ACs: US-__ AC__
2. [MVP item] -> Story IDs: US-__ -> Required ACs: US-__ AC__
3. [MVP item] -> Story IDs: US-__ -> Required ACs: US-__ AC__

STUDENT RESPONSE END

## Final Demo Goals

List the additional behavior expected by the final demo and reference story IDs.

Use this format:

1. [Final demo item title] -> Story IDs: US-__ [, US-__] -> Required ACs: US-__ AC__
2. [Final demo item title] -> Story IDs: US-__ [, US-__] -> Required ACs: US-__ AC__
3. [Final demo item title] -> Story IDs: US-__ [, US-__] -> Required ACs: US-__ AC__

Final demo items should extend MVP scope, not repeat the same exact goal statements.

STUDENT RESPONSE START

1. [Final item] -> Story IDs: US-__ -> Required ACs: US-__ AC__
2. [Final item] -> Story IDs: US-__ -> Required ACs: US-__ AC__
3. [Final item] -> Story IDs: US-__ -> Required ACs: US-__ AC__

STUDENT RESPONSE END

## Stretch Features

Stretch features are optional improvements after required MVP, milestone, and final demo requirements are stable.

Stretch features should not replace required work. If a stretch feature threatens the MVP, milestones, or final demo, postpone it.

STUDENT RESPONSE START

Stretch feature 1:
- Why it helps:
- Risk/dependency:
- Attempt only after:

Stretch feature 2:
- Why it helps:
- Risk/dependency:
- Attempt only after:

STUDENT RESPONSE END

## Approval Checklist

Before submitting the proposal, confirm:

- The project objective is specific enough to evaluate
- Authentication flows (register, login, logout, and profile update) are covered in user stories
- Password security approach is noted (passwords will not be stored in plaintext)
- Admin role, role/permission model, and maintenance pages are planned and covered by at least one user story
- At least one external API is required, documented, and relevant
- The team-owned database data is described
- User-data associations are clear
- Core user stories represent feature-complete scope (recommended 5-8, minimum 5)
- Service touchpoints are defined at a useful high level for each story (APP, DB, RabbitMQ, API)
- MVP and final demo goals are realistic
- MVP and final demo items reference story IDs and acceptance criteria
- MVP and final demo goals together cover the core user stories
- Stretch features are clearly optional
- Team responsibilities are visible
- The approved proposal Markdown is committed to the team repository

## AI Disclosure

Disclose any meaningful AI help used for this proposal. Include what the AI helped with, what you changed, and how you verified the result. If you did not use AI, write "No meaningful AI assistance used."

STUDENT RESPONSE START

[Your disclosure text here]

STUDENT RESPONSE END
