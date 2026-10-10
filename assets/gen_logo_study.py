"""Generate four repo and technology logo tiles for visual review."""

import xml.etree.ElementTree as ET
from pathlib import Path

from gen_cells import CELLS, DISPLAY_NAMES, SVG, cell_svg

ASSETS = Path(__file__).parent
STUDY = {key: DISPLAY_NAMES[key] for key in ("ocaml_limit", "ClearHash", "CapitolAlpha", "MedCore")}


def logo_cell(theme: str, cell: tuple) -> ET.Element:
    _, _, num, symbol, lang, project, disc = cell
    return ET.fromstring(cell_svg(theme, num, symbol, lang, project, disc))


def study_svg(theme: str) -> str:
    root = ET.Element(
        f"{{{SVG}}}svg",
        {
            "width": "600",
            "height": "170",
            "viewBox": "0 0 600 170",
            "role": "img",
            "aria-label": "OCaml Limit: Quant, OCaml; ClearHash: Cybersec, Rust; CapitolAlpha: Analyst, Python; MedCore: HealthTech, React",
        },
    )
    selected = [cell for cell in CELLS if cell[5] in STUDY]
    for index, cell in enumerate(selected):
        tile = logo_cell(theme, cell)
        tile.set("x", str(16 + index * 146))
        tile.set("y", "20")
        root.append(tile)
    return ET.tostring(root, encoding="unicode") + "\n"


def write_study(out_dir: Path) -> None:
    for theme in ("light", "dark"):
        (out_dir / f"logo-study-{theme}.svg").write_text(study_svg(theme))


if __name__ == "__main__":
    write_study(ASSETS)
