#!/usr/bin/env python3
"""Generate the light and dark flagship project index.

The profile README has no stylesheet, so this source produces one responsive
SVG per color scheme. The index is deliberately editorial rather than a set
of dashboard cards: each project gets a small diagram tied to the work and a
single evidence-bearing signal. The README keeps the click-through links as
plain HTML below the image.
"""

import html
from pathlib import Path

from gen_cells import disc_accent, disc_text

W, H = 1200, 760

FLAGSHIPS = (
    {
        "id": "ocaml-limit",
        "project": "ocaml_limit",
        "repo": "https://github.com/Builder106/ocaml-limit",
        "demo": "https://ocaml-lob.vercel.app/",
        "track": "Q",
        "stack": "OCaml / Quant",
        "headline_lines": ("Sub-microsecond matching", "with a live financial dashboard."),
        "signal_label": "matching latency",
        "signal": "under 1 µs",
        "visual": "order-book",
        "alt": "Project index showing ocaml_limit as an OCaml quantitative system with sub-microsecond matching and a live financial dashboard.",
    },
    {
        "id": "linux-bench-hub",
        "project": "LinuxBenchHub",
        "repo": "https://github.com/Builder106/linux-bench-hub",
        "demo": "https://linuxbenchhub.vercel.app/",
        "track": "A",
        "stack": "Rails / Analyst",
        "headline_lines": ("Automated Linux speed tests", "on identical hardware."),
        "signal_label": "test condition",
        "signal": "same hardware",
        "visual": "benchmark",
        "alt": "Project index showing LinuxBenchHub as a Rails analyst system that compares Linux performance with automated speed tests on identical hardware.",
    },
    {
        "id": "med-core",
        "project": "MedCore",
        "repo": "https://github.com/Builder106/med-core",
        "demo": "https://medcore-health.vercel.app",
        "track": "H",
        "stack": "React / HealthTech",
        "headline_lines": ("Digital medical records", "for African clinics."),
        "signal_label": "recognition",
        "signal": "Yale Africa IV",
        "visual": "care",
        "alt": "Project index showing MedCore as a React health technology system for digital medical records in African clinics and a Yale Africa Innovation Symposium IV winner.",
    },
    {
        "id": "datafest-2026",
        "project": "datafest-2026",
        "repo": "https://github.com/Builder106/datafest-2026",
        "demo": "https://datafest-2026.vercel.app/",
        "track": "A",
        "stack": "R / Analyst",
        "headline_lines": ("Transportation and emergency care", "across approximately 1M patients."),
        "signal_label": "observed pattern",
        "signal": "3x more ER visits",
        "visual": "route",
        "alt": "Project index showing datafest-2026 as an R healthcare study of approximately 1 million patients that found unreliable transportation leads to three times more emergency room visits.",
    },
    {
        "id": "clear-hash",
        "project": "ClearHash",
        "repo": "https://github.com/Builder106/clear-hash",
        "demo": "https://clearhash.vercel.app/",
        "track": "Y",
        "stack": "Rust / Cybersec",
        "headline_lines": ("Byte-level security scanning", "before release."),
        "signal_label": "scan target",
        "signal": "tampering + backdoors",
        "visual": "hash",
        "alt": "Project index showing ClearHash as a Rust security scanner that inspects software byte by byte for tampering and malicious backdoors before release.",
    },
    {
        "id": "capitol-alpha",
        "project": "CapitolAlpha",
        "repo": "https://github.com/Builder106/capitol-alpha",
        "demo": "https://capitolalpha.vercel.app/",
        "track": "A",
        "stack": "Python / Analyst",
        "headline_lines": ("16,000+ Congressional trades", "mapped against the broader market."),
        "signal_label": "market edge",
        "signal": "+2.58% / year",
        "visual": "market",
        "alt": "Project index showing CapitolAlpha as a Python financial investigation of more than 16,000 Congressional stock trades, with a 2.58 percent annual market edge.",
    },
)

GROUPS = (
    ("Performance", "Systems under load", ("ocaml-limit", "linux-bench-hub")),
    ("Health and evidence", "Data with human stakes", ("med-core", "datafest-2026")),
    ("Security and markets", "Trust, risk, and signal", ("clear-hash", "capitol-alpha")),
)


def esc(value):
    """Escape text for safe insertion into XML text and attributes."""
    return html.escape(value, quote=True)


