# Builder106 profile assets

This repository contains the generated visual assets and source tooling for the Builder106 GitHub profile: hero graphics, periodic-table graphics, banners, palette generation, accessibility auditing, and profile-picture source files.

The canonical profile README remains in [`Builder106/Builder106`](https://github.com/Builder106/Builder106). This repository does not duplicate that README. CI receives an external copy through `--readme` or `PROFILE_README_PATH`, so asset checks can validate the published profile without making two files authoritative.

## Local commands

```text
python -m pytest
python assets/audit.py --readme /path/to/Builder106/README.md
python assets/build.py
```

`assets/build.py` writes generated per-cell SVGs to `assets/cells/` (ignored by Git) and the flagship index to `assets/flagships/`. The index is reproducible, but remains versioned because it is a published profile asset. The committed hero, table, banner, flagship-index, and profile-picture outputs are all published profile assets.

## Profile README asset URLs

The profile README should reference published files with absolute URLs under:

`https://raw.githubusercontent.com/Builder106/profile-assets/main/assets/`

Keep the README's light/dark `<picture>` structure and descriptive alternative text when updating those references.
