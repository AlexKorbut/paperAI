"""Sample content for the typography prototype.

Used by `cli render-proto` and the renderer contract test so we can exercise the
whole theme/render path with NO LLM, network, or DB. The prose is filler, but the
STRUCTURE is real: a dominant lead feature, secondary features, a boxed sidebar,
a briefs cluster, and two teasers ("анонсы") — so every theme shows true
newspaper hierarchy rather than a flat list of summaries.
"""

from __future__ import annotations

from .models import GridPlan, GridSlot, Story
from .render.document import build_render_document
from .render.themes import load_manifest

_LOREM = (
    "<p>В предрассветной тишине редакция собрала главные сюжеты дня, чтобы "
    "читатель мог осмыслить их за неспешной чашкой кофе. Ниже — связное "
    "изложение событий, без спешки и без шума ленты.</p>"
    "<p>Аналитики отмечают, что за сухими цифрами стоят живые решения людей, "
    "и именно их последствия определят повестку ближайших недель. Контекст "
    "важнее заголовка, а перспектива важнее сенсации.</p>"
    "<p>Мы переводим и пересказываем источники на разных языках, сохраняя "
    "ссылку на оригинал и уважая труд журналистов, чьи материалы легли в "
    "основу этого выпуска.</p>"
)
_SHORT = (
    "<p>Короткая заметка для колонки кратких новостей: один факт, один контекст, "
    "одна ссылка на первоисточник.</p>"
)

# id, section, kind, kicker, headline, deck, dateline, teaser_text, body
_ROWS = [
    ("s-lead", "world", "feature", "В МИРЕ", "Дипломатия выходит из тупика",
     "Переговоры дали первый за месяц результат", "ЖЕНЕВА", None, _LOREM),
    ("s-eu", "world", "standard", "ЕВРОПА", "Европа сверяет часы",
     "Брюссель ищет общий знаменатель", "БРЮССЕЛЬ", None, _LOREM),
    ("s-mkt", "business", "feature", "РЫНКИ", "Рынки нащупывают дно",
     "Инвесторы осторожно возвращаются", "ЛОНДОН", None, _LOREM),
    ("s-firm", "business", "sidebar", "СПРАВКА", "Что важно знать о сделке",
     None, None, None,
     "<p>Регулятор берёт паузу до конца квартала.</p><p>Стороны сохраняют условия.</p>"),
    ("s-ai", "tech", "standard", "ТЕХНОЛОГИИ", "ИИ переписывает редакции",
     "Инструменты меняют рабочий день", "САН-ФРАНЦИСКО", None, _LOREM),
    ("s-chip", "tech", "brief", "ПОЛУПРОВОДНИКИ", "Гонка за кремнием",
     "Новые фабрики и старые узкие места", None, None, _SHORT),
    ("s-art", "culture", "teaser", "КУЛЬТУРА", "Возвращение большой формы",
     None, None, "Почему толстые романы снова в моде — и кто их издаёт.", _SHORT),
    ("s-film", "culture", "teaser", "КИНО", "Фестиваль без фаворитов",
     None, None, "Жюри в растерянности: репортаж с закрытия — на стр. 7.", _SHORT),
]


def _stories() -> list[Story]:
    out: list[Story] = []
    for sid, section, kind, kicker, headline, deck, dateline, teaser, body in _ROWS:
        out.append(
            Story(
                id=sid, section=section, kind=kind, kicker=kicker,
                headline=headline, deck=deck, dateline=dateline, teaser_text=teaser,
                body_html=body, byline="Редакция Morning Paper",
                source="Wire", source_url="https://example.org/",
            )
        )
    return out


