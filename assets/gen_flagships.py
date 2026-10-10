#!/usr/bin/env python3
"""Generate light and dark flagship project index SVGs.

Presents six flagship builds arranged with clear architecture headlines
and verifiable empirical signals.
"""

import html
import json
import os
from pathlib import Path

from gen_cells import MOTION_CSS, NEUTRAL, disc_accent, disc_text

ASSETS = Path(__file__).parent

PROJECTS_DATA = json.loads((ASSETS / "projects.json").read_text())
FLAGSHIPS = [p for p in PROJECTS_DATA["projects"] if p.get("flagship")]

W, H = 1200, 480


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def svg_text(x, y, text, size=14, fill="#ffffff", weight="400", family="sans", anchor="start", letter_spacing=0):
    font_fam = (
        "ui-monospace, SFMono-Regular, Menlo, monospace"
        if family == "mono"
        else "-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif"
    )
    spacing_attr = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
    anchor_attr = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{font_fam}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}"{anchor_attr}{spacing_attr}>{esc(text)}</text>'
    )


def index_svg(theme: str) -> str:
    neutral = NEUTRAL[theme]
    title = "Six projects that earn a closer look."
    description = "Empirical benchmarks, security primitives, and measured system performance."

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Flagship projects index: {esc(title)}">',
        "  <defs>",
        MOTION_CSS,
        "  </defs>",
        f'  <g data-bg="{neutral["surface"]}">    <rect width="{W}" height="{H}" fill="{neutral["surface"]}"/>',
        "    " + svg_text(52, 44, title, size=22, fill=neutral["fg"], weight="700"),
        "    " + svg_text(52, 68, description, size=13, fill=neutral["muted"]),
        "    " + svg_text(1148, 44, "06", size=22, fill=neutral["fg"], weight="700", family="mono", anchor="end"),
        "    "
        + svg_text(
            1148,
            68,
            "FLAGSHIPS",
            size=11,
            fill=neutral["faded"],
            family="mono",
            anchor="end",
            letter_spacing=1.5,
        ),
        f'    <line x1="52" y1="86" x2="1148" y2="86" stroke="{neutral["rule"]}" stroke-width="1"/>',
    ]

    card_w, card_h = 536, 110
    col_x = [52, 612]
    row_y = [102, 224, 346]

    for idx, p in enumerate(FLAGSHIPS[:6]):
        c = idx % 2
        r = idx // 2
        x = col_x[c]
        y = row_y[r]
        accent = disc_accent(p["track"], theme)
        ink = disc_text(p["track"], theme)

        out.extend(
            [
                f'    <g data-bg="{neutral["surface"]}">'
                f'      <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="6" fill="{neutral["surface"]}" stroke="{neutral["rule"]}" stroke-width="1"/>',
                f'      <rect x="{x}" y="{y}" width="4" height="{card_h}" rx="2" fill="{accent}"/>',
                "      " + svg_text(x + 20, y + 28, p["name"], size=16, fill=neutral["fg"], weight="700"),
                "      "
                + svg_text(
                    x + 190,
                    y + 28,
                    p["stack"],
                    size=11,
                    fill=ink,
                    weight="600",
                    family="mono",
                ),
                "      "
                + svg_text(
                    x + card_w - 20,
                    y + 28,
                    p["signal"],
                    size=15,
                    fill=neutral["fg"],
                    weight="700",
                    family="mono",
                    anchor="end",
                ),
                "      "
                + svg_text(
                    x + card_w - 20,
                    y + 46,
                    p["signal_label"],
                    size=10,
                    fill=neutral["faded"],
                    family="mono",
                    anchor="end",
                ),
                f'      <line x1="{x + 20}" y1="{y + 56}" x2="{x + card_w - 20}" y2="{y + 56}" stroke="{neutral["rule"]}" stroke-width="1" stroke-opacity="0.25"/>',
                "      "
                + svg_text(
                    x + 20,
                    y + 82,
                    p["headline"],
                    size=12,
                    fill=neutral["muted"],
                    weight="400",
                ),
                "    </g>",
            ]
        )

    out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def write_cards(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for theme in ("dark", "light"):
        content = index_svg(theme)
        out_path = Path(out_dir) / f"flagships-{theme}.svg"
        out_path.write_text(content)


def main():
    flagships_dir = ASSETS / "flagships"
    write_cards(flagships_dir)
    print(f"Generated flagships in {flagships_dir}")


if __name__ == "__main__":
    main()
