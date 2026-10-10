#!/usr/bin/env python3
"""Generate per-cell SVGs for the periodic table.

Each cell is a self-contained 130x130 SVG with a transparent background,
so they tile into a continuous-looking grid when laid out in an HTML
<table>. Each cell is wrapped in <a> in the README for click-through.

Usage:
    python3 gen_cells.py svgs            # writes cells/*.svg
    python3 gen_cells.py table > /tmp/t  # prints HTML <table> markup
"""

import base64
import json
import os
import sys
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

# Neutral colors come from palette.json; brand colors come from upstream artwork.
PALETTE = json.loads((Path(__file__).parent / "palette.json").read_text())
NEUTRAL = PALETTE["neutral"]
TRACK = PALETTE["tracks"]

PROJECTS_DATA = json.loads((Path(__file__).parent / "projects.json").read_text())

# Dynamically construct CELLS and REPO_NAME from projects.json
CELLS = []
REPO_NAME = {}
for p in PROJECTS_DATA["projects"]:
    REPO_NAME[p["id"]] = p["repo"]
    if "periodic" in p:
        per = p["periodic"]
        CELLS.append((per["period"], per["slot"], per["num"], per["symbol"], p["lang"], p["id"], p["track"]))

CELLS.sort(key=lambda c: (c[0], c[1]))


SVG = "http://www.w3.org/2000/svg"
FONT = "Arial, Helvetica, sans-serif"
LOGOS = Path(__file__).parent / "logos"
SOURCES = json.loads((LOGOS / "sources.json").read_text())
DISPLAY_NAMES = {p["id"]: p["name"].replace("_", " ") for p in PROJECTS_DATA["projects"]}
DISPLAY_NAMES.update(
    {
        "ocaml_limit": "OCaml Limit",
        "IMC_Prosperity": "IMC Prosperity",
        "celestial_sanctum": "Celestial Sanctum",
        "ascii_arcade": "ASCII Arcade",
    }
)
ET.register_namespace("", SVG)


def embedded_logo(path: Path, colour: str | None = None, attribute: str = "fill") -> str:
    source = path.read_bytes()
    mime = {".svg": "image/svg+xml", ".webp": "image/webp", ".png": "image/png"}[path.suffix]
    if colour is not None:
        root = ET.fromstring(source)
        root.set(attribute, colour)
        source = ET.tostring(root)
    return f"data:{mime};base64," + base64.b64encode(source).decode("ascii")


def category_image(theme, disc, x=104, y=10):
    source = embedded_logo(LOGOS / SOURCES["categories"][disc]["file"], NEUTRAL[theme]["muted"], "stroke")
    return f'<image x="{x}" y="{y}" width="18" height="18" href="{source}" aria-hidden="true"/>'


def disc_label(code):
    return TRACK[code]["label"]


def disc_accent(code, theme):
    return TRACK[code][theme]["accent"]


def disc_tint(code, theme):
    return TRACK[code][theme]["tint"]


def disc_text(code, theme):
    """Label colour for text set on a discipline's card. Darker/lighter than the
    accent so it clears WCAG 2.2 AAA (7:1) against the tint."""
    return TRACK[code][theme]["text"]


# Animation, declared in CSS rather than SMIL so that a reader who has asked
# their OS for reduced motion actually gets a still image (WCAG 2.2.2).
MOTION_CSS = """  <style>
    .cell { animation: reveal 0.55s ease-out both; }
    @keyframes reveal { from { opacity: 0; } to { opacity: 1; } }
    @media (prefers-reduced-motion: reduce) {
      .cell { animation: none; opacity: 1; }
    }
  </style>"""


def cell_svg(theme, num, symbol, lang, project, disc):
    n = NEUTRAL[theme]
    name = escape(DISPLAY_NAMES.get(project, project))
    label = disc_label(disc)
    repo = SOURCES["repositories"].get(project)
    if repo:
        art = embedded_logo(LOGOS / repo["file"])
        mark = f'<image x="39" y="31" width="52" height="52" href="{art}" aria-hidden="true"/>'
    else:
        mark = f'<text x="65" y="72" font-family="{FONT}" font-size="32" fill="{n["fg"]}" text-anchor="middle">{escape(symbol)}</text>'
    tech = SOURCES["technologies"].get(lang)
    if tech:
        colour = n["fg"] if tech["hex"] == "000000" else "#" + tech["hex"]
        art = embedded_logo(LOGOS / tech["file"], colour)
        start = (130 - (22 + len(lang) * 5.5)) / 2
        technology = f'<image x="{start:.1f}" y="109" width="16" height="16" href="{art}" aria-hidden="true"/><text x="{start + 22:.1f}" y="121" font-family="{FONT}" font-size="11" fill="{n["muted"]}">{escape(lang)}</text>'
    else:
        technology = f'<text x="65" y="121" font-family="{FONT}" font-size="11" fill="{n["muted"]}" text-anchor="middle">{escape(lang)}</text>'
    return f'''<svg xmlns="{SVG}" width="130" height="130" viewBox="0 0 130 130" role="img" aria-label="{name}, {escape(lang)}, {label}">
{MOTION_CSS}
  <g class="cell">
    <rect x="0.5" y="0.5" width="129" height="129" rx="2" fill="none" stroke="{n["border"]}" stroke-width="1"/>
    {category_image(theme, disc)}
    {mark}
    <text x="65" y="100" font-family="{FONT}" font-size="12" font-weight="500" fill="{n["fg"]}" text-anchor="middle">{name}</text>
    {technology}
  </g>
</svg>
'''


