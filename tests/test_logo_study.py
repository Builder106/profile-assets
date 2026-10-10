import base64
import hashlib
import xml.etree.ElementTree as ET

from test_assets import load


def test_logo_study_embeds_original_artwork_and_named_tiles(tmp_path):
    study = load("gen_logo_study")
    study.write_study(tmp_path)
    for theme in ("light", "dark"):
        root = ET.parse(tmp_path / f"logo-study-{theme}.svg").getroot()
        tiles = root.findall(f"{{{study.SVG}}}svg")
        assert len(tiles) == 4
        assert [tile.get("x") for tile in tiles] == ["16", "162", "308", "454"]
        images = root.findall(f".//{{{study.SVG}}}image")
        assert len(images) == 12
        for image in images:
            href = image.get("href")
            assert href.startswith("data:image/svg+xml;base64,")
            ET.fromstring(base64.b64decode(href.split(",", 1)[1]))
        for tile, project in zip(tiles, study.STUDY, strict=True):
            image = next(
                image for image in tile.findall(f".//{{{study.SVG}}}image") if image.get("data-role") == "project"
            )
            content = base64.b64decode(image.get("href").split(",", 1)[1])
            assert hashlib.sha256(content).hexdigest() == load("gen_cells").SOURCES["repositories"][project]["sha256"]


def test_full_table_preserves_artwork_and_transparent_cards():
    cells = load("gen_cells")
    for theme in ("light", "dark"):
        root = ET.fromstring(cells.unified_svg(theme))
        groups = [g for g in root.findall(f"{{{cells.SVG}}}g") if g.get("class") == "cell"]
        assert len(groups) == len(cells.CELLS) == 20
        for group, cell in zip(groups, cells.CELLS, strict=True):
            card = group.find(f"{{{cells.SVG}}}rect")
            assert card.get("fill") == "none"
            assert card.get("rx") == "2"
            assert len(group.findall(f"{{{cells.SVG}}}rect")) == 1
            art = next(
                image for image in group.findall(f".//{{{cells.SVG}}}image") if image.get("data-role") == "project"
            )
            data = base64.b64decode(art.get("href").split(",", 1)[1])
            assert (
                hashlib.sha256(data).hexdigest()
                == cells.SOURCES.get("repository_variants", {}).get(
                    f"{cell[5]}_{theme}", cells.SOURCES["repositories"][cell[5]]
                )["sha256"]
            )
            labels = [text.text for text in group.findall(f"{{{cells.SVG}}}text")]
            assert labels == [cells.DISPLAY_NAMES[cell[5]], cell[4]]
            if cell[4] in {"C99", "Yul"}:
                assert len(group.findall(f".//{{{cells.SVG}}}image")) == 2
            else:
                assert len(group.findall(f".//{{{cells.SVG}}}image")) == 3
        for image in root.iter(f"{{{cells.SVG}}}image"):
            href = image.get("href")
            assert href.startswith("data:image/")
            content = base64.b64decode(href.split(",", 1)[1])
            if href.startswith("data:image/svg+xml"):
                ET.fromstring(content)
            elif href.startswith("data:image/png"):
                assert content.startswith(b"\x89PNG\r\n\x1a\n")
            else:
                assert content[:4] == b"RIFF" and content[8:12] == b"WEBP"
        for kind in cells.SOURCES.values():
            if isinstance(kind, dict):
                for source in kind.values():
                    assert hashlib.sha256((cells.LOGOS / source["file"]).read_bytes()).hexdigest() == source["sha256"]
