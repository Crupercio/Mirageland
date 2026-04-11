# Mirageland Project Brief

## Project Summary

Mirageland is a story-driven virtual figurine collector built for the web. The player discovers characters, unlocks scene variants through light quest progression, and curates those figurines inside a personal display room. The game is not about combat. The shelf is the game.

## Product Goal

Build a small but polished first playable version that proves this loop is fun:

1. meet a character
2. unlock a variant through story progression
3. view the figurine in an interactive presentation
4. place it on a shelf
5. return and see lasting progress

## Core Experience Pillars

- `Collect and Display`: figurines are the primary reward and expression system
- `Story Unlocks`: progress comes from curiosity and light questing, not grind-heavy loops
- `Character Attachment`: a small number of strong characters matters more than broad roster size
- `Fair Progression`: players can earn meaningful progress without paywalls
- `Shelf Identity`: the display room is a personal, social-feeling space

## Phase 1 Product Shape

The first implementation target is a vertical slice, not a full launch.

That slice includes:

- 1 character
- 3 variants
- 1 room theme
- 1 display room
- 3 to 5 quests
- 1 simple currency
- basic account and ownership tracking

## First Vertical Slice Choice

- `Character`: Sora Kasumi
- `Reason`: strongest onboarding character, lore guide, emotionally representative of Mirageland, visually aligned with the default room fantasy

## First Success Criteria

The slice is successful when a local user can:

- create or access an account
- see Sora and her available variants
- complete a short quest sequence
- unlock at least one additional Sora variant
- view Sora in a character page with a figurine viewer
- place unlocked Sora variants in a display room
- revisit later and find progress preserved

## Technical Direction

- `Backend`: Django
- `Database`: PostgreSQL
- `Frontend`: Django templates + HTMX where useful
- `3D Presentation`: Three.js
- `Workflow`: local-first development, Git-tracked, deploy-safe from the start

## Rules For This Build

- keep scope intentionally small
- do not add WebXR to the vertical slice
- do not add premium currency yet
- do not block the slice on realtime features
- do not build systems for all 10 characters before one character feels good

## Current Build Strategy

1. define the vertical slice fully
2. scaffold the local Django/PostgreSQL project
3. implement one complete playable loop
4. push stable milestones to GitHub
5. expand only after the slice feels real

