# Lab Asset Profile Report

## Purpose

This report documents what the current Mirageland GLB assets actually expose for editing and recommends a safer customization architecture for the lab, character page, and display room.

The goal is to move away from fragile live mesh-name saving and toward:

- immutable asset defaults per variant
- player-owned override state
- safe reset behavior
- support for future uploaded personal assets

## Executive Summary

The current assets are not uniform.

- `Base` variants are the richest assets and are the best candidates for the first real lab workflow.
- `School` variants are partial assets with fewer meshes and almost no morph support.
- `Rainy Day` variants are extremely reduced exports and should be treated as limited-display assets unless replaced later.

The most important finding is this:

- the data needed for a stable lab exists inside the GLBs
- but it varies per model
- and it should be captured into an immutable per-variant asset profile before player edits are applied

That means the right long-term system is:

1. scan a variant model and generate a `VariantAssetProfile`
2. store the default editable schema there
3. store player edits only as overrides
4. build runtime state from `profile defaults + player overrides`
5. reset by deleting overrides, never by mutating defaults

## Current Model Findings

### Sora

#### `sora/base/sora-base-v1.glb`

- Meshes: `10`
- Nodes: `81`
- Materials: `3`
- Animations: `1`
- Material names:
  - `Skin`
  - `Student cloth`
  - `Hair`
- Interesting node names:
  - `Foot fixed`
  - `panties`
  - `shirt`
  - `shoe`
  - `skirt`
  - `socks`
  - `tie`
  - `Hair`
- Morph targets on `Character`:
  - `Foot fixed`
  - `Blink`
  - `Left Blink`
  - `Right Blink`
  - `Mouth Open`
  - `Eyebrow Raise`
  - `Left Eyebrow Raise`
  - `Right Eyebrow Raise`
  - `Mouth Angry/Sad`
  - `Pretty plz`
  - `Eyebrow Brave`
  - `Right Eyebrow Brave`
  - `Left Eyebrow Brave`
  - `Mouth - pout`
  - `Mouth - expanded`
  - `Eyes:Left`
  - `Eyes:Right`
  - `Eyes:Up`
  - `Eyes:Down`
- Animation clips:
  - `KeyAction.001`

Assessment:
- strong first-class lab asset
- good morph support
- meaningful hide/show candidates from node names
- animation exists, but naming needs cleanup

#### `sora/school/sora-school-v1.glb`

- Meshes: `6`
- Nodes: `77`
- Materials: `1`
- Animations: `0`
- Interesting node names:
  - `panties`
  - `shirt`
  - `shoe`
  - `skirt`
  - `socks`
  - `tie`
- Morph targets: none

Assessment:
- usable for part toggles
- no expression layer
- likely should inherit a reduced lab capability set

#### `sora/rainy-day/sora-rainy-day-v1.glb`

- Meshes: `2`
- Nodes: `73`
- Materials: `1`
- Animations: `0`
- Interesting node names:
  - `panties`
  - `tie`
- Morph targets: none

Assessment:
- highly limited export
- not suitable for rich customization
- should probably expose only render mode and maybe no parts at all

### Ren

#### `ren/base/ren-base-v1.glb`

- Meshes: `10`
- Nodes: `72`
- Materials: `4`
- Animations: `0`
- Material names:
  - `Skin`
  - `Hair Red`
  - `Student cloth`
  - `Student cloth.001`
- Interesting node names:
  - `Body`
  - `Hair`
  - `panties`
  - `shirt`
  - `shoe`
  - `skirt`
  - `socks`
  - `tie`
- Morph targets:
  - on `Cube`
    - `Blink`
    - `R Blink`
    - `L Blink`
    - `Mouth Open`
    - `Key 15`
    - `Mouth Angry/Sad`
    - `Mouth - pout`
    - `Mouth - expanded`
    - `Pretty plz`
    - `Eyebrow Brave`
    - `R Eyebrow Brave`
    - `L Eyebrow Brave`
    - `Eyebrow Raise`
    - `L Eyebrow Raise`
    - `R Eyebrow Raise`
    - `Eyes:Left`
    - `Eyes:Right`
    - `Eyes:Up`
    - `Eyes:Down`
  - on `Cylinder.009`
    - `Key 1`
  - on `Cube.001`
    - `Key 1`

Assessment:
- strong lab asset
- morph support is good but naming is noisier than Sora
- some morphs like `Key 1` and `Key 15` should be hidden or relabeled

#### `ren/school/ren-school-v1.glb`

- Meshes: `6`
- Nodes: `68`
- Materials: `2`
- Animations: `0`
- Interesting node names:
  - `panties`
  - `shirt`
  - `shoe`
  - `skirt`
  - `socks`
  - `tie`
- Morph targets:
  - on `Cylinder.009`
    - `Key 1`

Assessment:
- usable for parts
- morph support is too weak/noisy for player-facing sliders unless curated

#### `ren/rainy-day/ren-rainy-day-v1.glb`

