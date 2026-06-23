"""
load_tokens.py — Helper to load Avvale brand design tokens.

This skill is a *design system*: it does not create deliverables. Use this
helper from another skill (pptx, docx, xlsx, pdf, …) to pull the Avvale
tokens you need (palette, fonts, asset paths) and apply them at production
time.

Typical usage from another skill:

    from pathlib import Path
    import sys
    AVVALE = Path("<path-to>/avvale-brand")
    sys.path.insert(0, str(AVVALE / "scripts"))
    from load_tokens import load_tokens, rgb_tuple, asset_path

    tokens = load_tokens(AVVALE)
    celadon_rgb = rgb_tuple(tokens["color"]["primary"]["celadon_green"])
    logo_pos    = asset_path(AVVALE, tokens["logo"]["paths"]["horizontal_positive"])
    body_font   = tokens["typography"]["primary_family"]   # "Archivo"
    fallbacks   = tokens["typography"]["fallback_chain"]

The helper does only three things — load the JSON, convert HEX to RGB tuples,
resolve asset paths — so callers can stay focused on producing the document.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_tokens(skill_root: str | Path) -> dict[str, Any]:
    """Load tokens.json from the avvale-brand skill root."""
    root = Path(skill_root)
    tokens_file = root / "tokens.json"
    if not tokens_file.exists():
        raise FileNotFoundError(f"tokens.json not found at {tokens_file}")
    with tokens_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def rgb_tuple(color_token: dict | str) -> tuple[int, int, int]:
    """Return an (r, g, b) tuple from a color token (dict with 'rgb'/'hex')
    or directly from a HEX string like '#248B7E'."""
    if isinstance(color_token, str):
        s = color_token.lstrip("#")
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    if "rgb" in color_token:
        r, g, b = color_token["rgb"]
        return (int(r), int(g), int(b))
    if "hex" in color_token:
        return rgb_tuple(color_token["hex"])
    raise ValueError(f"Color token has no 'rgb' or 'hex' field: {color_token!r}")


def asset_path(skill_root: str | Path, relative: str) -> Path:
    """Resolve an asset path (relative to the skill root) to an absolute Path.
    Raises FileNotFoundError if the asset is missing."""
    root = Path(skill_root)
    p = root / relative
    if not p.exists():
        raise FileNotFoundError(f"Brand asset not found: {p}")
    return p


def chart_palette(tokens: dict[str, Any]) -> list[tuple[int, int, int]]:
    """Return the recommended chart series order as RGB tuples."""
    hexes = tokens["color"]["chart_series_order"]
    return [rgb_tuple(h) for h in hexes]


def font_stack(tokens: dict[str, Any]) -> list[str]:
    """Return the font family + fallback chain, primary first."""
    typo = tokens["typography"]
    return [typo["primary_family"]] + list(typo.get("fallback_chain", []))


if __name__ == "__main__":
    # Smoke test: print the loaded tokens summary.
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", help="Path to avvale-brand directory")
    args = parser.parse_args()
    tokens = load_tokens(args.skill_root)
    print(f"Brand: {tokens['brand']['name']}")
    print(f"Font stack: {', '.join(font_stack(tokens))}")
    print(f"Signature color: {tokens['color']['primary']['celadon_green']['hex']}")
    print(f"Chart palette: {tokens['color']['chart_series_order']}")
