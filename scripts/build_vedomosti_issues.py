#!/usr/bin/env python3
"""Two issues of «Петровскія Вѣдомости» (petrine-vedomosti), A3, ~2 spreads each,
for tomorrow and the day after. Captivating long-form Russian features live in
scripts/vedomosti_content.py (authored offline in place of the LLM).

Usage:  PYTHONPATH=src python scripts/build_vedomosti_issues.py
Outputs: .data/vedomosti/vedomosti_<date>.pdf + dumps docs for previews.
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

# Load the sibling content module without needing a package.
_spec = importlib.util.spec_from_file_location("vedomosti_content", ROOT / "scripts" / "vedomosti_content.py")
_content = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_content)
ISSUE1 = _content.ISSUE1 + _content.MISC1
ISSUE2 = _content.ISSUE2 + _content.MISC2

THEME = "petrine-vedomosti"
OUT = ROOT / ".data" / "vedomosti"
OUT.mkdir(parents=True, exist_ok=True)
JSONDIR = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/veddocs")
JSONDIR.mkdir(parents=True, exist_ok=True)
A3_THEMES = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/themes_a3v")

SECTIONS = [
    ("life",    "СТИЛЬ ЖИЗНИ"),
    ("world",   "МИРЪ"),
    ("belarus", "БѢЛАРУСЬ"),
    ("science", "НАУКА И ПРИРОДА"),
    ("misc",    "РАЗНЫЯ ВѢСТИ"),
]
_SEC = dict(SECTIONS)
ORDER = [name for _id, name in SECTIONS]

ISSUES = [
    ("2026-07-03", "Печатана въ Москвѣ, iюля въ 3 день 2026 года", ISSUE1),
    ("2026-07-04", "Печатана въ Москвѣ, iюля въ 4 день 2026 года", ISSUE2),
]


def prepare_a3_theme() -> Path:
    if A3_THEMES.exists():
        shutil.rmtree(A3_THEMES)
    shutil.copytree(ROOT / "themes", A3_THEMES)
    toml = A3_THEMES / THEME / "theme.toml"
    txt = toml.read_text(encoding="utf-8")
    txt = re.sub(r'(?m)^(page\s*=\s*)"a4"', r'\1"a3"', txt)
    txt = re.sub(r'(?m)^(body_pt\s*=\s*)[\d.]+', r'\g<1>13.0', txt)
    txt = re.sub(r'(?m)^(leading\s*=\s*)[\d.]+', r'\g<1>1.36', txt)
    toml.write_text(txt, encoding="utf-8")
    return A3_THEMES


def build_issue(date_iso: str, date_line: str, rows, renderer: NodeRenderer):
    stories = [
        Story(id=aid, section=_SEC[sec], kind="feature", headline=head,
              dateline=dl, body_html=body, byline=None,
              source="Вѣдомости", source_url="#")
        for aid, sec, head, dl, body in rows
    ]
    stories.sort(key=lambda s: ORDER.index(s.section))
    grid = GridPlan(
        page_format="a3", section_order=ORDER,
        slots=[GridSlot(story_id=s.id, section=s.section, size="medium",
                        columns=min(load_manifest(THEME).grid.columns, 6)) for s in stories],
    )
    doc = build_render_document(
        issue_id=f"vedomosti-{date_iso}", theme_id=THEME, locale="ru",
        title="Вѣдомости", stories=stories, grid_plan=grid,
    )
    doc.masthead.date = date_line
    (JSONDIR / f"vedomosti_{date_iso}.json").write_text(doc.model_dump_json(), encoding="utf-8")
    res = renderer.render(doc, out_path=OUT / f"vedomosti_{date_iso}.pdf")
    print(f"{date_iso}  -> vedomosti_{date_iso}.pdf  ({res.page_count} pp A3)")


def main() -> None:
    a3 = prepare_a3_theme()
    renderer = NodeRenderer(themes_dir=a3)
    for date_iso, date_line, rows in ISSUES:
        build_issue(date_iso, date_line, rows, renderer)


if __name__ == "__main__":
    main()