- Meshes: `2`
- Nodes: `64`
- Materials: `1`
- Animations: `0`
- Interesting node names:
  - `panties`
  - `tie`
- Morph targets: none

Assessment:
- same limitation pattern as Sora rainy-day

### Mei

#### `mei/base/mei-base-v1.glb`

- Meshes: `11`
- Nodes: `73`
- Materials: `4`
- Animations: `3`
- Material names:
  - `Skin`
  - `Unhas`
  - `Student cloth`
  - `Hair Loiro Texture`
- Interesting node names:
  - `Body`
  - `panties`
  - `shirt`
  - `shoe`
  - `skirt`
  - `socks`
  - `tie`
  - `Hair`
- Morph targets:
  - on `Cube.003`
    - `Blink`
    - `R Blink`
    - `L Blink`
    - `Mouth: Smile`
    - `Mouth: Contract`
    - `Mouth: Expand`
    - `Mouth: Bad`
    - `Mouth:Smile 2`
    - `Eyebrows Up`
    - `Eyebrows Down`
    - `Pretty plz`
    - `R eyebrow up`
    - `L eyebrow up`
    - `L eyebrow down`
    - `R eyeborw down`
    - `Eyes:Left`
    - `Eyes:Right`
    - `Eyes:Up`
    - `Eyes:Down`
  - on `Cube.002`
    - `Lip: Smile`
    - `LIP: Open`
    - `Eyes:Right Blink`
    - `Eyes: Semi openned`
    - `LIP: bad mood`
    - `Eyes:Close`
  - on `Sphere.005`
    - `Hair pose 1`
- Animation clips:
  - `shirtAction`
  - `Cylinder.011Action`
  - `TeethAction`

Assessment:
- richest current asset
- very strong candidate for the full lab pipeline
- especially useful for testing grouped morph UI and future pose support

#### `mei/school/mei-school-v1.glb`

- Meshes: `6`
- Nodes: `68`
- Materials: `1`
- Animations: `2`
- Interesting node names:
  - `panties`
  - `shirt`
  - `shoe`
  - `skirt`
  - `socks`
  - `tie`
- Morph targets: none
- Animation clips:
  - `shirtAction`
  - `Cylinder.011Action`

Assessment:
- parts plus possible animation inspection
- no expression layer

#### `mei/rainy-day/mei-rainy-day-v1.glb`

- Meshes: `2`
- Nodes: `64`
- Materials: `1`
- Animations: `1`
- Interesting node names:
  - `panties`
  - `tie`
- Morph targets: none
- Animation clips:
  - `Cylinder.011Action`

Assessment:
- still very limited
- not good for broad customization

## Cross-Asset Conclusions

### 1. Node names are more useful than mesh names

The mesh names are often generic:

- `Cube.003`
- `Cylinder.011`
- `Plane.006`

The node names are much more usable:

- `shoe`
- `socks`
- `tie`
- `Hair`
- `shirt`
- `skirt`
- `Body`

Recommendation:
- generate editable parts from node names first
- treat raw mesh names as internal implementation detail

### 2. Base variants should be the primary lab targets

Base variants consistently provide:

- more materials
- more morphs
- more complete body/face structure
- better long-term customization value

Recommendation:
- make base variants the reference set for the full lab
- let school/rainy-day variants expose reduced controls when needed

### 3. Rainy-day variants are not ready for rich customization

The rainy-day exports are only showing a tiny subset of the full asset.

Recommendation:
- for now, rainy-day variants should probably expose:
  - render mode
  - maybe animation if present
  - possibly no parts or only a very limited set
- do not force every variant into the same lab capability surface

### 4. Morph naming is inconsistent

Examples:

- `Blink`
- `R Blink`
- `Left Blink`
- `Eyes:Close`
- `Mouth Open`
- `Mouth: Smile`
- `Mouth - expanded`
- `Key 1`
- `Key 15`

Recommendation:
- build morph profiles with:
  - stable id
  - raw source name(s)
  - player label
  - group
  - visibility flag

### 5. Animation names are not player-safe yet

Examples:

- `shirtAction`
- `Cylinder.011Action`
- `TeethAction`
- `KeyAction.001`

Recommendation:
- expose animation clips in an inspector now
- later map them to player-facing labels or treat some as pose sources

## What Is Editable Right Now

### Safe now

- render mode
- part visibility for meaningful node names
- morph sliders where targets exist
- animation clip preview where clips exist

### Possible later

- active animation / idle pose selection
- saved expression presets
- material tint / color modulation
- local transform offsets for optional accessories or props
- user-uploaded personal background or asset support

### Risky right now

- hiding core body parts
- exposing every raw mesh name directly without context
- saving raw mesh-name state as the long-term source of truth
- assuming all variants support the same controls

## Recommended Architecture

### A. Immutable asset definition per variant

Create a new model:

- `VariantAssetProfile`

Suggested fields:

- `variant` (`OneToOne`)
- `asset_version`
- `parts_schema` (`JSONField`)
- `morph_schema` (`JSONField`)
- `animation_schema` (`JSONField`)
- `generated_at`

