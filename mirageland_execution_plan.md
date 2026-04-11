# Mirageland Execution Plan

## Current Status

- `Done`: Source docs reviewed
- `Done`: Core strengths and risks identified
- `Next`: Build the project brief and vertical slice scope
- `Later`: Start implementation only after the scope is locked

## Tracking Rules

Use these states for every task:

- `Done`
- `In Progress`
- `Next`
- `Blocked`
- `Later`

Update this file as we move so it stays our single source of truth.

## The Plan I Recommend

We will build Mirageland in three layers:

1. `Preproduction`
2. `Vertical Slice`
3. `MVP Expansion`

This keeps the vision intact while making execution realistic.

## Phase 1: Preproduction

### Goal

Lock the smallest version of the game that still feels like Mirageland.

### Deliverables

- concise project brief
- vertical slice feature list
- reduced data model list
- first character selection
- first 3 variants selection
- first quest chain outline

### Tasks

- `Next` Write a one-page project brief
- `Next` Choose the first launch character
- `Next` Define the first 3 variants for that character
- `Next` Define the first room theme
- `Next` Define 3 to 5 quests for the first character arc
- `Next` Confirm what currencies exist in slice 1
- `Later` Write the full lore bible
- `Later` Define all 10 characters in implementation detail

### Definition of Done

We can explain the first playable experience in under one minute without referring back to the full GDD.

## Phase 2: Vertical Slice

### Goal

Prove the full game loop with the smallest polished version.

### Scope

- 1 character
- 3 variants
- 1 quest chain
- 1 room theme
- 1 shelf layout
- 1 currency
- basic account flow

### Milestone 2.1: Project Foundation

- `Later` Create Django project scaffold
- `Later` Set up apps: accounts, catalogue, collection, quests, economy
- `Later` Configure database and environment settings
- `Later` Add base templates and static pipeline

### Milestone 2.2: Core Data

- `Later` Build Character model
- `Later` Build Variant model
- `Later` Build OwnedVariant model
- `Later` Seed the first character and 3 variants

### Milestone 2.3: First Progression Loop

- `Later` Implement one simple currency
- `Later` Implement one quest chain
- `Later` Award variant unlock from quest completion
- `Later` Track ownership correctly

### Milestone 2.4: Figurine Presentation

- `Later` Build the character detail page
- `Later` Add one Three.js figurine viewer
- `Later` Support loading one real model or placeholder asset
- `Later` Add graceful fallback if model is missing

### Milestone 2.5: Shelf Loop

- `Later` Build one display room page
- `Later` Add shelf slot placement
- `Later` Save placed figurine positions
- `Later` Reload room state correctly

### Milestone 2.6: First Shareable Result

- `Later` Make room viewable by URL
- `Later` Add a simple public/private toggle
- `Later` Add a basic visit counter

### Definition of Done

A player can unlock a figurine, place it in a room, and return later to see that progress preserved.

## Phase 3: MVP Expansion

### Goal

Turn the slice into a small but complete product.

### Scope

- 3 characters
- 9 variants total
- chapter 1 narrative
- basic catalogue
- basic room customization
- simple social reactions

### Tasks

- `Later` Expand from 1 character to 3
- `Later` Add chapter 1 quest hub
- `Later` Add basic catalogue browsing
- `Later` Add bond progression if still valuable
- `Later` Add reactions to public rooms
- `Later` Add a second and third room theme
- `Later` Add content/admin workflow for seeding new variants

### Definition of Done

The product has a clear beginning, repeatable collector loop, and enough content for players to understand the larger vision.

## Explicitly Deferred

These should not block the first slice:

- WebXR support
- seasonal events
- premium currency complexity
- live websocket reactions
- gifting
- spotlight systems
- full 10-character roster
- chapter 2 to 5 implementation

## Immediate Next Small Goals

These are the tasks I suggest we do first:

1. `Next` Write a short project brief from this plan.
2. `Next` Pick the first character for the vertical slice.
3. `Next` Define the exact 3 variants and how they unlock.
4. `Next` Draft the reduced Django data model list.
5. `Next` Start the project scaffold.

## Progress Log

### 2026-04-10

- `Done` Reviewed both planning documents
- `Done` Extracted the strongest design pillars
- `Done` Reframed the project into a vertical-slice-first plan
- `Next` Convert this plan into the actual implementation brief

