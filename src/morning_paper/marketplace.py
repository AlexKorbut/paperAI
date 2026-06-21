"""Theme marketplace (Phase 3): themes are data, so third parties can ship them.

A "theme bundle" is just a ``themes/<id>/`` directory (theme.toml [+ theme.css,
masthead.svg, fonts/]). This module lists installed themes with their marketplace
metadata, installs a bundle from a directory (after validating its manifest),
and packages an installed theme into a shareable zip — the primitives a real
marketplace (upload/download/payment) would build on.

Builtin themes ship in the repo; ``install_theme`` adds new ones into the same
``themes/`` dir so the Node renderer (which is pointed at one dir) can use them
without any multi-directory plumbing.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from .config import THEMES_DIR
from .render.themes import ThemeManifest, list_theme_ids, load_manifest

# Themes shipped in the repo. Anything else under themes/ was installed.
BUILTIN_IDS = {
    "times-classic", "economist", "nyt-modern", "mono-minimal", "old-russian",
    "vintage", "art-nouveau", "swiss-grotesk", "victorian", "infographic",
}


def listing() -> list[dict]:
    """All installed themes with marketplace metadata, for a store UI."""
    out: list[dict] = []
    for tid in list_theme_ids():
        try:
            m = load_manifest(tid)
        except Exception:
            continue
        mk = m.marketplace
        out.append(
            {
                "id": m.id,
                "display_name": m.display_name,
                "mood": m.mood,
                "author": mk.author,
                "price_usd": mk.price_usd,
                "homepage": mk.homepage,
                "license": mk.license,
                "builtin": m.id in BUILTIN_IDS,
                "third_party": m.id not in BUILTIN_IDS,
            }
        )
    return out


def _validate_bundle(src: Path) -> ThemeManifest:
    toml = src / "theme.toml"
    if not toml.exists():
        raise ValueError(f"not a theme bundle: missing {toml}")
    # Parse via the same loader used at render time so we reject bad manifests early.
    import tomllib

    with toml.open("rb") as fh:
        data = tomllib.load(fh)
    manifest = ThemeManifest.model_validate(data)
    if manifest.id != src.name:
        raise ValueError(
            f"theme id {manifest.id!r} must match its directory name {src.name!r}"
        )
    return manifest


def install_theme(src_dir: str | Path, *, overwrite: bool = False) -> str:
    """Install a theme bundle directory into ``themes/``; returns the theme id.

    Refuses to clobber a builtin theme, and any existing theme unless
    ``overwrite=True``.
    """
    src = Path(src_dir)
    if not src.is_dir():
        raise ValueError(f"{src} is not a directory")
    manifest = _validate_bundle(src)
    tid = manifest.id

    if tid in BUILTIN_IDS:
        raise ValueError(f"{tid!r} is a builtin theme and cannot be overwritten")
    dest = THEMES_DIR / tid
    if dest.exists():
        if not overwrite:
            raise ValueError(f"theme {tid!r} already installed; pass overwrite=True to replace")
        shutil.rmtree(dest)

    shutil.copytree(src, dest)
    return tid


def uninstall_theme(theme_id: str) -> bool:
    """Remove an installed (non-builtin) theme. Returns True if removed."""
    if theme_id in BUILTIN_IDS:
        raise ValueError(f"{theme_id!r} is a builtin theme and cannot be uninstalled")
    dest = THEMES_DIR / theme_id
    if not dest.exists():
        return False
    shutil.rmtree(dest)
    return True


def install_zip(zip_path: str | Path, *, overwrite: bool = False) -> str:
    """Install a theme packaged as a zip (a single top-level ``<id>/`` dir)."""
    import tempfile

    zp = Path(zip_path)
    if not zp.is_file():
        raise ValueError(f"{zp} is not a file")
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zp) as zf:
            # Guard against path traversal in crafted archives.
            for name in zf.namelist():
                if name.startswith("/") or ".." in Path(name).parts:
                    raise ValueError(f"unsafe path in archive: {name!r}")
            zf.extractall(tmp)
        roots = [p for p in Path(tmp).iterdir() if p.is_dir() and (p / "theme.toml").exists()]
        if len(roots) != 1:
            raise ValueError("zip must contain exactly one theme bundle directory")
        return install_theme(roots[0], overwrite=overwrite)


def package_theme(theme_id: str, out_zip: str | Path) -> Path:
    """Zip an installed theme into a shareable bundle (for publishing)."""
    src = THEMES_DIR / theme_id
    if not (src / "theme.toml").exists():
        raise ValueError(f"no installed theme {theme_id!r}")
    out = Path(out_zip)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(src.parent)))
    return out