This profile stores the default, never-mutated asset definition.

Example `parts_schema`:

```json
[
  {
    "id": "shoe",
    "label": "Shoes",
    "source_nodes": ["shoe"],
    "category": "accessory",
    "default_visible": true,
    "editable": true,
    "safe_hide": true
  },
  {
    "id": "hair",
    "label": "Hair",
    "source_nodes": ["Hair"],
    "category": "body",
    "default_visible": true,
    "editable": false,
    "safe_hide": false
  }
]
```

Example `morph_schema`:

```json
[
  {
    "id": "blink",
    "label": "Blink",
    "group": "eyes",
    "targets": ["Blink", "Left Blink", "Right Blink"],
    "default_value": 0.0,
    "min": 0.0,
    "max": 1.0,
    "editable": true
  },
  {
    "id": "mouth_open",
    "label": "Mouth Open",
    "group": "mouth",
    "targets": ["Mouth Open", "LIP: Open "],
    "default_value": 0.0,
    "min": 0.0,
    "max": 1.0,
    "editable": true
  }
]
```

Example `animation_schema`:

```json
[
  {
    "id": "idle_01",
    "label": "Idle 01",
    "clip_name": "KeyAction.001",
    "editable": true
  }
]
```

### B. Mutable player override state

Keep `OwnedVariantCustomization`, but redefine it as only an override layer:

- `render_mode`
- `hidden_parts` -> list of `part ids`
- `morph_values` -> dict keyed by `morph ids`
- later:
  - `active_animation`
  - `part_transforms`
  - `tint_overrides`

Important:
- do not store raw mesh names as the player contract
- store stable logical ids from `VariantAssetProfile`

### C. Runtime loading flow

For lab, character page, and display room:

1. load `VariantAssetProfile`
2. build default runtime state from the profile
3. load `OwnedVariantCustomization`
4. validate overrides against the profile
5. merge overrides onto the default runtime state
6. apply the merged result to the loaded model

### D. Reset behavior

Reset should do this:

- delete or clear `OwnedVariantCustomization`
- do not mutate the profile
- on next load, rebuild from profile defaults

This is the safest possible reset.

## Lab UI Recommendation

### Viewer

Keep:

- one active figurine
- large single viewer
- compact top identity row

### Right rail

Use four control sections:

1. `Render`
2. `Parts`
3. `Morphs`
4. `Animations / Poses`

### Parts panel behavior

Support two display modes:

1. friendly labels when the profile has them
2. raw fallback names when the asset is messy

That means if the asset contains `chu3`, show it exactly as `chu3` until a better label is curated.

This is important because:

- players can experiment
- uploaded personal assets may have arbitrary names
- the system remains useful even without clean naming

### Morph panel behavior

Group morphs by category:

- `Eyes`
- `Mouth`
- `Brows`
- `Hair / Pose`
- `Other`

Unknown morphs like `Key 1` should go into `Other` unless curated later.

### Animation panel behavior

For now:

- list detected clips
- allow preview

Later:

- mark some clips as `pose-capable`
- allow a player to save an active clip or frame as a display state

## Future User Upload Support

This architecture also scales to personal uploads.

Recommended future models:

- `UserAsset`
- `UserAssetProfile`
- `UserAssetCustomization`

Same pattern:

- profile is generated from the uploaded model
- player state is stored separately
- reset deletes player overrides only

This avoids hard-coding Mirageland-specific naming into the core system.

## What I Recommend Building Next

### Phase 16A: Asset Profile Foundation

- add `VariantAssetProfile`
- generate profile data from each current variant
- store:
  - parts
  - morphs
  - animations
  - default visibility
  - default morph values

### Phase 16B: Runtime Merge Layer

- stop using raw discovered mesh names as the saved-state contract
- load `profile defaults + player overrides`
- validate hidden parts and morph values against the profile

### Phase 16C: Reset Rewrite

- keep reset as delete-override only
- rebuild viewer state from the profile

### Phase 16D: Lab Controls Over Profile

- show profile-approved parts
- show profile-approved morphs
- show raw fallback names if no curated label exists
- keep unknown controls editable if they are not dangerous

### Phase 16E: Animation / Pose Layer

- allow clip preview now
- prepare a path for future pose saving

## Final Recommendation

The best long-term solution is:

- immutable `VariantAssetProfile` per variant
- mutable `OwnedVariantCustomization` as an override layer
- runtime merge on load
- reset by deleting overrides

This is better than hard-coded part lists because:

- it works with inconsistent legacy assets
- it works with future clean naming conventions
- it works with user-uploaded personal assets
- it gives us a safe foundation for parts, morphs, animations, and later transforms/tints

## Immediate Product Recommendation

Start by implementing the asset-profile layer for:

- `Sora Base`
- `Ren Base`
- `Mei Base`

Use those as the first gold-standard lab assets.

Then allow:

- raw fallback part names when needed
- morph grouping with sensible defaults
- animation inspection

That gives Mirageland a robust lab system without waiting for perfect final models.
