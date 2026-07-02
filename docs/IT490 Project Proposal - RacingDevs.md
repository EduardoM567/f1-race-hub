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
Authentication and accounts:

1. Registration: Users must be able to register for an account.  
2. Login and logout: Users must be able to log in and log out. Sessions must be properly destroyed on logout.  
3. Profile management: Users must be able to update their own profile information.  
4. Password security: Passwords must not be stored in plaintext.

Roles and permissions:

5. General user baseline: General users have no role by default. Roles exist only to grant permissions above the general user level.  
6. Admin role with maintenance pages: An admin role is required. Admins must have working maintenance pages in the web UI to manage user accounts, user roles, and application data (records from external APIs or team-created data).

Data and integration:

7. External API integration: At least one external API must be meaningfully integrated into the project workflow. See the External API Data section.

Include at least one user story for authentication flows and at least one user story for the admin role's maintenance functionality.

## Project Summary

* Team name: Racing Devs  
* Repository URL: [https://github.com/MattToegel/it490-m2026-racingdevs](https://github.com/MattToegel/it490-m2026-racingdevs)   
* Proposed project name: F1 Race Hub  
* One-sentence project summary: A web application that allows users to view Formula 1 race data, track drivers/teams, and save their favorite races and stats  
* Target users: Formula 1 fans, beginners learning F1, and sports data enthusiasts  
* Problem or need the project addresses: There is F1 data scattered across multiple websites and users want one simple place to view, track and personalize race and driver information

## Project Objective

Describe what the system is trying to accomplish and who it is for.  
Include:

* The real user problem or scenario  
* The primary outcome users should get from the system  
* Why this project needs saved data, user interaction, and system integration instead of being a static page

This system will aim to provide a centralized platform where users are able to explore Formula 1 data such as races, drivers, standing, and results. This will make it easier fo  se r users to be able to save favorites, track stats, and personalize their experience. 

The main goal is for users to easily access and interact with F1 data without needing multiple websites. They can log in, save their favorite drivers or races, and track updates over time.

This project will require saved data and system integration because it uses real-time or external F1 data, stores user preferences, and allows interaction beyond just viewing static information.

## Core User Stories

Write user stories in this format:

* As a \[user role\], I want \[behavior\] so that \[outcome/value\].

For each story, add acceptance criteria.  
Copy this block for each story (should have full project coverage):  
Recommended story count for final submission: 5-8 stories.  
Before submitting, make sure the full set of stories covers the required gradable behaviors below. You do not need one story per bullet, but every bullet should be clearly visible in at least one story, acceptance criterion, workflow, or data note:

* Account access: registration, login, logout, profile update, and password security.  
* General user behavior: what a normal user can create, view, update, save, or delete.  
* Admin maintenance behavior: how an admin manages users, roles, or application data.  
* External API behavior: what outside data is requested and how it affects the user workflow.  
* Stored data behavior: what team-owned data is saved and how it is connected to users.  
* Ownership and authorization: how the system prevents one user from changing another user's data.  
* Error or unavailable-service behavior: what users see when data, validation, or an API request fails.  
* Course service evidence: where APP, DB, RabbitMQ, and API are expected to appear at a high level by MVP or final demo.

STUDENT RESPONSE START  
Story ID: US-01 Authentication  
User story: As a user, I want to register, log in, and log out so that I can have a personal account  
Acceptance criteria:

* AC1: Registration form includes username, email, and password fields  
* AC2: System validates required fields and shows error messages (“Password must be 8+ characters”)  
* AC3: User can log in using valid credentials and is redirected to the dashboard  
* AC4: Invalid login shows error message (“Incorrect username or password”)  
* AC5: User can log out and session is terminated

Data needed:

* User-created data: User credentials  
* External API data: None

Service touchpoints (high-level):

* APP: Handles login/register requests  
* DB: Stores user account data  
* RabbitMQ: Not used   
* API: Not used

How to answer touchpoints:

1. Keep each touchpoint to 1-2 plain-language sentences.  
2. Use action words: receives, validates, stores, publishes, consumes, requests, returns.  
3. If something is not used for this story yet, write Not used in this story.

Optional detail (add only if useful now):

* APP detail:  
* DB detail:  
* RabbitMQ detail:  
* API detail:  
* Notes for later implementation:

STUDENT RESPONSE END

STUDENT RESPONSE START  
Story ID: US-02 View F1 Data  
User story: As a user I want to view F1 races, drivers, and standings so that I can stay updated  
Acceptance criteria:

*  AC1: User can view a race schedule list including: race name, date, and location  
*  AC2: User can view a driver standings table including: driver name, team, points, and position  
* AC3: User can click a driver to view a driver detail page including: name, team, nationality, and stats (wins, podiums, points)  
* AC4: Data loads from external API  
* AC5: If no data is available, system shows empty state message: “No data available at this time”

Data needed:

* User-created data: None   
* External API data: race schedule (race name, date, location), driver standings (name, team, points, position), driver details (nationality, stats)

Service touchpoints (high-level):

* APP: Receives user request for F1 data and displays the results in a clean UI  
* DB: Caches frequently accessed F1 data (schedule, standings, drivers) for fast loading  
* RabbitMQ: Receives fetch requests from APP and publishes them to the API service for processing   
* API: Consumes messages from RabbitMQ, requests data from OpenF1, processes/transforms it, and returns results

How to answer touchpoints:

4. Keep each touchpoint to 1-2 plain-language sentences.  
5. Use action words: receives, validates, stores, publishes, consumes, requests, returns.  
6. If something is not used for this story yet, write Not used in this story.

Optional detail (add only if useful now):

* APP detail:  
* DB detail:  
* RabbitMQ detail:  
* API detail:  
* Notes for later implementation:

STUDENT RESPONSE END

STUDENT RESPONSE START  
Story ID: US-03 Save Favorites  
User story: As a user, I want to save my favorite drivers or races so that I can easily access them later  
Acceptance criteria:

* AC1: User can click “Save” on a driver or race  
* AC2: System stores favorite with fields: user\_id, item\_id, item\_type  
* AC3: User can view a Favorites list page displaying: item name, item type (drive or race)

AC4: If no favorites exist, show empty state message: “No favorites saved yet”  
AC5: User can rename a favorites list  
AC6: User can filter favorites by type (drives vs races)

* AC7: User can remove items from favorites  
* AC8: Only the logged in user can view their own favorites

Data needed:

* User-created data: Favorite items (user\_id, item\_id, item\_type)  
* External API data: Driver information (name, team, etc.)

Service touchpoints (high-level):

* APP: Handles save actions  
* DB: Stores favorites  
* RabbitMQ: Sends save event  
* API: Uses driver data

How to answer touchpoints:

7. Keep each touchpoint to 1-2 plain-language sentences.  
8. Use action words: receives, validates, stores, publishes, consumes, requests, returns.  
9. If something is not used for this story yet, write Not used in this story.

Optional detail (add only if useful now):

* APP detail:  
* DB detail:  
* RabbitMQ detail:  
* API detail:  
* Notes for later implementation:

STUDENT RESPONSE END

STUDENT RESPONSE START  
Story ID: US-04 Profile Management   
User story: As a user I want to update my profile so that my information stays current  
Acceptance criteria:

*  AC1: User can update profile information such as username, email, password (optional update)  
* AC2: User can submit updates and receive confirmation message (“Profile updated successfully”)  
*  AC3: Changes are saved in DB and reflect immediately  
*  AC4: Unauthorized users cannot edit others   
* AC5: Unauthorized access attempts redirect to an error or login page

Data needed:

* User-created data: username, email, password (hashed)  
* External API data: None

Service touchpoints (high-level):

* APP: Handles updates  
* DB: Updates user information  
* RabbitMQ: Not used  
* API: Not used

How to answer touchpoints:

10. Keep each touchpoint to 1-2 plain-language sentences.  
11. Use action words: receives, validates, stores, publishes, consumes, requests, returns.  
12. If something is not used for this story yet, write Not used in this story.

Optional detail (add only if useful now):

* APP detail:  
* DB detail:  
* RabbitMQ detail:  
* API detail:  
* Notes for later implementation:

STUDENT RESPONSE END

STUDENT RESPONSE START  
Story ID: US-05 Admin Management  
User story: As an admin I want to manage users and data so that the system stays organized  
Acceptance criteria:

* AC1: Admin can view a user list table including: username, email, role, and account\_status  
* AC2: Admin can assign and update roles  
* AC3: Admin can disable or reactivate user accounts instead of only hard deleting users  
* AC4: When an account is disabled, the system updates account\_status and disabled\_at  
* AC5: Admin can delete invalid or outdated stored data  
* AC6: Admin can trigger refresh of external data (e.g., reload race schedules from API)  
* AC7: Non-admin users cannot access admin dashboard (authorization enforced)  
* AC8: Unauthorized access shows error message: “Access denied”

Data needed:

* User-created data: Roles, user account records, account\_status, disabled\_at  
* External API data: Cached data

Service touchpoints (high-level):

* APP: Admin dashboard  
* DB: Stores roles/data  
* RabbitMQ: Sends update events  
* API: May refresh data

How to answer touchpoints:

13. Keep each touchpoint to 1-2 plain-language sentences.  
14. Use action words: receives, validates, stores, publishes, consumes, requests, returns.  
15. If something is not used for this story yet, write Not used in this story.

Optional detail (add only if useful now):

* APP detail:  
* DB detail:  
* RabbitMQ detail:  
* API detail:  
* Notes for later implementation:

STUDENT RESPONSE END

STUDENT RESPONSE START  
Story ID: US-06 Error Handling  
User story: As a user I want to see error messages when something fails so that I can understand what happened  
Acceptance criteria:

* AC1: Shows error if API fails: “Unable to load data. Please try again later.”  
* AC2: Form validation errors display next to the relevant fields  
* AC3: Network errors show retry options  
* AC4:User-friendly error pages are shown for: 404 (page not found) and 500 (server error)

Data needed:

* User-created data: None  
* External API data: API failure states

Service touchpoints (high-level):

* APP: Displays errors  
* DB: Logs errors  
* RabbitMQ: Logs events  
* API: Handles failure

How to answer touchpoints:

16. Keep each touchpoint to 1-2 plain-language sentences.  
17. Use action words: receives, validates, stores, publishes, consumes, requests, returns.  
18. If something is not used for this story yet, write Not used in this story.

Optional detail (add only if useful now):

* APP detail:  
* DB detail:  
* RabbitMQ detail:  
* API detail:  
* Notes for later implementation:

STUDENT RESPONSE END

## Core User Workflows

Use short workflow bullets that map to your user stories.  
Example:

* US-01 workflow: User searches for item \-\> selects item \-\> saves item \-\> sees saved item in dashboard.

STUDENT RESPONSE START

* US-01 workflow: user searches for account creation/login \-\> selects create account \-\> types in username, password, and other essential information \-\> brought to the dashboard \-\> selects logout \-\> brought to login page  
* US-02 workflow: user searches for race schedule \-\> selects race schedule \-\> sees race schedule in dashboard \-\> searches for race standing \-\> selects race standing \> sees race standing in dashboard  
* US-03 workflow: user searches for drivers \-\> selects driver \-\> sees driver in dashboard \-\> selects favorite button on driver \-\> search for favorites section \-\> selects favorites section \-\>sees favorite drivers \-\> searches for delete button on favorites tab \-\> selects delete button \-\> sees driver deleted from favorite section \-\> searches for edit button \-\> sees edit button \-\> selects edit button  
* US-04 workflow: User searches for profile tab \-\> selects profile tab \-\> searches for username or password change \-\> select username/password change \-\> Insert new username/password \-\> select confirm button \-\> see the change on dashboard  
* US-05 workflow:user searches for admin panel \-\> user selects admin panel \-\> user sees users tab \-\> user selects user tab \-\> users sees users in dashboard \-\> user selects a user \-\> user sees user permission \-\> User adds role to user \-\> user searches for driver schedule data tab \-\> user selects data tab \-\> user changes schedule data \- sees schedule data changes in dashboard  
* US-06 workflow: user searches for information \-\> user selects driver schedule tab \-\> user receives error message \-\> user searches for admin panel \-\> uses selects admin panel \-\> user selects schedule tab \-\> user enters schedule information in incorrect format \-\> user receives incorrect format error message

STUDENT RESPONSE END

## External API Data

This section is required. All projects must use at least one external API.  
Keep this section high-level. Identify a realistic data source and explain why it matters to the project. Include how the data will be used or stored and what should happen when the API is unavailable. Exact request formats and implementation details can be refined later.  
STUDENT RESPONSE START  
API 1:

* Name: Open F1  
* Documentation link: https://openf1.org/  
* Fields needed:   
  * Races/Sessions: session\_key, meeting\_key, session\_name, date\_start, date\_end, session\_type  
  * Drivers: driver\_number, full\_name, name\_acronym, team\_name, team\_color, first\_name, last\_name  
  * Standings: position\_current, points\_current, driver\_number, team\_name  
  * Race Results/Schedule: laps, intervals, positions, pit stops  
* How used in user stories:  
  * US-02: Fetch and display race schedule, driver standings, and current race information.  
  * US-03: Pull driver/race details when users save favorites  
  * US-05: Admin can trigger manual refresh of cached F1 data  
* Fetch/cache/storage plan:  
  * API service will make GET requests to [https://api.openf1.org/v1/](https://api.openf1.org/v1/) endpoints (sessions, drivers, championship\_drivers, etc.)  
  * Use RabbitMQ to publish “fetch data” events  
  * Check cached\_f1 data first, if fresh cached data exists return immediately. If the cache is missing or stale, request fresh data from OpenF1, update the cache, and return the new results  
  * Cache frequently used data (standings, schedule , drivers) in our DB to reduce API calls and improve performance  
  * Background worker (via RabbitMQ) will periodically refresh data every 24 hours, standings refresh every 1 hour during active race weekends, and driver/team data refresh every 7 days unless an admin forces a refresh  
* Failure handling plan:  
  * If OpenF1 is unavailable, first attempt to return cached data. If fresh cached data exists, return it normally. If only stale cached exists, display the stale data with a “Last updated” label and the message: “Live data temporarily unavailable \- showing last cached results.”  
  * If no cache data exists, display: “Live data temporarily unavailable. Please try again later.”  
  * Log errors and retry with exponential backoff  
  * Rate limit handling (respect 3 req/sec free tier)

API 2 (optional):

* Name:  
* Documentation link:  
* Fields needed:  
* How used in user stories:  
* Fetch/cache/storage plan:  
* Failure handling plan:

STUDENT RESPONSE END

## Stored Data Model

Keep this section high-level. You can refine names/fields later.  
Describe the project-specific data stored in the team's own database.  
Include expected tables or collections such as:

* Users or user profile data  
* External API records saved locally  
* User-owned records  
* Relationship or association tables  
* Audit, log, status, or history records when relevant

STUDENT RESPONSE START  
Data entity 1: 

* Name: Users  
* Purpose: Store user account and profile information for authentication and profile management  
* Important fields: user\_ID, username, email, password, role, created\_at, updated\_at, account\_status, disabled\_at  
* Created by: System  
* Updated by: User/Admin

Data entity 2:

* Name: Favorites  
* Purpose: Store saved drivers/races  
* Important fields: user\_id, item\_id, type, favorites\_id, list\_name, updated\_at, created\_at  
* Created by: User  
* Updated by: User

Data entity 3:

* Name: cached\_f1\_data  
* Purpose: Store external API data locally for faster access and fallback when API is unavailable  
* Important fields: cache\_id, data\_type, data\_payload, last\_updated, cached\_at, expires\_at, source\_endpoint, query\_params  
* Created by: System/API  
* Updated by: System/API

Data entity 4:

* Name: admin\_audit\_logs  
* Purpose: Record admin actions for accountability and system monitoring  
* Important fields: audit\_id, admin\_id, action\_type, target\_entity, target\_id  
* Created by: Admin  
* Updated by: Not typically updated

Data entity 5:

* Name: api\_error\_logs  
* Purpose: Store API and system error information for debugging and monitoring  
* Important fields: error\_id, error\_type, error\_message, endpoint, status\_code  
* Created by: System/API  
* Updated by: Not typically updated

STUDENT RESPONSE END

## User Data Associations

Keep this simple: explain who owns what data and who can change it.  
Include:

* Which records belong to a specific user  
* Which records are shared across users  
* Which records are admin-only or team-managed  
* How the system prevents one user from changing another user's data

STUDENT RESPONSE START  
Association 1:

* User action: Save favorite   
* Stored association: favorites.user\_id → favorite  
* Access rule: Users can create, view, rename, filter, and remove only favorites where favorites.user\_id matches the logged in user

Association 2:

* User action: Admin assigns role  
* Stored association: user\_id → role  
* Access rule: Admin only

Association 3:

* User action: View cached F1 data  
* Stored association: cached\_f1\_data (shared application data)  
* Access rule: All users can read cached F1 data. Only the API admins or the API worker/background can refresh or delete cached records

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

* Feature/story US-01: Authentication  
  * Primary owner: Michelle  
  * Cross-domain touchpoints: APP / DB  
  * Planned subtasks for collaboration: Registration, login/logout, password hashing, session handling  
* Feature/story US-02: View F1 Data  
  * Primary owner: Eduardo  
  * Cross-domain touchpoints: APP / API / RabbitMQ   
  * Planned subtasks for collaboration: API integration, fetching race/driver data, displaying data  
* Feature/story US-03: Save Favorites  
  * Primary owner: Branden  
  * Cross-domain touchpoints: APP / RabbitMQ / DB  
  * Planned subtasks for collaboration: Save favorites, retrieve favorites, enforce user ownership  
* Feature/story US-04: Profile Management  
  * Primary owner: Omar  
  * Cross-domain touchpoints: APP / DB   
  * Planned subtasks for collaboration: Update profile information, validation, secure updates  
* Feature/story US-05: Admin Management  
  * Primary owner: Ruchir  
  * Cross-domain touchpoints: APP / API / RabbitMQ / DB  
  * Planned subtasks for collaboration: Admin dashboard, user role management, data moderation

STUDENT RESPONSE END

## Team Members And Responsibilities

List each team member's expected responsibilities. Responsibilities can overlap, but each person should have visible ownership.  
STUDENT RESPONSE START  
Team member 1:

* Name: Michelle  
* Primary responsibilities: Authentication system, password security, session management   
* Services/features touched: APP, DB

Team member 2:

* Name: Eduardo  
* Primary responsibilities: External API integration, displaying F\! data  
* Services/features touched: API, APP, RabbitMQ

Team member 3:

* Name:  Branden  
* Primary responsibilities: Favorites system, user-specific data handling  
* Services/features touched: APP, DB, RabbitMQ

Team member 4:

* Name: Omar  
* Primary responsibilities: Profile management, input validation, user updates  
* Services/features touched: APP, DB

Team member 5:

* Name: Ruchir Patel  
* Primary responsibilities: Admin panel, role management, system maintenance   
* Services/features touched: APP, DB, RabbitMQ, API

STUDENT RESPONSE END

## MVP Goals

The MVP is the minimum useful version of the project that should be ready for the midterm milestone.  
List the required MVP behaviors and reference story IDs.  
Use this format:

1. \[MVP item title\] \-\> Story IDs: US-\_\_ \[, US-\] \-\> Required ACs: US- AC\_\_  
2. \[MVP item title\] \-\> Story IDs: US-\_\_ \[, US-\] \-\> Required ACs: US- AC\_\_  
3. \[MVP item title\] \-\> Story IDs: US-\_\_ \[, US-\] \-\> Required ACs: US- AC\_\_

Use plain language for each item. You are describing goals, not implementation steps.  
The MVP should be demo-ready. It should show working behavior, not only plans or screenshots.  
STUDENT RESPONSE START

1. Authentication system → Story IDs: US-01 → Required ACs: US-01 AC1, US-01 AC2, US-01 AC3, US-01 AC5  
2. View F1 race data/standings → Story IDs: US-02 → Required ACs: US-02 AC1, US-02 AC2, US-02 AC3  
3. Save/view favorite drives or races → Story IDs: US-03 → Required ACs: US-03 AC1, US-03 AC2, US-03 AC3, US-03 AC7, US-03 AC8

STUDENT RESPONSE END

## Final Demo Goals

List the additional behavior expected by the final demo and reference story IDs.  
Use this format:

1. \[Final demo item title\] \-\> Story IDs: US-\_\_ \[, US-\] \-\> Required ACs: US- AC\_\_  
2. \[Final demo item title\] \-\> Story IDs: US-\_\_ \[, US-\] \-\> Required ACs: US- AC\_\_  
3. \[Final demo item title\] \-\> Story IDs: US-\_\_ \[, US-\] \-\> Required ACs: US- AC\_\_

Final demo items should extend MVP scope, not repeat the same exact goal statements.  
STUDENT RESPONSE START

1. Admin user management dashboard → Story IDs: US-05 → Required ACs: US-05 AC1, US-05 AC2, US-05 AC3  
2. User profile management → Story IDs: US-04 → Required ACs: US-04 AC1, US-04 AC2, US-04 AC3  
3. System error handling and API failure messaging → Story IDs: US-06 → Required ACs: US-06 AC1, US-06 AC2, US-06 AC3

STUDENT RESPONSE END

## Stretch Features

Stretch features are optional improvements after required MVP, milestone, and final demo requirements are stable.  
Stretch features should not replace required work. If a stretch feature threatens the MVP, milestones, or final demo, postpone it.  
STUDENT RESPONSE START  
Stretch feature 1: Live race updates

* Why it helps: More engaging  
* Risk/dependency: API limits  
* Attempt only after: MVP complete

Stretch feature 2:

* Why it helps:   
* Risk/dependency:  
* Attempt only after:

STUDENT RESPONSE END

## Approval Checklist

Before submitting the proposal, confirm:

* The project objective is specific enough to evaluate  
* Authentication flows (register, login, logout, and profile update) are covered in user stories  
* Password security approach is noted (passwords will not be stored in plaintext)  
* Admin role, role/permission model, and maintenance pages are planned and covered by at least one user story  
* At least one external API is required, documented, and relevant  
* The team-owned database data is described  
* User-data associations are clear  
* Core user stories represent feature-complete scope (recommended 5-8, minimum 5\)  
* Service touchpoints are defined at a useful high level for each story (APP, DB, RabbitMQ, API)  
* MVP and final demo goals are realistic  
* MVP and final demo items reference story IDs and acceptance criteria  
* MVP and final demo goals together cover the core user stories  
* Stretch features are clearly optional  
* Team responsibilities are visible  
* The approved proposal Markdown is committed to the team repository

## AI Disclosure

Disclose any meaningful AI help used for this proposal. Include what the AI helped with, what you changed, and how you verified the result. If you did not use AI, write "No meaningful AI assistance used."  
STUDENT RESPONSE START  
No AI used in the writing of this  
STUDENT RESPONSE END  
