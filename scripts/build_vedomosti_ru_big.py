#!/usr/bin/env python3
"""Russian «Вѣдомости» sized to the project's `spreads` setting.

The number of spreads (разворотов) comes from config/settings.toml
([defaults] spreads); one spread = two A3 pages, so the target is spreads*2
pages. The generator selects a proportional amount of content from both issues'
features + the «Разныя вѣсти» miscellany and auto-tunes the body size so the
rendered PDF lands on exactly that page count (rendering is deterministic).

Override the setting ad hoc with the MP_SPREADS env var.

Usage:  PYTHONPATH=src python scripts/build_vedomosti_ru_big.py
Output: .data/vedomosti/vedomosti_<spreads>sp.pdf
"""
from __future__ import annotations

import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from morning_paper.config import get_settings                       # noqa: E402
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

SECTIONS = [("life", "СТИЛЬ ЖИЗНИ"), ("world", "МИРЪ"), ("belarus", "БѢЛАРУСЬ"),
            ("science", "НАУКА И ПРИРОДА"), ("misc", "РАЗНЫЯ ВѢСТИ")]
_SEC = dict(SECTIONS)
ORDER = [name for _id, name in SECTIONS]

# Full content pool ≈ 4 spreads (8 pages). Prefix ids so the two issues' twin
# articles (same topic) do not collide.
FEATURES = [("a-" + r[0],) + tuple(r[1:]) for r in _c.ISSUE1] + \
           [("b-" + r[0],) + tuple(r[1:]) for r in _c.ISSUE2]
MISC = list(_c.MISC1) + list(_c.MISC2)
FULL_SPREADS = 4  # the pool fills about this many spreads


def spreads_setting() -> int:
    if os.environ.get("MP_SPREADS"):
        return max(1, int(os.environ["MP_SPREADS"]))
    return get_settings().file.defaults.spreads


def select_content(spreads: int):
    """Take a share of the pool proportional to the requested spreads."""
    frac = spreads / FULL_SPREADS
    nf = max(1, min(len(FEATURES), round(len(FEATURES) * frac)))
    nm = max(0, min(len(MISC), round(len(MISC) * frac)))
    return FEATURES[:nf] + MISC[:nm]


def prepare() -> Path:
    if A3_THEMES.exists():
        shutil.rmtree(A3_THEMES)
    shutil.copytree(ROOT / "themes", A3_THEMES)
    toml = A3_THEMES / THEME / "theme.toml"
    txt = toml.read_text(encoding="utf-8")
    txt = re.sub(r'(?m)^(page\s*=\s*)"a4"', r'\1"a3"', txt)
    txt = re.sub(r'(?m)^(leading\s*=\s*)[\d.]+', r'\g<1>1.36', txt)
    toml.write_text(txt, encoding="utf-8")
    return A3_THEMES


def set_body_pt(pt: float) -> None:
    toml = A3_THEMES / THEME / "theme.toml"
    txt = toml.read_text(encoding="utf-8")
    txt = re.sub(r'(?m)^(body_pt\s*=\s*)[\d.]+', rf'\g<1>{pt}', txt)
    toml.write_text(txt, encoding="utf-8")


def build_doc(rows, spreads: int):
    stories = [
        Story(id=aid, section=_SEC[sec], kind="feature", headline=head,
              dateline=dl, body_html=body, byline=None, source="Вѣдомости", source_url="#")
        for aid, sec, head, dl, body in rows
    ]
    stories.sort(key=lambda s: ORDER.index(s.section))
    grid = GridPlan(
        page_format="a3", section_order=ORDER,
        slots=[GridSlot(story_id=s.id, section=s.section, size="medium",
                        columns=min(load_manifest(THEME).grid.columns, 6)) for s in stories],
    )
    doc = build_render_document(
        issue_id=f"vedomosti-{spreads}sp", theme_id=THEME, locale="ru",
        title="Вѣдомости", stories=stories, grid_plan=grid,
    )
    doc.masthead.date = f"Выпускъ на {spreads} разворота · Печатана въ Москвѣ, лѣта 2026"
    return doc, stories


def main() -> None:
    spreads = spreads_setting()
    target = spreads * 2
    rows = select_content(spreads)
    a3 = prepare()
    renderer = NodeRenderer(themes_dir=a3)
    out = OUT / f"vedomosti_{spreads}sp.pdf"

    # Auto-tune body_pt so the deterministic render lands on `target` pages.
    tried: dict[float, int] = {}

    def npages(pt: float) -> int:
        pt = round(max(10.0, min(19.0, pt)), 1)
        if pt in tried:
            return tried[pt]
        set_body_pt(pt)
        doc, _ = build_doc(rows, spreads)
        n = NodeRenderer(themes_dir=a3).render(doc, out_path=out).page_count or 0
        tried[pt] = n
        return n

    pt = 13.0
    n = npages(pt)
    guard = 0
    while n != target and guard < 16:
        pt += 0.5 if n < target else -0.5
        n = npages(pt)
        guard += 1

    best = min(tried, key=lambda k: (abs(tried[k] - target), k))
    set_body_pt(best)
    doc, stories = build_doc(rows, spreads)
    (JSONDIR / f"vedomosti_{spreads}sp.json").write_text(doc.model_dump_json(), encoding="utf-8")
    res = NodeRenderer(themes_dir=a3).render(doc, out_path=out)
    got = res.page_count
    note = "" if got == target else f"  (closest to target {target}; content-limited)"
    print(f"spreads={spreads}  target={target}pp  -> {out.name}  {got}pp @ body_pt={best}"
          f"  stories={len(stories)}{note}")


if __name__ == "__main__":
    main()
