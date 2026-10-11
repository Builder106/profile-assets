# Stack schematic

The profile uses four static SVGator exports: light and dark versions of the wide and mobile layouts. Colored routes, larger logos, and bold category names give the schematic its structure. Web has separate frontend and backend/full-stack branches. The mobile layout uses three columns and keeps all 24 tools.

`source.json` contains each editable SVGator document and the editor link. To change a variant, pass its document to SVGator's `replace_project`, then export with `format: svg`, `svgFormat: static`, and `font: no-export`. The editor opens the wide light version. Keep all four exports together when changing the tool list.

Technology marks are embedded from [Simple Icons 11.15.0](https://github.com/simple-icons/simple-icons/tree/11.15.0), under [CC0](../logos/technologies/LICENSE.md). Brand marks remain subject to their respective trademarks. Dark variants adjust dark silhouettes for visibility. SVGs contain no external image or font dependencies, scripts, or animation.

The profile README selects the mobile layout below 768 px and includes the full tool list as alternative text. Publish these assets before publishing the README that references them.
