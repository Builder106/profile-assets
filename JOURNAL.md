# Journal

## 2026-10-11: Stack schematic

The Stack section uses unboxed connector branches to distinguish it from the project gallery. SVGator is the authoring source; `assets/stack/source.json` preserves all four documents. Wide and mobile layouts each have light and dark exports. All 24 existing tools remain, with Web split into frontend and backend/full-stack branches.

The assets are static for README compatibility. GitHub's Markdown renderer preserves the combined viewport and color-scheme media queries. The profile README remains in Builder106/Builder106 and must be published after the assets.

The first preview felt too bland. The revised schematic replaces gray hairlines with colored routes, increases logo size from 22 to 34 px on desktop, and uses larger category names. Labels sit beneath the logos, and Infrastructure fits on one desktop branch. Mobile uses three columns with 30 px logos. The layout stays unboxed to distinguish it from Projects.

## 2026-10-23: Reject Any annotations and deprecated APIs #decision

Ruff now rejects Any in function arguments and return annotations across the repository. Pytest treats Python DeprecationWarning as an error.
