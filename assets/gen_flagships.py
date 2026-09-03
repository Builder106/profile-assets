#!/usr/bin/env python3
"""Generate the light and dark flagship project cards.

The cards are deliberately image-based because GitHub profile READMEs do not
provide a stylesheet or a reliable responsive grid. The README supplies the
click-through links around each generated card.
"""

import html
from pathlib import Path

from gen_cells import disc_accent, disc_label, disc_text, disc_tint

W, H = 480, 280

FLAGSHIPS = (
    {
        "id": "ocaml-limit",
        "project": "ocaml_limit",
        "repo": "https://github.com/Builder106/ocaml-limit",
        "demo": "https://ocaml-lob.vercel.app/",
        "track": "Q",
        "stack": "OCaml",
        "monogram": "OC",
        "headline": "Sub-microsecond order matching",
        "detail_lines": ("High-speed trading engine with a live financial", "dashboard."),
        "signal_label": "MATCHING LATENCY",
        "signal": "UNDER 1 MICROSECOND",
        "alt": "ocaml_limit flagship card: Quant project in OCaml, a high-speed stock trading engine with a live financial dashboard and sub-microsecond matching.",
    },
    {
        "id": "med-core",
        "project": "MedCore",
        "repo": "https://github.com/Builder106/med-core",
        "demo": "https://medcore-health.vercel.app",
        "track": "H",
        "stack": "React",
        "monogram": "MC",
        "headline": "AI-assisted medical records",
        "detail_lines": ("Digital records platform built for African", "clinics."),
        "signal_label": "RECOGNITION",
        "signal": "YALE AFRICA IV WINNER",
        "alt": "MedCore flagship card: HealthTech project in React, an AI-assisted digital medical records platform for African clinics and winner of the Yale Africa Innovation Symposium IV.",
    },
    {
        "id": "clear-hash",
        "project": "ClearHash",
        "repo": "https://github.com/Builder106/clear-hash",
        "demo": "https://clearhash.vercel.app/",
        "track": "Y",
        "stack": "Rust",
        "monogram": "#H",
        "headline": "Byte-level security scanning",
        "detail_lines": ("Catches tampering and malicious backdoors", "before release."),
        "signal_label": "SCAN TARGET",
        "signal": "TAMPERING AND BACKDOORS",
        "alt": "ClearHash flagship card: Cybersec project in Rust, a byte-level software security scanner that catches tampering and malicious backdoors before release.",
    },
    {
        "id": "capitol-alpha",
        "project": "CapitolAlpha",
        "repo": "https://github.com/Builder106/capitol-alpha",
        "demo": "https://capitolalpha.vercel.app/",
        "track": "A",
        "stack": "Python",
        "monogram": "CA",
        "headline": "16,000+ Congressional trades",
        "detail_lines": ("Financial investigation mapped against the", "broader market."),
        "signal_label": "MARKET EDGE",
        "signal": "+2.58% ANNUALLY",
        "alt": "CapitolAlpha flagship card: Analyst project in Python analyzing more than 16,000 Congressional stock trades from 2020 to 2024, with a 2.58 percent annual market edge.",
    },
    {
        "id": "datafest-2026",
        "project": "datafest-2026",
        "repo": "https://github.com/Builder106/datafest-2026",
        "demo": "https://datafest-2026.vercel.app/",
        "track": "A",
        "stack": "R",
        "monogram": "DF",
        "headline": "Transportation and emergency care",
        "detail_lines": ("Healthcare study spanning approximately", "1M patients."),
        "signal_label": "OBSERVED PATTERN",
        "signal": "3X MORE ER VISITS",
        "alt": "datafest-2026 flagship card: Analyst project in R studying approximately 1 million patients and finding that unreliable transportation leads to three times more emergency room visits.",
    },
    {
        "id": "linux-bench-hub",
        "project": "LinuxBenchHub",
        "repo": "https://github.com/Builder106/linux-bench-hub",
        "demo": "https://linuxbenchhub.vercel.app/",
        "track": "A",
        "stack": "Rails",
        "monogram": "LB",
        "headline": "Linux performance lab",
        "detail_lines": ("Automated speed tests comparing systems", "on identical hardware."),
        "signal_label": "TEST BED",
        "signal": "IDENTICAL HARDWARE",
        "alt": "LinuxBenchHub flagship card: Analyst project in Rails comparing major Linux systems side by side with automated speed tests on identical hardware.",
    },
)


def esc(value):
    """Escape text for safe insertion into XML text and attributes."""
    return html.escape(value, quote=True)


