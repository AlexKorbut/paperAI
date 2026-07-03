#!/usr/bin/env python3
"""English edition of the two «Vedomosti» issues (3 & 4 July), A3, 2 spreads each.
Same paper as the Russian edition, in English, with a romanized VEDOMOSTI
nameplate. Content lives in scripts/vedomosti_content_en.py.

Usage:  PYTHONPATH=src python scripts/build_vedomosti_en.py
Outputs: .data/vedomosti_en/vedomosti_en_<date>.pdf
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

_spec = importlib.util.spec_from_file_location("ved_en", ROOT / "scripts" / "vedomosti_content_en.py")
_c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_c)
ISSUE1 = _c.ISSUE1 + _c.MISC1
ISSUE2 = _c.ISSUE2 + _c.MISC2

THEME = "petrine-vedomosti"
OUT = ROOT / ".data" / "vedomosti_en"
OUT.mkdir(parents=True, exist_ok=True)
JSONDIR = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/vedendocs")
JSONDIR.mkdir(parents=True, exist_ok=True)
A3_THEMES = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/themes_a3en")

SECTIONS = [
    ("life",    "LIFESTYLE"),
    ("world",   "THE WORLD"),
    ("belarus", "BELARUS"),
    ("science", "SCIENCE &amp; NATURE"),
    ("misc",    "SUNDRY NEWS"),
]
_SEC = dict(SECTIONS)
ORDER = [name for _id, name in SECTIONS]

ISSUES = [
    ("2026-07-03", "Printed at Moscow, the 3rd day of July, 2026", ISSUE1),
    ("2026-07-04", "Printed at Moscow, the 4th day of July, 2026", ISSUE2),
]


def prepare_a3_theme() -> Path:
    if A3_THEMES.exists():
        shutil.rmtree(A3_THEMES)
    shutil.copytree(ROOT / "themes", A3_THEMES)
    tdir = A3_THEMES / THEME
    # A3 + generous body size (matches the Russian edition).
    toml = tdir / "theme.toml"
    txt = toml.read_text(encoding="utf-8")
    txt = re.sub(r'(?m)^(page\s*=\s*)"a4"', r'\1"a3"', txt)
    txt = re.sub(r'(?m)^(body_pt\s*=\s*)[\d.]+', r'\g<1>16.5', txt)
    txt = re.sub(r'(?m)^(leading\s*=\s*)[\d.]+', r'\g<1>1.36', txt)
    toml.write_text(txt, encoding="utf-8")
    # English nameplate: romanize the title + subtitle, keep the eagle & rules.
    svg = (tdir / "masthead.svg").read_text(encoding="utf-8")
    svg = svg.replace("ВѢДОМОСТИ", "VEDOMOSTI")
    svg = svg.replace(
        "о воинскихъ и иныхъ дѣлахъ, достойныхъ знанія и памяти",
        "Of Military and Other Affairs Worthy of Knowledge and Memory")
    # widen letter-spacing suits the shorter Latin word; nudge it down a touch.
    svg = svg.replace('letter-spacing="6" fill="#241c10">VEDOMOSTI',
                      'letter-spacing="10" fill="#241c10">VEDOMOSTI')
    (tdir / "masthead.svg").write_text(svg, encoding="utf-8")
    return A3_THEMES


def build_issue(date_iso: str, date_line: str, rows, renderer: NodeRenderer):
    stories = [
        Story(id=aid, section=_SEC[sec], kind="feature", headline=head,
              dateline=dl, body_html=body, byline=None,
              source="Vedomosti", source_url="#")
        for aid, sec, head, dl, body in rows
    ]
    stories.sort(key=lambda s: ORDER.index(s.section))
    grid = GridPlan(
        page_format="a3", section_order=ORDER,
        slots=[GridSlot(story_id=s.id, section=s.section, size="medium",
                        columns=min(load_manifest(THEME).grid.columns, 6)) for s in stories],
    )
    doc = build_render_document(
        issue_id=f"vedomosti-en-{date_iso}", theme_id=THEME, locale="en",
        title="Vedomosti", stories=stories, grid_plan=grid,
    )
    doc.masthead.date = date_line
    (JSONDIR / f"vedomosti_en_{date_iso}.json").write_text(doc.model_dump_json(), encoding="utf-8")
    res = renderer.render(doc, out_path=OUT / f"vedomosti_en_{date_iso}.pdf")
    print(f"{date_iso}  -> vedomosti_en_{date_iso}.pdf  ({res.page_count} pp A3)")


def main() -> None:
    a3 = prepare_a3_theme()
    renderer = NodeRenderer(themes_dir=a3)
    for date_iso, date_line, rows in ISSUES:
        build_issue(date_iso, date_line, rows, renderer)


if __name__ == "__main__":
    main()
