# Mirageland Tracker

This file is the working board for the project. We will update it as we complete tasks.

## Status Legend

- `[x]` Done
- `[ ]` Not started
- `[-]` In progress
- `[!]` Blocked

## Current Direction

- Local-first development
- PostgreSQL from day one
- Safe GitHub workflow from day one
- Vertical-slice-first scope

## Phase 0: Repository Foundation

### Goal

Set up the project so we can work locally without leaking secrets or losing track of progress.

### Tasks

- [x] Review original planning documents
- [x] Write design analysis
- [x] Write initial execution plan
- [x] Add `.gitignore`
- [x] Add `.env.example`
- [x] Add project `README.md`
- [x] Initialize local Git repository
- [x] Configure GitHub remote
- [x] Create first GitHub repository
- [x] Make first commit and push

### GitHub Checkpoint

Push once the repo has the planning docs and safety files in place.

## Phase 1: Vertical Slice Definition

### Goal

Define the smallest version of Mirageland that is still real and fun.

### Tasks

- [x] Write one-page project brief
- [x] Choose the first character
- [x] Choose the first 3 variants
- [x] Define the first room theme
- [x] Define the first 3 to 5 quests
- [x] Define slice-1 currency rules
- [x] Define reduced data model list
- [x] Freeze vertical slice scope

### GitHub Checkpoint

Push when the slice can be described clearly and no core feature in the slice is still ambiguous.

### Phase 1 Output

- [x] [mirageland_project_brief.md](./mirageland_project_brief.md)
- [x] [mirageland_vertical_slice.md](./mirageland_vertical_slice.md)

## Phase 2: Local Dev Foundation

### Goal

Create the local Django foundation with deploy-safe patterns.

### Tasks

- [x] Create Django project scaffold
- [x] Create core apps
- [x] Configure settings with environment variables
- [x] Connect local PostgreSQL
- [x] Add base template and static structure
- [x] Add custom user model if needed
- [x] Run initial migrations
- [x] Verify clean Django configuration
- [x] Verify homepage route works locally

### Notes

- PostgreSQL is reachable on `127.0.0.1:5432`
- local PostgreSQL database `mirageland` created successfully
- initial migrations applied successfully in PostgreSQL

### GitHub Checkpoint

Push when the app boots locally from a clean setup and migrations run successfully.

## Phase 3: Core Catalogue And Ownership

### Goal

Represent one character, three variants, and player ownership correctly.

### Tasks

- [x] Create `Character` model
- [x] Create `Variant` model
- [x] Create `OwnedVariant` model
- [x] Seed first character and variants
- [x] Add basic admin support
- [x] Verify data can be created and viewed

### GitHub Checkpoint

Push when seeded data is stable and ownership relationships behave correctly.

## Phase 4: First Playable Progression Loop

### Goal

Let a player unlock a figurine through a simple quest flow.

### Tasks

- [x] Create simple quest model flow
- [x] Add first quest chain
- [x] Add simple reward logic
- [x] Add one currency if needed
- [x] Award ownership on completion
- [x] Verify repeat and edge-case behavior

### GitHub Checkpoint

Push when a user can complete the loop locally without manual database edits.

## Phase 5: Figurine Viewer

### Goal

Show the first collectible in a polished character page.

### Tasks

- [x] Create character detail page
- [x] Add Three.js viewer shell
- [x] Load placeholder or real model
- [x] Add graceful loading and error states
- [x] Connect variant switching

### GitHub Checkpoint

Push when the first figurine is viewable and stable in the browser.

## Phase 6: Display Room

### Goal

Let a player place an unlocked figurine onto a shelf and return later.

### Tasks

- [x] Create display room model
- [x] Create shelf slot model or layout system
- [x] Build room page
- [x] Save figurine placement
- [x] Reload saved placement
- [x] Add simple public/private room setting

### GitHub Checkpoint

Push when placement persists correctly and the room works end to end.

## Phase 7: MVP Expansion

### Goal

Grow the vertical slice into a small but complete product.

### Tasks

- [x] Expand to 3 characters
- [x] Expand to 9 variants total
- [x] Add chapter 1 quest hub
- [x] Add catalogue page
- [x] Add basic reactions
- [x] Add basic room theme selection

### GitHub Checkpoint

Push after each stable sub-milestone instead of waiting for the whole MVP to be done.

## Phase 8: Deployment And Staging Prep

### Goal

Make the project ready for a first hosted staging environment without breaking the local workflow.

### Tasks

- [x] Add production-safe Django settings adjustments
- [x] Add a `/health/` endpoint
- [x] Add Railway config-as-code
- [x] Add deploy documentation
- [x] Support Railway-style Postgres environment variables
- [x] Reduce local-only warnings in base settings

### GitHub Checkpoint

Push after production config, healthcheck, and deployment docs are verified locally.

## Phase 9: Authentication And Real Player Accounts

### Goal

Replace the prototype collector flow with real signed-in user accounts.

### Tasks

- [x] Add signup page
- [x] Add login and logout flow
- [x] Add account summary page
- [x] Require auth for catalogue progression pages
- [x] Require auth for quests and room management
- [x] Redirect new accounts into the playable app
- [x] Add tests for auth-protected routes
- [x] Verify the full test suite after auth changes

### GitHub Checkpoint

Push when a new user can sign up, log in, and reach their own catalogue, quests, and room state.

## Push Rules

- Push after something works, not before
- Update this tracker before each push
- Keep commits focused on one milestone or one coherent fix
- Never commit `.env`, credentials, production dumps, or private keys

## Latest Checkpoint

- `2026-04-10/11`: Phase 0, Phase 1, and Phase 2 foundation pushed to GitHub
- commit: `1dc39dc`
- `2026-04-11`: Phase 3 core catalogue and ownership models pushed to GitHub
- commit: `bda3c3a`
- `2026-04-11`: Phases 4-6 quest loop, viewer shell, and display room pushed to GitHub
- commit: `a682418`
- `2026-04-11`: Phase 7 MVP catalogue and room expansion pushed to GitHub
- commit: `af8d46b`
- `2026-04-11`: Phase 8 deployment and staging prep pushed to GitHub
- commit: `b39346b`
