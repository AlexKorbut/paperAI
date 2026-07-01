#!/usr/bin/env python3
"""Build a personal-interest newspaper in the four antique `columns` themes,
in Russian and English. The editorial copy below is ORIGINAL evergreen prose
authored in place of the LLM stage (offline, no API key) — it stands in for the
per-user summaries the pipeline would normally produce.

Topics (12): моделинг, красота, здоровье, тренды, Китай, путешествия, Беларусь,
недвижимость в Беларуси, космос, флора и фауна, экспедиции, открытия.

Usage:  PYTHONPATH=src python scripts/build_interest_papers.py
Outputs: .data/showcase/<theme>__<lang>.pdf  and dumps docs to <JSONDIR>.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from morning_paper.models import GridPlan, GridSlot, Story          # noqa: E402
from morning_paper.render.document import build_render_document      # noqa: E402
from morning_paper.render.renderer import NodeRenderer               # noqa: E402
from morning_paper.render.themes import load_manifest                # noqa: E402

THEMES = ["petrine-vedomosti", "gazette-de-france", "pennsylvania-gazette", "wiener-zeitung"]

OUT = ROOT / ".data" / "showcase"
OUT.mkdir(parents=True, exist_ok=True)
JSONDIR = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/docs")
JSONDIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Content — one item per topic, in RU and EN. Fields per language:
#   sec: section head (flow-head)   head: small-caps subhead in the column
#   dl:  dateline run-in            body: 2 short paragraphs of HTML
# --------------------------------------------------------------------------- #
ROWS = [
    dict(
        id="modeling",
        ru=dict(sec="МОДЕЛИНГ", head="Подиум учится у улицы", dl="МИЛАН.",
                body="<p>Модельный бизнес переживает тихую перестройку: кастинг становится "
                     "разнообразнее по возрасту и типажу, а бренды всё чаще ищут не идеальные "
                     "пропорции, а узнаваемую индивидуальность и живую подачу.</p>"
                     "<p>Параллельно растёт роль цифровых аватаров и виртуальных съёмок, однако "
                     "агентства подчёркивают: камера по-прежнему ценит характер, а не только "
                     "безупречный силуэт.</p>"),
        en=dict(sec="MODELING", head="The Runway Learns from the Street", dl="MILAN.",
                body="<p>The modelling trade is undergoing a quiet reset: casting has grown more "
                     "diverse in age and type, and houses increasingly prize a recognisable "
                     "presence over flawless proportion.</p>"
                     "<p>Digital avatars and virtual shoots are rising in parallel, yet agencies "
                     "insist the camera still rewards character rather than silhouette alone.</p>"),
    ),
    dict(
        id="beauty",
        ru=dict(sec="КРАСОТА", head="Меньше значит лучше", dl="ПАРИЖ.",
                body="<p>На смену многоступенчатым ритуалам приходит «скинимализм»: короткий уход, "
                     "прозрачные составы и внимание к барьеру кожи. Покупатель читает этикетку "
                     "внимательнее, чем рекламный слоган.</p>"
                     "<p>Марки отвечают спросом на сокращённые формулы и перезаряжаемую упаковку, "
                     "а визажисты возвращают моду на естественный тон и мягкий блеск.</p>"),
        en=dict(sec="BEAUTY", head="Less, but Better", dl="PARIS.",
                body="<p>Elaborate multi-step routines are giving way to \"skinimalism\": fewer "
                     "products, honest ingredients and care for the skin barrier. Shoppers now read "
                     "the label more closely than the slogan.</p>"
                     "<p>Brands answer with pared-down formulas and refillable packaging, while "
                     "make-up artists revive a taste for natural tone and a soft sheen.</p>"),
    ),
    dict(
        id="health",
        ru=dict(sec="ЗДОРОВЬЕ", head="Сон возвращает себе статус", dl="ЖЕНЕВА.",
                body="<p>Исследователи всё увереннее ставят сон в один ряд с питанием и движением. "
                     "Регулярный режим, дневной свет по утрам и спокойный вечер дают эффект, "
                     "сравнимый с иными добавками.</p>"
                     "<p>Врачи напоминают о простом: несколько тысяч шагов в день, вода и паузы "
                     "от экрана заметно улучшают самочувствие без всякой моды на чудо-средства.</p>"),
        en=dict(sec="HEALTH", head="Sleep Reclaims Its Status", dl="GENEVA.",
                body="<p>Researchers increasingly rank sleep alongside diet and movement. A steady "
                     "schedule, morning daylight and a calm evening can rival many a supplement in "
                     "their measurable effect.</p>"
                     "<p>Physicians repeat the plain advice: a few thousand steps a day, water and "
                     "screen-free pauses lift well-being without any craze for miracle cures.</p>"),
    ),
    dict(
        id="trends",
        ru=dict(sec="ТРЕНДЫ", head="Тихая роскошь и цифровой аскетизм", dl="ЛОНДОН.",
                body="<p>На первый план выходит сдержанность: качественные материалы без логотипов, "
                     "долговечные вещи и спокойная палитра. «Тихая роскошь» из подиумного термина "
                     "стала бытовой привычкой.</p>"
                     "<p>Рядом крепнет цифровой аскетизм — осознанные паузы от лент и уведомлений. "
                     "Внимание снова считают ценным ресурсом, который стоит беречь.</p>"),
        en=dict(sec="TRENDS", head="Quiet Luxury and Digital Restraint", dl="LONDON.",
                body="<p>Restraint is ascendant: good materials without logos, long-lasting pieces "
                     "and a calm palette. \"Quiet luxury\" has slipped from runway jargon into an "
                     "everyday habit.</p>"
                     "<p>Alongside it grows a digital asceticism — deliberate pauses from feeds and "
                     "notifications. Attention is again treated as a resource worth guarding.</p>"),
    ),
    dict(
        id="china",
        ru=dict(sec="КИТАЙ", head="Электромобили меняют улицы", dl="ШЭНЬЧЖЭНЬ.",
                body="<p>Городской транспорт Китая стремительно электрифицируется: автобусы и такси "
                     "переходят на ток, а сеть скоростных поездов связывает мегаполисы плотнее "
                     "прежнего.</p>"
                     "<p>Производители делают ставку на доступные модели и быструю зарядку; экспорт "
                     "растёт, и вместе с ним — конкуренция за стандарты завтрашнего дня.</p>"),
        en=dict(sec="CHINA", head="Electric Cars Reshape the Streets", dl="SHENZHEN.",
                body="<p>China's urban transport is electrifying fast: buses and taxis switch to "
                     "current, while a lattice of high-speed trains binds the megacities more "
                     "tightly than before.</p>"
                     "<p>Makers bet on affordable models and rapid charging; exports climb, and with "
                     "them the contest to set tomorrow's standards.</p>"),
    ),
    dict(
        id="travel",
        ru=dict(sec="ПУТЕШЕСТВИЯ", head="Медленные маршруты входят в моду", dl="ЛИССАБОН.",
                body="<p>Путешественники всё чаще выбирают неспешность: ночные поезда, долгие "
                     "прогулки и один город вместо десяти. Ценят не количество отметок, а глубину "
                     "впечатления.</p>"
                     "<p>Малые города выигрывают от такого поворота: гость остаётся дольше, тратит "
                     "осмысленнее и возвращается за атмосферой, а не за галочкой в списке.</p>"),
        en=dict(sec="TRAVEL", head="Slow Routes Come into Fashion", dl="LISBON.",
                body="<p>Travellers increasingly choose to dawdle: night trains, long walks and one "
                     "city instead of ten. They prize depth of impression over a tally of stamps.</p>"
                     "<p>Smaller towns gain from the shift: the guest lingers, spends more "
                     "thoughtfully and returns for atmosphere rather than a box ticked.</p>"),
    ),
    dict(
        id="belarus",
        ru=dict(sec="БЕЛАРУСЬ", head="Озёрный край зовёт", dl="МИНСК.",
                body="<p>Браславские озёра и Беловежская пуща остаются визитной карточкой страны. "
                     "Агроусадьбы и веломаршруты набирают популярность у тех, кто ищет тишину и "
                     "чистую воду.</p>"
                     "<p>Реставрация замков в Мире и Несвиже поддерживает интерес к культурному "
                     "туризму, а короткие поездки на выходные становятся привычным форматом.</p>"),
        en=dict(sec="BELARUS", head="The Lakeland Beckons", dl="MINSK.",
                body="<p>The Braslav Lakes and Belovezhskaya Pushcha remain the country's calling "
                     "card. Farm-stays and cycling routes are winning over those in search of quiet "
                     "and clean water.</p>"
                     "<p>The restored castles at Mir and Nesvizh sustain an appetite for cultural "
                     "travel, while short weekend trips settle into a familiar habit.</p>"),
    ),
    dict(
        id="realty",
        ru=dict(sec="НЕДВИЖИМОСТЬ В БЕЛАРУСИ", head="Спрос смещается за город", dl="МИНСК.",
                body="<p>Покупатели всё чаще смотрят за кольцевую: частный дом или таунхаус в "
                     "пригороде обещает пространство и тишину при разумной дороге до центра.</p>"
                     "<p>В самом Минске ценятся компактные квартиры у метро и готовая отделка. "
                     "Аналитики советуют смотреть на инфраструктуру района не меньше, чем на цену "
                     "метра.</p>"),
        en=dict(sec="REAL ESTATE IN BELARUS", head="Demand Shifts Out of Town", dl="MINSK.",
                body="<p>Buyers increasingly look beyond the ring road: a house or townhouse in the "
                     "suburbs promises space and quiet within a reasonable commute of the centre.</p>"
                     "<p>Within Minsk, compact flats near the metro and move-in-ready finishes hold "
                     "their value. Analysts advise weighing a district's amenities as heavily as the "
                     "price per square metre.</p>"),
    ),
    dict(
        id="space",
        ru=dict(sec="КОСМОС", head="Частные ракеты открывают орбиту", dl="БАЙКОНУР.",
                body="<p>Многоразовые ступени и рой малых спутников удешевили доступ к орбите. "
                     "Запуски, ещё недавно редкие, идут теперь почти конвейером.</p>"
                     "<p>Учёные ждут нового поколения телескопов и лунных станций; частные компании "
                     "спорят за контракты, а вместе с ними множатся планы дальних полётов.</p>"),
        en=dict(sec="SPACE", head="Private Rockets Open the Orbit", dl="BAIKONUR.",
                body="<p>Reusable stages and swarms of small satellites have cut the cost of reaching "
                     "orbit. Launches, rare not long ago, now run almost on a conveyor.</p>"
                     "<p>Scientists await a new generation of telescopes and lunar stations; private "
                     "firms vie for contracts, and with them multiply the plans for distant flight.</p>"),
    ),
    dict(
        id="flora",
        ru=dict(sec="ФЛОРА И ФАУНА", head="Возвращение зубра", dl="БЕЛОВЕЖСКАЯ ПУЩА.",
                body="<p>Европейский зубр, некогда почти исчезнувший, вновь пасётся в заповедных "
                     "лесах. Программы восстановления вернули в природу тысячи животных.</p>"
                     "<p>Экологи говорят о более широком повороте к «переосвоению» — возвращению "
                     "рек, лугов и хищников, чтобы природа сама поддерживала равновесие.</p>"),
        en=dict(sec="FLORA & FAUNA", head="The Bison Returns", dl="BIALOWIEZA FOREST.",
                body="<p>The European bison, once nearly lost, again grazes the protected woods. "
                     "Recovery programmes have returned thousands of the animals to the wild.</p>"
                     "<p>Ecologists speak of a wider turn to \"rewilding\" — restoring rivers, "
                     "meadows and predators so that nature keeps its own balance.</p>"),
    ),
    dict(
        id="expeditions",
        ru=dict(sec="ЭКСПЕДИЦИИ", head="Под лёд Антарктиды", dl="АНТАРКТИДА.",
                body="<p>Международные группы бурят к подлёдным озёрам, скрытым под многокилометровой "
                     "толщей. Каждая проба воды может рассказать о жизни, отрезанной от мира "
                     "тысячелетиями.</p>"
                     "<p>Логистика остаётся суровой: короткое лето, мороз и ветер диктуют график. "
                     "И всё же именно здесь проверяются приборы для будущих полётов к спутникам "
                     "планет.</p>"),
        en=dict(sec="EXPEDITIONS", head="Beneath the Antarctic Ice", dl="ANTARCTICA.",
                body="<p>International teams drill toward subglacial lakes hidden under kilometres of "
                     "ice. Each sample of water may speak of life cut off from the world for "
                     "millennia.</p>"
                     "<p>The logistics stay harsh: a short summer, frost and wind dictate the "
                     "schedule. Yet it is here that instruments for future flights to icy moons are "
                     "put to the test.</p>"),
    ),
    dict(
        id="discoveries",
        ru=dict(sec="ОТКРЫТИЯ", head="Древний город под песками", dl="КАИР.",
                body="<p>Археологи описали кварталы поселения, скрытого под барханами. Находки — "
                     "мастерские, печати и утварь — уточняют карту древних торговых путей.</p>"
                     "<p>В лабораториях тем временем алгоритмы помогают читать выцветшие свитки и "
                     "складывать черепки, ускоряя работу, на которую прежде уходили годы.</p>"),
        en=dict(sec="DISCOVERIES", head="An Ancient City Beneath the Sands", dl="CAIRO.",
                body="<p>Archaeologists have mapped the quarters of a settlement buried under the "
                     "dunes. The finds — workshops, seals and vessels — sharpen the chart of old "
                     "trade roads.</p>"
                     "<p>In the laboratories, meanwhile, algorithms help read faded scrolls and "
                     "reassemble potsherds, speeding work that once took years.</p>"),
    ),
]


import re

# Paged.js pushes a multi-column block forward when it spans 3+ pages, blanking
# page 1. Keeping every paper to <=2 pages avoids the bug entirely. With 12
# topics that means a tight, brief-style item per topic — authentic for a dense
# antique sheet. We keep the first two sentences of the first paragraph (wide
# Cyrillic-fallback serifs run tall, so we leave generous margin).
_SENT = re.compile(r"(?<=[.!?])\s+")


def _brief(body: str) -> str:
    m = re.search(r"<p>(.*?)</p>", body, re.S)
    text = (m.group(1) if m else body).strip()
    short = " ".join(_SENT.split(text)[:2])
    return f"<p>{short}</p>"


def stories_for(lang: str) -> tuple[list[Story], list[str]]:
    out: list[Story] = []
    order: list[str] = []
    src_name = "Утренняя газета" if lang == "ru" else "The Morning Paper"
    for r in ROWS:
        c = r[lang]
        if c["sec"] not in order:
            order.append(c["sec"])
        out.append(
            Story(
                id=r["id"], section=c["sec"], kind="standard",
                headline=c["head"], dateline=c["dl"], body_html=_brief(c["body"]),
                byline=None, source=src_name, source_url="#",
            )
        )
    return out, order


def build(theme: str, lang: str):
    man = load_manifest(theme)
    sts, order = stories_for(lang)
    cols = min(man.grid.columns, 6)
    grid = GridPlan(
        page_format=man.format.page,
        section_order=order,
        slots=[GridSlot(story_id=s.id, section=s.section, size="medium", columns=cols) for s in sts],
    )
    title = "Утренняя газета" if lang == "ru" else "The Morning Paper"
    edition = "Выпуск по интересам" if lang == "ru" else "Interests Edition"
    doc = build_render_document(
        issue_id=f"{theme}-{lang}", theme_id=theme, locale=lang,
        title=title, stories=sts, grid_plan=grid, edition=edition,
    )
    return doc


def main() -> None:
    renderer = NodeRenderer()
    for theme in THEMES:
        for lang in ("ru", "en"):
            doc = build(theme, lang)
            (JSONDIR / f"{theme}__{lang}.json").write_text(doc.model_dump_json(), encoding="utf-8")
            pdf = OUT / f"{theme}__{lang}.pdf"
            res = renderer.render(doc, out_path=pdf)
            warn = f"  warnings={res.warnings}" if res.warnings else ""
            print(f"{theme:22} {lang}  -> {pdf.name}  ({res.page_count} pp){warn}")


if __name__ == "__main__":
    main()