def svg_text(x, y, content, *, size, fill, weight="400", family="sans", anchor="start", letter_spacing=None):
    """Return one SVG text element with consistent typography."""
    font_family = (
        "ui-monospace, SFMono-Regular, Menlo, monospace"
        if family == "mono"
        else "-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif"
    )
    spacing = f' letter-spacing="{letter_spacing}"' if letter_spacing is not None else ""
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{font_family}" font-size="{size:g}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{spacing}>{esc(content)}</text>'
    )


def visual(kind, x, y, accent, neutral):
    """Return a small project-specific line illustration."""
    rule = neutral["rule"]
    muted = neutral["muted"]
    if kind == "order-book":
        return f'''<g transform="translate({x:g} {y:g})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <line x1="4" y1="72" x2="110" y2="72" stroke="{rule}" stroke-width="1.5"/>
  <rect x="8" y="24" width="18" height="12" stroke="{accent}" stroke-width="2"/>
  <rect x="32" y="42" width="27" height="12" stroke="{accent}" stroke-width="2"/>
  <rect x="65" y="56" width="37" height="12" stroke="{accent}" stroke-width="2"/>
  <path d="M7 16 C28 18 33 10 51 14 S78 29 106 9" stroke="{muted}" stroke-width="2"/>
  <path d="M101 9h7v7" stroke="{accent}" stroke-width="2"/>
</g>'''
    if kind == "benchmark":
        return f'''<g transform="translate({x:g} {y:g})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <line x1="5" y1="78" x2="110" y2="78" stroke="{rule}" stroke-width="1.5"/>
  <line x1="5" y1="12" x2="5" y2="78" stroke="{rule}" stroke-width="1.5"/>
  <rect x="18" y="47" width="15" height="31" fill="{accent}" stroke="{accent}" stroke-width="2"/>
  <rect x="45" y="31" width="15" height="47" fill="{accent}" opacity="0.72" stroke="{accent}" stroke-width="2"/>
  <rect x="72" y="20" width="15" height="58" fill="{accent}" opacity="0.42" stroke="{accent}" stroke-width="2"/>
  <path d="M13 15h82" stroke="{muted}" stroke-width="1.5" stroke-dasharray="3 5"/>
</g>'''
    if kind == "care":
        return f'''<g transform="translate({x:g} {y:g})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="M6 61h19l8-25 11 39 11-29 9 15h35" stroke="{accent}" stroke-width="2.5"/>
  <path d="M83 22v20M73 32h20" stroke="{muted}" stroke-width="2"/>
  <circle cx="104" cy="61" r="5" stroke="{rule}" stroke-width="1.5"/>
  <line x1="6" y1="78" x2="110" y2="78" stroke="{rule}" stroke-width="1.5"/>
</g>'''
    if kind == "route":
        return f'''<g transform="translate({x:g} {y:g})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 69 C23 20 36 76 54 42 S82 14 105 63" stroke="{accent}" stroke-width="2.5"/>
  <circle cx="8" cy="69" r="5" fill="{neutral["surface"]}" stroke="{accent}" stroke-width="2"/>
  <circle cx="54" cy="42" r="4" fill="{neutral["surface"]}" stroke="{muted}" stroke-width="1.5"/>
  <circle cx="105" cy="63" r="6" fill="{accent}" stroke="{accent}" stroke-width="2"/>
  <path d="M78 20v18M69 29h18" stroke="{muted}" stroke-width="2"/>
</g>'''
    if kind == "hash":
        return f'''<g transform="translate({x:g} {y:g})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="M25 10L15 77M54 10L44 77M5 31h76M1 57h76" stroke="{muted}" stroke-width="1.5"/>
  <rect x="74" y="16" width="25" height="25" stroke="{accent}" stroke-width="2"/>
  <path d="M80 29l5 5 10-12" stroke="{accent}" stroke-width="2.5"/>
  <line x1="88" y1="57" x2="110" y2="57" stroke="{rule}" stroke-width="1.5"/>
</g>'''
    if kind == "market":
        return f'''<g transform="translate({x:g} {y:g})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <line x1="5" y1="78" x2="110" y2="78" stroke="{rule}" stroke-width="1.5"/>
  <rect x="15" y="51" width="12" height="27" fill="{accent}" opacity="0.36" stroke="{accent}" stroke-width="1.5"/>
  <rect x="37" y="39" width="12" height="39" fill="{accent}" opacity="0.56" stroke="{accent}" stroke-width="1.5"/>
  <rect x="59" y="24" width="12" height="54" fill="{accent}" opacity="0.78" stroke="{accent}" stroke-width="1.5"/>
  <path d="M7 63L30 55 49 59 70 36 105 14" stroke="{muted}" stroke-width="2"/>
  <path d="M99 14h8v8" stroke="{accent}" stroke-width="2"/>
</g>'''
    raise ValueError(f"unknown flagship visual: {kind}")


