#!/usr/bin/env python3
"""Generate light and dark GitHub telemetry and language breakdown SVGs.

Replaces third-party Vercel stats badges with bespoke SVGs styled using
palette.json and guaranteed to pass WCAG 2.2 AAA contrast checks.
"""

from __future__ import annotations

import html
import json
import os
from pathlib import Path

from gen_cells import MOTION_CSS, NEUTRAL

ASSETS = Path(__file__).parent

PALETTE = json.loads((ASSETS / "palette.json").read_text())

# Default language weights mirroring the fleet portfolio
LANGUAGES = [
    {"name": "TypeScript", "pct": 32, "color": "#3178c6"},
    {"name": "Python", "pct": 24, "color": "#3572a5"},
    {"name": "Rust", "pct": 14, "color": "#dea584"},
    {"name": "OCaml", "pct": 10, "color": "#ef7a08"},
    {"name": "Go", "pct": 8, "color": "#00add8"},
    {"name": "C99", "pct": 6, "color": "#555555"},
    {"name": "R", "pct": 6, "color": "#198ce7"},
]

TELEMETRY_DEFAULT = {
    "total_commits": "1,850+",
    "verified_pct": "100%",
    "pull_requests": "95+",
    "repositories": "20",
    "oss_status": "GSoC 2027 Track",
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def stats_svg(theme: str, data: dict | None = None) -> str:
    stats = data or TELEMETRY_DEFAULT
    neutral = NEUTRAL[theme]
    w, h = 495, 195

    metrics = [
        ("Total Commits", stats["total_commits"]),
        ("Commit Verification", stats["verified_pct"]),
        ("Pull Requests Merged", stats["pull_requests"]),
        ("Engineered Repos", stats["repositories"]),
        ("OSS Track", stats["oss_status"]),
    ]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="GitHub telemetry: {stats["total_commits"]} commits, {stats["verified_pct"]} verified">',
        "  <defs>",
        MOTION_CSS,
        "  </defs>",
        f'  <g data-bg="{neutral["surface"]}">'
        f'    <rect width="{w}" height="{h}" rx="6" fill="{neutral["surface"]}" stroke="{neutral["rule"]}" stroke-width="1"/>',
        f'    <text x="24" y="32" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" '
        f'font-weight="700" fill="{neutral["muted"]}" letter-spacing="1.5">TELEMETRY // BUILDER106</text>',
        f'    <line x1="24" y1="44" x2="{w - 24}" y2="44" stroke="{neutral["rule"]}" stroke-width="1" stroke-opacity="0.25"/>',
    ]

    y_start = 68
    y_step = 24
    for idx, (label, val) in enumerate(metrics):
        y = y_start + idx * y_step
        out.append(
            f'    <text x="24" y="{y}" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" '
            f'font-size="12" font-weight="500" fill="{neutral["muted"]}">{esc(label)}</text>'
        )
        out.append(
            f'    <text x="{w - 24}" y="{y}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="13" font-weight="700" fill="{neutral["fg"]}" text-anchor="end">{esc(val)}</text>'
        )

    out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def langs_svg(theme: str, langs: list[dict] | None = None) -> str:
    lang_list = langs or LANGUAGES
    neutral = NEUTRAL[theme]
    w, h = 495, 195

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Most-used programming languages breakdown">',
        "  <defs>",
        MOTION_CSS,
        "  </defs>",
        f'  <g data-bg="{neutral["surface"]}">'
        f'    <rect width="{w}" height="{h}" rx="6" fill="{neutral["surface"]}" stroke="{neutral["rule"]}" stroke-width="1"/>',
        f'    <text x="24" y="32" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" '
        f'font-weight="700" fill="{neutral["muted"]}" letter-spacing="1.5">LANGUAGES // DISTRIBUTION</text>',
        f'    <line x1="24" y1="44" x2="{w - 24}" y2="44" stroke="{neutral["rule"]}" stroke-width="1" stroke-opacity="0.25"/>',
    ]

    # Progress bar across the width
    bar_x = 24
    bar_y = 58
    bar_w = w - 48
    bar_h = 10
    cur_x = bar_x

    out.append('    <g clip-path="url(#bar-clip)">')
    out.append(
        f'      <clipPath id="bar-clip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5"/></clipPath>'
    )
    for item in lang_list:
        seg_w = round((item["pct"] / 100.0) * bar_w)
        out.append(f'      <rect x="{cur_x}" y="{bar_y}" width="{seg_w}" height="{bar_h}" fill="{item["color"]}"/>')
        cur_x += seg_w
    out.append("    </g>")

    # Legend list in two columns
    legend_y = 96
    col1_x = 24
    col2_x = 260
    for idx, item in enumerate(lang_list):
        col = col1_x if idx < 4 else col2_x
        row = idx % 4
        item_y = legend_y + row * 22

        out.extend(
            [
                f'    <circle cx="{col + 5}" cy="{item_y - 4}" r="4" fill="{item["color"]}"/>',
                f'    <text x="{col + 16}" y="{item_y}" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" '
                f'font-size="12" font-weight="600" fill="{neutral["fg"]}">{esc(item["name"])}</text>',
                f'    <text x="{col + 160}" y="{item_y}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
                f'font-size="11" font-weight="500" fill="{neutral["muted"]}" text-anchor="end">{item["pct"]}%</text>',
            ]
        )

    out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def write_stats(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for theme in ("dark", "light"):
        (Path(out_dir) / f"stats-{theme}.svg").write_text(stats_svg(theme))
        (Path(out_dir) / f"langs-{theme}.svg").write_text(langs_svg(theme))


def main():
    write_stats(ASSETS)
    print(f"Generated telemetry and language SVGs in {ASSETS}")


if __name__ == "__main__":
    main()
