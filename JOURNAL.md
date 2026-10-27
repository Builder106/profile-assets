# Journal

## 2026-10-27: Check generated SVGs in CI #ci #decision

CI runs `python assets/build.py` and compares generated SVGs with tracked files. A mismatch now fails the asset job.

## 2026-10-26: Match the project grid to the portfolio #decision

The grid still showed enclave and helm, whose portfolio racks went to TCG CABT Lab and VGC Rulebreak on 2026-10-25, so those two cards take slots 17 and 18. IMC Prosperity now shows as TradeTell, the name the portfolio uses; its id stays `IMC_Prosperity` so the logo key and card number don't move. EconOS, Halberd, DataFest and TradeTell take their new marks from each project's own SVG, and MicroMatch from the portfolio's webp, each pinned to the source commit in `sources.json`. Halberd's signal was "p50 ≤ 200 µs", a declared ceiling; it now shows the measured 2.6 µs. With Next.js gone the grid lists 13 technologies, so the table test expects 13.

## 2026-10-25: Sync recolored ClearHash repository logo #decision

Synchronized ClearHash's updated terminal phosphor logo into `assets/logos/repositories/ClearHash.svg`, refreshed its checksum in `sources.json`, and rebuilt all derived cell, card, table, and study SVGs.

## 2026-10-11: Stack schematic

The Stack section uses unboxed connector branches to distinguish it from the project gallery. SVGator is the authoring source; `assets/stack/source.json` preserves all four documents. Wide and mobile layouts each have light and dark exports. All 24 existing tools remain, with Web split into frontend and backend/full-stack branches.

The assets are static for README compatibility. GitHub's Markdown renderer preserves the combined viewport and color-scheme media queries. The profile README remains in Builder106/Builder106 and must be published after the assets.

The first preview felt too bland. The revised schematic replaces gray hairlines with colored routes, increases logo size from 22 to 34 px on desktop, and uses larger category names. Labels sit beneath the logos, and Infrastructure fits on one desktop branch. Mobile uses three columns with 30 px logos. The layout stays unboxed to distinguish it from Projects.

## 2026-10-23: Reject Any annotations and deprecated APIs #decision

Ruff now rejects Any in function arguments and return annotations across the repository. Pytest treats Python DeprecationWarning as an error.
