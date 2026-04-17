from __future__ import annotations

import json
import pathlib
import re
import struct
from dataclasses import dataclass

from django.conf import settings
from django.utils.text import slugify

from .models import Variant, VariantAssetProfile


SAFE_HIDE_KEYWORDS = (
    "shoe",
    "sock",
    "boot",
    "bag",
    "purse",
    "hat",
    "cap",
    "glass",
    "glasses",
    "ribbon",
    "tie",
    "scarf",
    "accessory",
)


@dataclass(frozen=True)
class GlbSummary:
    parts_schema: list[dict]
    morph_schema: list[dict]
    animation_schema: list[dict]


def _make_unique_id(raw_name: str, used_ids: set[str]) -> str:
    base_id = slugify(raw_name) or "item"
    candidate = base_id
    suffix = 2
    while candidate in used_ids:
        candidate = f"{base_id}-{suffix}"
        suffix += 1
    used_ids.add(candidate)
    return candidate


def _humanize_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", str(name).replace("_", " ").replace("-", " ")).strip()
    return re.sub(r"\b\w", lambda match: match.group(0).upper(), cleaned) if cleaned else str(name)


def _guess_part_category(name: str) -> str:
    lowered = name.lower()
    if any(keyword in lowered for keyword in ("shoe", "sock", "boot")):
        return "footwear"
    if any(keyword in lowered for keyword in ("bag", "purse", "hat", "cap", "glass", "glasses", "ribbon", "tie", "scarf", "accessory")):
        return "accessory"
    if any(keyword in lowered for keyword in ("hair",)):
        return "hair"
    if any(keyword in lowered for keyword in ("eye", "brow", "mouth", "face", "head")):
        return "face"
    if any(keyword in lowered for keyword in ("shirt", "skirt", "pant", "body", "sock")):
        return "clothing"
    return "other"


def _guess_morph_group(name: str) -> str:
    lowered = name.lower()
    if "blink" in lowered or "eye" in lowered:
        return "eyes"
    if "mouth" in lowered or "lip" in lowered:
        return "mouth"
    if "brow" in lowered:
        return "brows"
    if "hair" in lowered:
        return "hair_pose"
    if "foot" in lowered:
        return "body_fix"
    return "other"


def _is_safe_hide(name: str) -> bool:
    lowered = name.lower()
    return any(keyword in lowered for keyword in SAFE_HIDE_KEYWORDS)


def _load_glb_json(model_relative_path: str) -> dict:
    model_path = pathlib.Path(settings.BASE_DIR) / "static" / model_relative_path
    data = model_path.read_bytes()
    if data[:4] != b"glTF":
        raise ValueError(f"{model_path} is not a valid GLB file.")

    offset = 12
    json_chunk = None
    while offset < len(data):
        chunk_len, chunk_type = struct.unpack_from("<I4s", data, offset)
        offset += 8
        chunk_data = data[offset : offset + chunk_len]
        offset += chunk_len
        if chunk_type == b"JSON":
            json_chunk = json.loads(chunk_data.decode("utf-8"))
            break

    if json_chunk is None:
        raise ValueError(f"No JSON chunk found in {model_relative_path}.")
    return json_chunk


def build_glb_summary(model_relative_path: str) -> GlbSummary:
    gltf = _load_glb_json(model_relative_path)
    nodes = gltf.get("nodes", [])
    meshes = gltf.get("meshes", [])
    materials = gltf.get("materials", [])
    animations = gltf.get("animations", [])

    material_names = [material.get("name") or f"material_{index}" for index, material in enumerate(materials)]

    used_part_ids: set[str] = set()
    parts_schema: list[dict] = []
    for node_index, node in enumerate(nodes):
        mesh_index = node.get("mesh")
        if mesh_index is None or mesh_index >= len(meshes):
            continue

        raw_name = node.get("name") or f"node_{node_index}"
        mesh = meshes[mesh_index]
        mesh_name = mesh.get("name") or f"mesh_{mesh_index}"
        primitive_material_names = []
        for primitive in mesh.get("primitives", []):
            material_index = primitive.get("material")
            if material_index is None or material_index >= len(material_names):
                continue
            primitive_material_names.append(material_names[material_index])

        parts_schema.append(
            {
                "id": _make_unique_id(raw_name, used_part_ids),
                "label": _humanize_name(raw_name),
                "raw_name": raw_name,
                "mesh_name": mesh_name,
                "material_names": primitive_material_names,
                "category": _guess_part_category(raw_name),
                "default_visible": True,
                "editable": True,
                "safe_hide": _is_safe_hide(raw_name),
            }
        )

    morph_map: dict[str, dict] = {}
    used_morph_ids: set[str] = set()
    for mesh_index, mesh in enumerate(meshes):
        mesh_name = mesh.get("name") or f"mesh_{mesh_index}"
        target_names = mesh.get("extras", {}).get("targetNames") or mesh.get("targetNames") or []
        for target_name in target_names:
            key = str(target_name)
            if key not in morph_map:
                morph_map[key] = {
                    "id": _make_unique_id(key, used_morph_ids),
                    "label": _humanize_name(key),
                    "raw_name": key,
                    "group": _guess_morph_group(key),
                    "default_value": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "editable": True,
                    "source_meshes": [],
                }
            morph_map[key]["source_meshes"].append(mesh_name)

    used_animation_ids: set[str] = set()
    animation_schema = [
        {
            "id": _make_unique_id(animation.get("name") or f"animation_{index}", used_animation_ids),
            "label": _humanize_name(animation.get("name") or f"Animation {index + 1}"),
            "clip_name": animation.get("name") or f"animation_{index}",
            "editable": True,
        }
        for index, animation in enumerate(animations)
    ]

    return GlbSummary(
        parts_schema=parts_schema,
        morph_schema=sorted(morph_map.values(), key=lambda item: item["label"].lower()),
        animation_schema=animation_schema,
    )


def build_variant_asset_profile(variant: Variant) -> VariantAssetProfile:
    summary = build_glb_summary(variant.model_file_path)
    profile, _ = VariantAssetProfile.objects.update_or_create(
        variant=variant,
        defaults={
            "parts_schema": summary.parts_schema,
            "morph_schema": summary.morph_schema,
            "animation_schema": summary.animation_schema,
        },
    )
    return profile
