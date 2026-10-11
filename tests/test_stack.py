import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

import pytest
from test_assets import load

STACK = Path(__file__).parents[1] / "assets" / "stack"
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}"
TOOLS = {
    "OCaml",
    "Rust",
    "C",
    "Swift",
    "TypeScript",
    "Angular",
    "Vue",
    "React",
    "Tailwind",
    "Next.js",
    "SvelteKit",
    "Rails",
    "Express",
    "Python",
    "R",
    "Jupyter",
    "DuckDB",
    "pandas",
    "Docker",
    "GitHub Actions",
    "Vercel",
    "Caddy",
    "Oracle Cloud",
    "Playwright",
}


@pytest.mark.parametrize("variant", ["light", "dark", "mobile-light", "mobile-dark"])
def test_stack_export(variant):
    path = STACK / f"stack-{variant}.svg"
    source = path.read_text()
    root = ET.fromstring(source)
    labels = {"".join(node.itertext()) for node in root.iter(f"{SVG}text")}
    assert TOOLS <= labels
    assert {"Systems", "Web", "Data", "Infrastructure"} <= labels
    assert not load("audit").audit_svg(path)
    assert "NaN" not in source
    assert not root.findall(f".//{SVG}script")
    assert not root.findall(f".//{SVG}animate")
    images = list(root.iter(f"{SVG}image"))
    assert len(images) == len(TOOLS)
    for image in images:
        href = image.get("href") or image.get(f"{XLINK}href")
        assert href.startswith("data:image/svg+xml,")
        assert ET.fromstring(unquote(href.split(",", 1)[1])).tag == f"{SVG}svg"
    documents = json.loads((STACK / "source.json").read_text())["documents"]
    key = variant if variant.startswith("mobile") else f"wide-{variant}"
    size = documents[key]["properties"]["shape"]["size"]
    assert root.get("viewBox") == f"0 0 {size['width']} {size['height']}"