def write_svgs(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for _, _, num, symbol, lang, project, disc in CELLS:
        for theme in ("dark", "light"):
            path = os.path.join(out_dir, f"{num:02d}-{symbol.lower()}-{theme}.svg")
            with open(path, "w") as f:
                f.write(cell_svg(theme, num, symbol, lang, project, disc))


def print_table():
    by_pos = {(p, s): (num, symbol, project) for p, s, num, symbol, _, project, _ in CELLS}
    print('<table cellspacing="2" cellpadding="0" border="0">')
    # Column header: group numbers
    print("  <tr>")
    print('    <td width="28"></td>')
    for g in range(1, 9):
        print(f'    <td width="132" align="center"><sub><code>{g}</code></sub></td>')
    print("  </tr>")
    for period in range(4):
        print("  <tr>")
        # Row header: period number
        print(f'    <td width="28" align="right" valign="middle"><sub><code>{period + 1}</code></sub></td>')
        for slot in range(8):
            if (period, slot) in by_pos:
                num, symbol, project = by_pos[(period, slot)]
                repo = REPO_NAME.get(project, project)
                stem = f"{num:02d}-{symbol.lower()}"
                url = f"https://github.com/Builder106/{repo}"
                print(
                    f'    <td width="132" align="center"><a href="{url}" title="{project}"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/cells/{stem}-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/cells/{stem}-light.svg"><img alt="{num:02d} {symbol} {project}" src="assets/cells/{stem}-dark.svg" width="130" height="130"></picture></a></td>'
                )
            else:
                print('    <td width="132"></td>')
        print("  </tr>")
    print("</table>")


def unified_svg(theme):
    """Single SVG containing the whole periodic table — visual centerpiece.
    Click-through per cell isn't possible when img-served; flat link list below
    the SVG in the README provides navigation."""
    n = NEUTRAL[theme]
    muted = n["muted"]
    faded = n["faded"]
    chrome_rule = n["rule"]

    W, H = 1200, 768
    MARGIN_L, MARGIN_TOP = 52, 82
    CELL_W, CELL_H = 130, 130
    COL_STRIDE, ROW_STRIDE = 139, 145

    by_pos = {(p, s): (num, symbol, lang, project, disc) for p, s, num, symbol, lang, project, disc in CELLS}

    summary = f"{len(CELLS)} projects | {len({c[4] for c in CELLS})} technologies | {len({c[6] for c in CELLS})} tracks"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="The Elements: {summary}">',
        MOTION_CSS,
        f'  <text x="52" y="28" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="{faded}">{summary}</text>',
        f'  <line x1="52" y1="54" x2="{W - 47}" y2="54" stroke="{chrome_rule}" stroke-width="1"/>',
    ]

    # Group labels (1..8 across the top of cell columns)
    for g in range(8):
        cx = MARGIN_L + g * COL_STRIDE + CELL_W // 2
        out.append(
            f'    <text x="{cx}" y="74" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="500" fill="{muted}" text-anchor="middle">{g + 1}</text>'
        )

    # Period labels (1..4 down the left side)
    for p in range(4):
        cy = MARGIN_TOP + p * ROW_STRIDE + CELL_H // 2 + 5
        out.append(
            f'    <text x="36" y="{cy}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="500" fill="{muted}" text-anchor="end">{p + 1}</text>'
        )

    # Reuse the same artwork and layout for standalone and combined tiles.
    for (p, s), (num, symbol, lang, project, disc) in sorted(by_pos.items()):
        tile = ET.fromstring(cell_svg(theme, num, symbol, lang, project, disc))
        group = tile.find(f"{{{SVG}}}g")
        group.set("transform", f"translate({MARGIN_L + s * COL_STRIDE}, {MARGIN_TOP + p * ROW_STRIDE})")
        group.set("aria-label", tile.get("aria-label"))
        out.append(ET.tostring(group, encoding="unicode"))

    # Legend area
    legend_y = MARGIN_TOP + 4 * ROW_STRIDE + 12
    out.append(
        f'  <line x1="52" y1="{legend_y}" x2="{W - 47}" y2="{legend_y}" stroke="{chrome_rule}" stroke-width="1"/>'
    )
    out.append(
        f'  <text x="52" y="{legend_y + 28}" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="{muted}">Tracks</text>'
    )

    chip_x, chip_y = 52, legend_y + 42
    order = [code for code in TRACK if code in {c[6] for c in CELLS}]
    for code in order:
        name = disc_label(code)
        out.append(f'  <g transform="translate({chip_x}, {chip_y})">')
        out.append(category_image(theme, code, 0, 4))
        out.append(f'    <text x="25" y="17" font-family="{FONT}" font-size="12" fill="{muted}">{name}</text>')
        out.append("  </g>")
        chip_x += 132

    out.append("</svg>")
    return "\n".join(out)


def write_unified():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for theme in ("dark", "light"):
        path = os.path.join(out_dir, f"table-{theme}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(unified_svg(theme))
    print(f"wrote 2 unified table svgs to {out_dir}/", file=sys.stderr)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "svgs"
    base = os.path.dirname(os.path.abspath(__file__))
    if mode == "svgs":
        out = os.path.join(base, "cells")
        write_svgs(out)
        print(f"wrote {len(CELLS) * 2} svgs to {out}/", file=sys.stderr)
    elif mode == "table":
        print_table()
    elif mode == "unified":
        write_unified()
    else:
        print(f"unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)
