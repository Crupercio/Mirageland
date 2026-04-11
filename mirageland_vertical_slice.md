# Mirageland Vertical Slice Specification

## Purpose

This document defines the first playable version of Mirageland in concrete terms so implementation can begin without scope drift.

## Slice Identity

- `Character`: Sora Kasumi
- `Theme`: Warm Library
- `Progression Style`: light narrative quests with direct figurine rewards
- `Primary Feeling`: calm wonder, personal collection, quiet emotional discovery

## Why Sora First

Sora is the strongest first-slice anchor because:

- she naturally introduces the Prism Effect
- she matches the game's soft, introspective tone
- her Library identity pairs well with the default room theme
- she can support tutorial-style quest writing without feeling mechanical

## First 3 Variants

### 1. Base Variant

- `Name`: Sora Base
- `Scene`: Library atrium, open book, casual clothes
- `Availability`: granted during onboarding or first quest
- `Role`: establishes the character, viewer, and first ownership state

### 2. School Variant

- `Name`: Sora School
- `Scene`: classroom window seat, notebook, uniform
- `Availability`: unlocked through the second quest in the chain
- `Role`: proves progression and multi-variant support

### 3. Rainy Day Variant

- `Name`: Sora Rainy Day
- `Scene`: cafe window, oversized sweater, warm drink
- `Availability`: unlocked through the final slice quest
- `Role`: gives the slice an emotional payoff and a stronger display reward than a purely functional third unlock

## First Room Theme

- `Theme`: Warm Library
- `Why`: fits Sora, reinforces the collectible fantasy, and can be implemented elegantly without complex environmental variety

## Currency Rules

The slice uses one currency only:

- `Coins`

Coins are used lightly in the first slice. They are not the main loop.

### Slice-1 Coin Uses

- optional simple reward feedback
- room visits or progression feedback later if needed
- future-proofing for shop and unlock systems

### Slice-1 Coin Rules

- players cannot buy progress skips in this slice
- players do not need premium currency
- quest rewards may include small coin rewards, but variants are still unlocked directly by story completion

## Quest Arc

The slice should include 4 quests.

### Quest 1: First Light

- `Purpose`: onboarding
- `Player Action`: meet Sora, view first figurine page, enter first room
- `Reward`: Sora Base

### Quest 2: Margin Notes

- `Purpose`: teach interaction and progression
- `Player Action`: revisit Sora, inspect a memory/lore prompt, return to the character page
- `Reward`: Sora School

### Quest 3: Shelf Memory

- `Purpose`: connect collection to room placement
- `Player Action`: place Sora on a shelf and save the arrangement
- `Reward`: coins and progression to next quest

### Quest 4: Quiet Hours

- `Purpose`: emotional payoff and final vertical-slice reward
- `Player Action`: revisit Sora after completing prior tasks, trigger a short final story step
- `Reward`: Sora Rainy Day

## Reduced Data Model List

The first slice should only include the models needed to complete the loop.

### Core Models

- `User`
- `Character`
- `Variant`
- `OwnedVariant`
- `Quest`
- `PlayerQuest`
- `DisplayRoom`
- `ShelfSlot`

### Optional Early Model

- `CoinTransaction`

This should only exist in slice 1 if we decide to expose coins meaningfully. If coins are just a small feedback number at first, we can defer the ledger until Phase 4 implementation.

## Reduced Field Direction

### User

- username
- email if needed
- coins

### Character

- name
- slug
- archetype
- short_description
- lore_quote
- color_hex

### Variant

- character
- name
- slug
- scene_type
- unlock_order
- rarity
- short_description
- model_file_path

### OwnedVariant

- user
- variant
- acquired_at

### Quest

- slug
- title
- description
- quest_order
- reward_variant
- reward_coins
- is_active

### PlayerQuest

- user
- quest
- status
- started_at
- completed_at

### DisplayRoom

- user
- theme_slug
- is_public

### ShelfSlot

- room
- slot_index
- owned_variant

## Explicit Deferrals

The slice does not need:

- full chapter system
- all 10 characters
- premium currency
- fragments/pity system
- social reactions
- gifting
- websocket notifications
- seasonal events
- WebXR
- bond-level complexity

## Phase 1 Exit Condition

Phase 1 is complete when this slice is agreed and implementation can proceed without unresolved scope questions.

