# Mirageland Design Analysis

## Source Material Reviewed

- `mirageland_gdd.docx`
- `mirageland_claude_strategy.docx`

## Executive Take

Mirageland has a strong identity. The best parts are not the number of features, but the clarity of the fantasy:

- collecting characters as curated shelf pieces instead of combat units
- story-driven unlocks instead of pure luck
- a social display room as the heart of self-expression
- a soft, emotional cast with collectible depth

That said, the current documents describe a very large product. As written, this is closer to a full live-service roadmap than a first release. The vision is worth keeping, but the implementation plan needs to be reduced into a vertical slice first, then an MVP, then content expansion.

## What Is Strong and Worth Keeping

### 1. Core fantasy

The line "the shelf is the game" is the strongest design anchor in the material. It immediately separates Mirageland from generic gacha or stat battlers.

### 2. Character-first design

Ten deep original characters with repeatable scene variants is much better than a huge shallow roster. This creates attachment, replay value, and a cleaner content pipeline.

### 3. Fair progression

The "eventually unlock everything" philosophy is a major strength. It supports trust, reduces monetization toxicity, and fits the emotional tone of the project.

### 4. Display room as the social loop

The display room is the most viable long-term retention feature because it creates a reason to collect, customize, revisit, and share.

### 5. Django + Three.js split

The technical direction is sensible for this concept:

- Django for content, progression, auth, and operations
- Three.js for the figurine viewer and room presentation
- HTMX/templates for most UI to avoid unnecessary frontend overhead

## What Needs Improvement

### 1. Launch scope is too large

The GDD launch plan includes:

- 10 characters
- 30 launch figurines for MVP, then 80 total
- quest system
- economy
- social systems
- display room customization
- realtime features
- seasonal content
- WebXR

This is too much for an initial build unless there is already a team, budget, and asset pipeline in place.

### 2. Content volume comes too early

The projected launch content of roughly 148 quests is not MVP-sized. The first release should prove that the loop is fun with a very small amount of premium content.

### 3. Too many system dependencies

The original build order makes many features depend on many others at once. That raises integration risk early. The project needs a cleaner dependency chain:

- collectible data
- ownership/progression
- single-character quest loop
- figurine viewer
- shelf room
- social/economy polish later

### 4. WebXR is a later-stage feature

WebXR is exciting, but it is not core to validating whether collectors enjoy the main loop. It should move well after the first playable web version.

### 5. Realtime and Celery can wait

Channels, websocket notifications, and background tasks are good future architecture decisions, but they should not block the first vertical slice.

## My Recommended Product Shape

### Vertical Slice

Build one polished character journey end to end:

- 1 character
- 3 variants
- 1 display room
- 1 simple shelf layout
- 3 to 5 quests
- 1 currency
- 1 public shareable room page

If this feels good, the game has real legs.

### MVP

Expand only after the slice works:

- 3 characters
- 9 total variants
- chapter 1 only
- basic room customization
- simple profile/social reactions
- one reliable progression loop

### Full v1

Only after MVP validation:

- 10 characters
- expanded chapters
- premium currency
- events
- seasonal content
- richer room systems

## What I Am Taking From Each Document

### From the GDD

- world tone and narrative identity
- character-first collectible structure
- display-room-first player fantasy
- fair progression rules
- UI tone and visual direction

### From the strategy document

- phased build thinking
- emphasis on atomic economy operations
- separation of core systems by app/domain
- practical reminder to work in dependency order

## Recommended Design Changes

1. Reduce initial launch to a vertical slice, not a live-service launch.
2. Replace "10 characters at start" with "1 polished character, then expand."
3. Delay WebXR until after the browser version is stable and fun.
4. Delay seasonal events and advanced social features until the core loop is proven.
5. Keep Coins for early development; add Crystals/Fragments later if needed.
6. Start with one shelf room and one theme; expand after placement feels good.
7. Build quest content only after the figurine-viewer-to-ownership loop works.

## Success Criteria For The First Version

The first playable version should let a user:

- sign in
- view a character
- unlock a variant through a simple quest/task
- place the unlocked figurine on a shelf
- revisit the shelf and feel progress
- share or preview that shelf in a presentable way

If those six things feel good, Mirageland is on track.