def sample_grid_plan(*, page_format: str, columns: int, section_order: list[str]) -> GridPlan:
    cols = min(columns, 6)
    hi = (cols + 1) // 2          # ceil half
    lo = max(2, cols // 2)        # floor half (>=2)
    sm = 2                        # narrow modules tile the bottom row
    slots = [
        # Dominant lead feature — the Center of Visual Impact (full bleed).
        GridSlot(story_id="s-lead", section="world", size="lead", role="feature",
                 dominant=True, columns=cols, with_photo=False,
                 pull_quote="Контекст важнее заголовка, перспектива важнее сенсации."),
        # Row 2: two features side by side (lo + hi = cols).
        GridSlot(story_id="s-eu", section="world", size="medium", role="feature", columns=lo),
        GridSlot(story_id="s-mkt", section="business", size="medium", role="feature", columns=hi),
        # Row 3: a standard article + a boxed sidebar (lo + hi = cols).
        GridSlot(story_id="s-ai", section="tech", size="medium", role="standard", columns=lo),
        GridSlot(story_id="s-firm", section="business", size="brief", role="sidebar", columns=hi),
        # Row 4: a brief + two teasers / анонсы.
        GridSlot(story_id="s-chip", section="tech", size="brief", role="brief", columns=sm),
        GridSlot(story_id="s-art", section="culture", size="brief", role="teaser",
                 body_policy="teaser_only", columns=sm),
        GridSlot(story_id="s-film", section="culture", size="brief", role="teaser",
                 body_policy="teaser_only", columns=sm),
    ]
    return GridPlan(page_format=page_format, section_order=section_order, slots=slots)


_DEFAULT_SECTION_ORDER = ["world", "business", "tech", "culture"]


def specimen_render_document(theme_id: str, *, locale: str = "ru", style_overrides: dict | None = None):
    """A tiny one-section document for theme PREVIEW cards: masthead + a dominant
    headline + a few body lines + a teaser, so a user sees the font and layout
    style at a glance. Honors per-user style overrides for a live tuning preview."""
    manifest = load_manifest(theme_id)
    stories = [
        Story(id="p-lead", section="sample", kind="feature", kicker="ОБРАЗЕЦ",
              headline="Как читается эта газета",
              deck="Заголовок, подзаголовок и основной текст — в типографике темы",
              dateline="МИНСК", body_html=_LOREM, byline="Morning Paper",
              source="Wire", source_url="#"),
        Story(id="p-std", section="sample", kind="standard", kicker="РУБРИКА",
              headline="Вторичный материал колонкой", deck=None,
              body_html=_SHORT, byline="Morning Paper", source="Wire", source_url="#"),
        Story(id="p-teaser", section="sample", kind="teaser", kicker="АНОНС",
              headline="Большой материал — внутри номера", deck=None,
              teaser_text="Так выглядит анонс: рубрика, заголовок, строка и стрелка.",
              body_html=_SHORT, byline="Подробнее", source="Wire", source_url="#"),
    ]
    cols = min(manifest.grid.columns, 6)
    grid = GridPlan(
        page_format=manifest.format.page,
        section_order=["sample"],
        slots=[
            GridSlot(story_id="p-lead", section="sample", size="lead", role="feature",
                     dominant=True, columns=cols,
                     pull_quote="Приятная типографика важнее сенсации."),
            GridSlot(story_id="p-std", section="sample", size="medium", role="standard",
                     columns=max(2, cols // 2)),
            GridSlot(story_id="p-teaser", section="sample", size="brief", role="teaser",
                     body_policy="teaser_only", columns=max(2, cols // 2)),
        ],
    )
    return build_render_document(
        issue_id="specimen", theme_id=theme_id, locale=locale,
        title="The Morning Paper", stories=stories, grid_plan=grid,
        edition="Образец стиля", style_overrides=style_overrides or {},
    )


def sample_render_document(theme_id: str, *, locale: str = "ru"):
    """Build a complete RenderDocument for a theme using sample content.

    Uses a fixed generic section_order so the sample GridSlots (which reference
    "world", "business", "tech", "culture") render consistently across every theme.
    """
    manifest = load_manifest(theme_id)
    grid = sample_grid_plan(
        page_format=manifest.format.page,
        columns=manifest.grid.columns,
        section_order=_DEFAULT_SECTION_ORDER,
    )
    return build_render_document(
        issue_id="proto-0001",
        theme_id=theme_id,
        locale=locale,
        title="The Morning Paper",
        stories=_stories(),
        grid_plan=grid,
        issue_no="1",
        edition="Prototype",
    )