def index_svg(theme):
    """Return the accessible portfolio index for one color scheme."""
    is_dark = theme == "dark"
    neutral = {
        "background": "#12161c" if is_dark else "#f7f4ed",
        "surface": "#181d23" if is_dark else "#f0ece3",
        "fg": "#f0eee8" if is_dark else "#171a1d",
        "muted": "#b7bcc1" if is_dark else "#3d444b",
        "faded": "#a9b0b7" if is_dark else "#444c55",
        "rule": "#8b949e" if is_dark else "#6e7781",
    }
    by_id = {flagship["id"]: flagship for flagship in FLAGSHIPS}
    title = "Six projects, three questions."
    description = "How fast? Who does it serve? What can be trusted?"
    alt = "Six-project index grouped by Performance, Health and evidence, and Security and markets. " + " ".join(
        flagship["alt"] for flagship in FLAGSHIPS
    )
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">',
        f"  <title>{esc(title)} {esc(description)}</title>",
        f'  <g data-bg="{neutral["background"]}">',
        f'    <rect width="{W}" height="{H}" fill="{neutral["background"]}"/>',
        "    " + svg_text(56, 68, title, size=40, fill=neutral["fg"], weight="800"),
        "    " + svg_text(56, 102, description, size=17, fill=neutral["muted"]),
        "    " + svg_text(1144, 63, "06", size=30, fill=neutral["fg"], weight="800", family="mono", anchor="end"),
        "    " + svg_text(1144, 91, "selected builds", size=12, fill=neutral["faded"], family="mono", anchor="end"),
        f'    <line x1="56" y1="132" x2="1144" y2="132" stroke="{neutral["rule"]}" stroke-width="1.5"/>',
    ]

    row_y = 158
    row_h = 176
    project_x = (304, 766)
    visual_x = (632, 1040)
    for group_index, (group_name, group_note, project_ids) in enumerate(GROUPS):
        y = row_y + group_index * row_h
        row_fill = neutral["surface"] if group_index % 2 == 0 else neutral["background"]
        output.extend(
            [
                f'    <g data-bg="{row_fill}">',
                f'      <rect x="40" y="{y}" width="1120" height="160" fill="{row_fill}"/>',
                "      " + svg_text(56, y + 35, group_name, size=20, fill=neutral["fg"], weight="750"),
                "      " + svg_text(56, y + 62, group_note, size=13, fill=neutral["muted"]),
                f'      <line x1="272" y1="{y + 16}" x2="272" y2="{y + 144}" stroke="{neutral["rule"]}" stroke-width="1"/>',
            ]
        )
        for index, project_id in enumerate(project_ids):
            flagship = by_id[project_id]
            x = project_x[index]
            accent = disc_accent(flagship["track"], theme)
            output.extend(
                [
                    "      " + svg_text(x, y + 34, flagship["project"], size=23, fill=neutral["fg"], weight="800"),
                    "      "
                    + svg_text(
                        x,
                        y + 58,
                        flagship["stack"],
                        size=11,
                        fill=disc_text(flagship["track"], theme),
                        weight="700",
                        family="mono",
                        letter_spacing=1.2,
                    ),
                    "      "
                    + svg_text(
                        x,
                        y + 92,
                        flagship["headline_lines"][0],
                        size=14,
                        fill=neutral["muted"],
                        weight="650",
                    ),
                    "      " + svg_text(x, y + 112, flagship["headline_lines"][1], size=14, fill=neutral["muted"]),
                    "      "
                    + svg_text(
                        x,
                        y + 140,
                        flagship["signal_label"],
                        size=10,
                        fill=neutral["faded"],
                        family="mono",
                        letter_spacing=1,
                    ),
                    "      " + svg_text(x, y + 158, flagship["signal"], size=16, fill=neutral["fg"], weight="800"),
                    "      " + visual(flagship["visual"], visual_x[index], y + 45, accent, neutral),
                ]
            )
        output.extend(
            [
                "    </g>",
                f'    <line x1="40" y1="{y + 160}" x2="1160" y2="{y + 160}" stroke="{neutral["rule"]}" stroke-width="1.5"/>',
            ]
        )

    output.extend(["  </g>", "</svg>", ""])
    return "\n".join(output)


def write_cards(out_dir):
    """Write one full-width index for each supported color scheme."""
    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        path = output_dir / f"flagships-{theme}.svg"
        path.write_text(index_svg(theme), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    output = Path(__file__).parent / "flagships"
    write_cards(output)
    print(f"wrote 2 flagship indexes to {output}/")
