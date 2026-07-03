#!/usr/bin/env python3
"""One big Russian «Вѣдомости» — 4 spreads (8 A3 pages) in a single PDF.

Combines all Russian content of both daily issues (features of issue I & II plus
the two «Разныя вѣсти» miscellanies) into ONE issue, so every topic runs two
articles and the notices column is long — filling four spreads. Content lives in
scripts/vedomosti_content.py.

Usage:  PYTHONPATH=src python scripts/build_vedomosti_ru_big.py
Output: .data/vedomosti/vedomosti_bolshoy.pdf
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from morning_paper.models import GridPlan, GridSlot, Story          # noqa: E402
from morning_paper.render.document import build_render_document      # noqa: E402
from morning_paper.render.renderer import NodeRenderer               # noqa: E402
from morning_paper.render.themes import load_manifest                # noqa: E402

_spec = importlib.util.spec_from_file_location("ved_ru", ROOT / "scripts" / "vedomosti_content.py")
_c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_c)

THEME = "petrine-vedomosti"
OUT = ROOT / ".data" / "vedomosti"
OUT.mkdir(parents=True, exist_ok=True)
JSONDIR = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/vedbigdocs")
JSONDIR.mkdir(parents=True, exist_ok=True)
A3_THEMES = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/themes_a3big")

SECTIONS = [
    ("life",    "СТИЛЬ ЖИЗНИ"),
    ("world",   "МИРЪ"),
    ("belarus", "БѢЛАРУСЬ"),
    ("science", "НАУКА И ПРИРОДА"),
    ("misc",    "РАЗНЫЯ ВѢСТИ"),
]
_SEC = dict(SECTIONS)
ORDER = [name for _id, name in SECTIONS]
DATE_LINE = "Большой выпускъ · Печатана въ Москвѣ, лѣта 2026, iюля"

BODY_PT = 13.0  # tuned so the combined content fills exactly 4 spreads (8 pp)


def prepare() -> Path:
    if A3_THEMES.exists():
        shutil.rmtree(A3_THEMES)
    shutil.copytree(ROOT / "themes", A3_THEMES)
    toml = A3_THEMES / THEME / "theme.toml"
    txt = toml.read_text(encoding="utf-8")
    txt = re.sub(r'(?m)^(page\s*=\s*)"a4"', r'\1"a3"', txt)
    txt = re.sub(r'(?m)^(body_pt\s*=\s*)[\d.]+', rf'\g<1>{BODY_PT}', txt)
    txt = re.sub(r'(?m)^(leading\s*=\s*)[\d.]+', r'\g<1>1.36', txt)
    toml.write_text(txt, encoding="utf-8")
    return A3_THEMES


def rows():
    # Interleave the two issues' features per section so each topic's two
    # articles sit together, then all notices. Prefix ids to keep them unique.
    feats = [("a-" + r[0],) + r[1:] for r in _c.ISSUE1] + [("b-" + r[0],) + r[1:] for r in _c.ISSUE2]
    misc = _c.MISC1 + _c.MISC2
    return feats + misc


def main() -> None:
    a3 = prepare()
    renderer = NodeRenderer(themes_dir=a3)
    stories = [
        Story(id=aid, section=_SEC[sec], kind="feature", headline=head,
              dateline=dl, body_html=body, byline=None,
              source="Вѣдомости", source_url="#")
        for aid, sec, head, dl, body in rows()
    ]
    stories.sort(key=lambda s: ORDER.index(s.section))
    grid = GridPlan(
        page_format="a3", section_order=ORDER,
        slots=[GridSlot(story_id=s.id, section=s.section, size="medium",
                        columns=min(load_manifest(THEME).grid.columns, 6)) for s in stories],
    )
    doc = build_render_document(
        issue_id="vedomosti-bolshoy", theme_id=THEME, locale="ru",
        title="Вѣдомости", stories=stories, grid_plan=grid,
    )
    doc.masthead.date = DATE_LINE
    (JSONDIR / "vedomosti_bolshoy.json").write_text(doc.model_dump_json(), encoding="utf-8")
    res = renderer.render(doc, out_path=OUT / "vedomosti_bolshoy.pdf")
    print(f"vedomosti_bolshoy.pdf  ({res.page_count} pp A3)  stories={len(stories)}")


if __name__ == "__main__":
    main()