def card_svg(theme, flagship):
    """Return one accessible flagship card SVG."""
    is_dark = theme == "dark"
    surface = "#161b22" if is_dark else "#f6f8fa"
    dots = "#1f2630" if is_dark else "#d0d7de"
    fg = "#e6edf3" if is_dark else "#1f2328"
    muted = "#d5d8db" if is_dark else "#34383c"
    faded = "#c1c5ca" if is_dark else "#3e444a"
    border = "#7d8590" if is_dark else "#656d76"
    accent = disc_accent(flagship["track"], theme)
    tint = disc_tint(flagship["track"], theme)
    track_ink = disc_text(flagship["track"], theme)
    track_label = disc_label(flagship["track"])
    number = next(index for index, item in enumerate(FLAGSHIPS, start=1) if item["id"] == flagship["id"])
    pill_width = 18 + len(track_label) * 7
    pill_x = W - 26 - pill_width
    detail_svg = "\n".join(
        f'    <text x="122" y="{174 + offset * 18}" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" font-size="13" fill="{faded}">{esc(line)}</text>'
        for offset, line in enumerate(flagship["detail_lines"])
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(flagship["alt"])}">
  <g data-bg="{surface}">
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{surface}" stroke="{border}" stroke-width="2"/>
    <g fill="{dots}" opacity="0.55">
      <circle cx="28" cy="58" r="1"/><circle cx="46" cy="58" r="1"/><circle cx="64" cy="58" r="1"/><circle cx="82" cy="58" r="1"/>
      <circle cx="28" cy="76" r="1"/><circle cx="46" cy="76" r="1"/><circle cx="64" cy="76" r="1"/><circle cx="82" cy="76" r="1"/>
      <circle cx="398" cy="58" r="1"/><circle cx="416" cy="58" r="1"/><circle cx="434" cy="58" r="1"/>
      <circle cx="398" cy="76" r="1"/><circle cx="416" cy="76" r="1"/><circle cx="434" cy="76" r="1"/>
    </g>
    <rect x="2" y="2" width="{W - 4}" height="6" rx="3" fill="{accent}"/>

    <text x="26" y="36" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" font-weight="600" letter-spacing="2" fill="{faded}">FLAGSHIP {number:02d}</text>
    <g data-bg="{tint}">
      <rect x="{pill_x}" y="19" width="{pill_width}" height="24" rx="12" fill="{tint}"/>
      <text x="{pill_x + pill_width / 2:g}" y="35" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" font-size="12" font-weight="700" fill="{track_ink}" text-anchor="middle">{esc(track_label)}</text>
    </g>

    <rect x="26" y="78" width="72" height="72" rx="12" fill="{tint}" stroke="{accent}" stroke-width="2"/>
    <text x="62" y="124" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" font-size="27" font-weight="800" letter-spacing="-1" fill="{track_ink}" text-anchor="middle">{esc(flagship["monogram"])}</text>

    <text x="122" y="91" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" font-size="23" font-weight="750" fill="{fg}">{esc(flagship["project"])}</text>
    <text x="122" y="116" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" font-weight="600" letter-spacing="1.5" fill="{track_ink}">{esc(flagship["stack"].upper())}  /  {esc(track_label.upper())}</text>
    <text x="122" y="151" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" font-size="15" font-weight="700" fill="{muted}">{esc(flagship["headline"])}</text>
{detail_svg}

    <line x1="26" y1="211" x2="454" y2="211" stroke="{border}" stroke-width="1" opacity="0.65"/>
    <text x="26" y="235" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10" font-weight="600" letter-spacing="1.4" fill="{faded}">{esc(flagship["signal_label"])}</text>
    <text x="26" y="263" font-family="-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif" font-size="15" font-weight="800" fill="{track_ink}">{esc(flagship["signal"])}</text>
    <text x="454" y="263" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10" font-weight="600" letter-spacing="1.2" fill="{faded}" text-anchor="end">OPEN REPOSITORY</text>
  </g>
</svg>
'''


def write_cards(out_dir):
    """Write both theme variants for every flagship."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for flagship in FLAGSHIPS:
        for theme in ("dark", "light"):
            path = Path(out_dir) / f"{flagship['id']}-{theme}.svg"
            path.write_text(card_svg(theme, flagship), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    output = Path(__file__).parent / "flagships"
    write_cards(output)
    print(f"wrote {len(FLAGSHIPS) * 2} flagship cards to {output}/")
