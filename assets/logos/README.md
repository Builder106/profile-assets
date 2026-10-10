# Project and technology artwork

The full table uses original artwork for all twenty projects. Each transparent tile has a thin outline, a 52 px project mark, its name, and a 16 px technology mark beside the technology label. An 18 px Lucide icon in the upper-right corner identifies the track. The table legend pairs each icon with its name.

Original SVG, PNG, and WebP files are copied unchanged from the project repositories or the portfolio’s existing project-logo collection. `sources.json` records their paths, repository URLs, revisions, and SHA-256 hashes. Technology marks come from [Simple Icons](https://github.com/simple-icons/simple-icons), and track icons come from [Lucide](https://github.com/lucide-icons/lucide). Their pinned revisions, source URLs, hashes, and upstream licenses are included here.

The generator embeds artwork as data URLs. Original project colors and proportions remain intact. Technology silhouettes use their upstream colors; black marks use the theme’s foreground color. C99 and Yul retain text labels because this source collection has no dedicated marks for them.

Tiles share one renderer between the full table and the four-project review strip. Neither version uses background fills, colored edge bars, corner numbers, blinking indicators, or repeating motion. The brief entrance fade becomes static when reduced motion is enabled.

Run `python assets/build.py` to regenerate the full table and standalone cells. Run `python assets/gen_logo_study.py` to regenerate the four-project review strip.

## Design decisions

On 2026-10-10, the logo layout replaced the symbol-only table. Transparent interiors replaced the rejected tinted and off-white surfaces. Celestial Sanctum’s technology label was corrected from Swift to TypeScript after checking its Angular source and project journal.
