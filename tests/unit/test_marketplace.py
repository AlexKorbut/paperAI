import textwrap
from pathlib import Path

import pytest

from morning_paper import marketplace
from morning_paper.render import themes as themes_mod


def _bundle(parent: Path, tid: str, *, author: str = "", price: float = 0.0) -> Path:
    d = parent / tid
    d.mkdir(parents=True)
    mk = ""
    if author or price:
        mk = f'\n[marketplace]\nauthor = "{author}"\nprice_usd = {price}\nlicense = "OFL-1.1"\n'
    (d / "theme.toml").write_text(
        textwrap.dedent(
            f"""
            schema_version = 1
            id = "{tid}"
            display_name = "{tid} display"
            [type]
            masthead_font = "Georgia"
            headline_font = "Georgia"
            body_font = "Georgia"
            """
        ).strip()
        + mk,
        encoding="utf-8",
    )
    (d / "theme.css").write_text("/* x */", encoding="utf-8")
    return d


@pytest.fixture
def tmp_themes(tmp_path, monkeypatch):
    root = tmp_path / "themes"
    root.mkdir()
    monkeypatch.setattr(themes_mod, "THEMES_DIR", root)
    monkeypatch.setattr(marketplace, "THEMES_DIR", root)
    return root


def test_listing_marks_builtins_real_dir():
    # Against the real themes/ dir: builtins are flagged, none are third-party.
    items = {i["id"]: i for i in marketplace.listing()}
    assert "economist" in items
    assert items["economist"]["builtin"] is True
    assert items["economist"]["third_party"] is False


def test_install_and_uninstall(tmp_themes, tmp_path):
    src = _bundle(tmp_path / "src", "cool-theme", author="Jane", price=5.0)
    tid = marketplace.install_theme(src)
    assert tid == "cool-theme"
    assert "cool-theme" in themes_mod.list_theme_ids()

    listed = {i["id"]: i for i in marketplace.listing()}
    assert listed["cool-theme"]["third_party"] is True
    assert listed["cool-theme"]["author"] == "Jane"
    assert listed["cool-theme"]["price_usd"] == 5.0

    assert marketplace.uninstall_theme("cool-theme") is True
    assert "cool-theme" not in themes_mod.list_theme_ids()


def test_refuse_builtin_overwrite(tmp_themes, tmp_path):
    src = _bundle(tmp_path / "src", "economist")
    with pytest.raises(ValueError):
        marketplace.install_theme(src)
    with pytest.raises(ValueError):
        marketplace.uninstall_theme("economist")


def test_install_existing_requires_overwrite(tmp_themes, tmp_path):
    src = _bundle(tmp_path / "src", "dup")
    marketplace.install_theme(src)
    with pytest.raises(ValueError):
        marketplace.install_theme(src)
    # overwrite path succeeds
    assert marketplace.install_theme(src, overwrite=True) == "dup"


def test_id_must_match_dir(tmp_themes, tmp_path):
    d = tmp_path / "src" / "namedir"
    d.mkdir(parents=True)
    (d / "theme.toml").write_text(
        'schema_version=1\nid="other"\ndisplay_name="x"\n[type]\n'
        'masthead_font="Georgia"\nheadline_font="Georgia"\nbody_font="Georgia"\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        marketplace.install_theme(d)


def test_package_and_install_zip_roundtrip(tmp_themes, tmp_path):
    src = _bundle(tmp_path / "src", "zippy", author="Q")
    marketplace.install_theme(src)
    zip_path = marketplace.package_theme("zippy", tmp_path / "zippy.zip")
    assert zip_path.exists()
    marketplace.uninstall_theme("zippy")
    assert "zippy" not in themes_mod.list_theme_ids()

    tid = marketplace.install_zip(zip_path)
    assert tid == "zippy"
    assert "zippy" in themes_mod.list_theme_ids()


def test_zip_traversal_guard(tmp_themes, tmp_path):
    import zipfile

    bad = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad, "w") as zf:
        zf.writestr("../evil/theme.toml", "id='evil'")
    with pytest.raises(ValueError):
        marketplace.install_zip(bad)


def test_manifest_marketplace_fields(tmp_themes, tmp_path):
    _bundle(tmp_themes, "premium", author="Studio", price=9.0)
    m = themes_mod.load_manifest("premium")
    assert m.marketplace.author == "Studio"
    assert m.marketplace.price_usd == 9.0
    assert m.marketplace.license == "OFL-1.1"
