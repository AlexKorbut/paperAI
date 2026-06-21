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
    half = max(2, min(columns, 6) // 2)
    third = max(2, min(columns, 6) // 2)
    slots = [
        # Dominant lead feature — the Center of Visual Impact.
        GridSlot(story_id="s-lead", section="world", size="lead", role="feature",
                 dominant=True, columns=min(columns, 6), with_photo=False,
                 pull_quote="Контекст важнее заголовка, перспектива важнее сенсации."),
        GridSlot(story_id="s-eu", section="world", size="medium", role="standard", columns=third),
        # Secondary feature.
        GridSlot(story_id="s-mkt", section="business", size="medium", role="feature", columns=third),
        # Boxed sidebar companion.
        GridSlot(story_id="s-firm", section="business", size="brief", role="sidebar", columns=half),
        GridSlot(story_id="s-ai", section="tech", size="medium", role="standard", columns=third),
        # Brief.
        GridSlot(story_id="s-chip", section="tech", size="brief", role="brief", columns=half),
        # Two teasers / анонсы.
        GridSlot(story_id="s-art", section="culture", size="brief", role="teaser",
                 body_policy="teaser_only", columns=half),
        GridSlot(story_id="s-film", section="culture", size="brief", role="teaser",
                 body_policy="teaser_only", columns=half),
    ]
    return GridPlan(page_format=page_format, section_order=section_order, slots=slots)


_DEFAULT_SECTION_ORDER = ["world", "business", "tech", "culture"]


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
