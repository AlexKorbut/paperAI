"""Web edition contract: the Node renderer turns a RenderDocument into a
self-contained responsive HTML file. Skips when Node/deps are absent (like the
PDF contract test) so the pure-Python suite stays green without a toolchain."""

import shutil
from pathlib import Path

import pytest

from morning_paper.config import RENDERER_DIR
from morning_paper.render.renderer import NodeRenderer
from morning_paper.sample import sample_render_document

node_missing = shutil.which("node") is None
deps_missing = not (RENDERER_DIR / "node_modules").exists()

pytestmark = pytest.mark.skipif(
    node_missing or deps_missing,
    reason="Node and renderer deps required (run `make install-node`)",
)


def test_renders_web_html(tmp_path: Path):
    doc = sample_render_document("infographic")
    out = tmp_path / "issue.html"
    path = NodeRenderer().render_web(doc, out_path=out)
    assert path.exists() and path.stat().st_size > 0
    html = out.read_text(encoding="utf-8")
    assert '<body data-theme="infographic">' in html
    assert "@media screen" in html            # responsive web overrides present
    assert "viewport" in html                 # mobile viewport meta present
