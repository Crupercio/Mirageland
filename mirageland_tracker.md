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

- [ ] Create simple quest model flow
- [ ] Add first quest chain
- [ ] Add simple reward logic
- [ ] Add one currency if needed
- [ ] Award ownership on completion
- [ ] Verify repeat and edge-case behavior

### GitHub Checkpoint

Push when a user can complete the loop locally without manual database edits.

## Phase 5: Figurine Viewer

### Goal

Show the first collectible in a polished character page.

### Tasks

- [ ] Create character detail page
- [ ] Add Three.js viewer shell
- [ ] Load placeholder or real model
- [ ] Add graceful loading and error states
- [ ] Connect variant switching

### GitHub Checkpoint

Push when the first figurine is viewable and stable in the browser.

## Phase 6: Display Room

### Goal

Let a player place an unlocked figurine onto a shelf and return later.

### Tasks

- [ ] Create display room model
- [ ] Create shelf slot model or layout system
- [ ] Build room page
- [ ] Save figurine placement
- [ ] Reload saved placement
- [ ] Add simple public/private room setting

### GitHub Checkpoint

Push when placement persists correctly and the room works end to end.

## Phase 7: MVP Expansion

### Goal

Grow the vertical slice into a small but complete product.

### Tasks

- [ ] Expand to 3 characters
- [ ] Expand to 9 variants total
- [ ] Add chapter 1 quest hub
- [ ] Add catalogue page
- [ ] Add basic reactions
- [ ] Add basic room theme selection

### GitHub Checkpoint

Push after each stable sub-milestone instead of waiting for the whole MVP to be done.

## Push Rules

- Push after something works, not before
- Update this tracker before each push
- Keep commits focused on one milestone or one coherent fix
- Never commit `.env`, credentials, production dumps, or private keys

## Latest Checkpoint

- `2026-04-10/11`: Phase 0, Phase 1, and Phase 2 foundation pushed to GitHub
- commit: `1dc39dc`
