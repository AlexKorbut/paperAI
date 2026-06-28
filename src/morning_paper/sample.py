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


# ---- Antique "columns" layout demo (The London Chronicle, 1759) ------------
# Period-flavoured English placeholder so the specimen reads "точь в точь" like
# the original evening post. In production the user's real content flows into the
# same continuous-column layout. id, section (= small-caps head), dateline, body.
_CHRON_SECTIONS = ["The London Gazette", "Foreign Affairs", "London",
                   "Country News", "Ship News", "Bankrupts"]
_CHRON_ROWS = [
    ("c-gaz1", "The London Gazette", None,
     "<p>Whitehall, October 13. The King hath been graciously pleased to grant "
     "unto the Reverend Doctor Markham the deanery of Rochester, void by the "
     "translation of the late incumbent; as also to constitute and appoint divers "
     "officers of the household, whose names shall in due course be made known.</p>"
     "<p>His Majesty hath likewise been pleased to order, that a medal be struck "
     "in commemoration of the late signal successes of his arms, both by sea and "
     "land, to the lasting honour of the British nation.</p>"),
    ("c-gaz2", "The London Gazette", "St. James's, October 13.",
     "<p>This day the Right Honourable the Lords Commissioners of the Admiralty "
     "waited upon his Majesty with the agreeable advices lately received from the "
     "fleet, and were received most graciously.</p>"),
    ("c-for1", "Foreign Affairs", "Hamburgh, September 21.",
     "<p>The advices we have this day received from the army import, that the "
     "allied forces had passed the river without opposition, and were advancing by "
     "hasty marches towards the enemy, who appeared in no condition to dispute the "
     "passage. It is added, that several magazines had fallen into our hands, with "
     "a considerable train of artillery.</p>"),
    ("c-for2", "Foreign Affairs", "Vienna, September 26.",
     "<p>Her Imperial Majesty hath been pleased to order a solemn Te Deum to be "
     "sung in the cathedral, in acknowledgment of the late advantages obtained over "
     "the common adversary; at which the whole court assisted.</p>"),
    ("c-lon1", "London", "London, October 15.",
     "<p>We hear that the merchants trading to the coast of Africa have resolved "
     "to present an humble address of congratulation upon the reduction of the "
     "enemy's settlements, and the security thereby given to the commerce of these "
     "kingdoms.</p><p>Yesterday the sessions ended at the Old Bailey, when seven "
     "prisoners received sentence of death, eleven were ordered for transportation, "
     "and the remainder discharged by proclamation.</p>"),
    ("c-lon2", "London", None,
     "<p>Letters from Portsmouth advise, that the squadron under the command of "
     "Rear Admiral Holmes lay ready to put to sea on the first fair wind, and that "
     "the troops were all embarked in good health and high spirits.</p>"),
    ("c-lon3", "London", None,
     "<p>On Saturday last a fire broke out in a warehouse near Thames-street, "
     "which consumed great quantities of merchandise before it could be subdued; "
     "but we hear of no lives lost.</p>"),
    ("c-cty1", "Country News", "Bristol, October 12.",
     "<p>The fair held here this week was more numerously attended than for some "
     "years past, and the dealers in woollen goods met with a ready vent for their "
     "commodities.</p>"),
    ("c-shp1", "Ship News", "Deal, October 14.",
     "<p>Came down and sailed the Friendship for Lisbon, the Two Brothers for "
     "Oporto, and the Betsey for Jamaica. Remain in the Downs his Majesty's ship "
     "the Centaur, with several merchantmen outward bound. Wind at W. by S.</p>"),
    ("c-shp2", "Ship News", "Gravesend, October 14.",
     "<p>Passed by the Prince of Wales, Captain Bell, from Jamaica; the Hope, "
     "Captain Reed, from Oporto; and the Diligence, Captain Snow, from Rotterdam, "
     "all bound up the river.</p>"),
    ("c-bnk1", "Bankrupts", None,
     "<p>William Wells, of Lombard-street, London, merchant, to surrender the 23d "
     "and 30th of October, and the 24th of November, at Guildhall.</p>"
     "<p>Thomas Hartley, of Leeds, in the county of York, clothier, to surrender "
     "the 29th and 31st of October, and the 24th of November, at Leeds.</p>"),
]


# ---- Петровскія «Вѣдомости» (1703) — кириллица ----------------------------
# Стилизованный под первый русский печатный лист контент (с отголосками реальных
# заметок 1703 г.: пушки, школы, руда на Соку). Лёгкая дореформенная орфография
# (ъ на концах, ѣ в иконных местах); редкие архаичные глифы при необходимости
# подменяются системным шрифтом по-глифно, так что «квадратов» не будет.
_VED_SECTIONS = ["ВѢДОМОСТИ", "ИЗЪ МОСКВЫ", "ИЗЪ ПОЛЬШИ", "О ТОРГѢ"]
_VED_ROWS = [
    ("v-ved1", "ВѢДОМОСТИ", "На Москвѣ.",
     "<p>Повелѣніемъ Его Царскаго Величества вновь нынѣ пушекъ мѣдныхъ, гаубицъ "
     "и мортиръ вылито четыреста. Тѣ пушки ядромъ по двадцати по четыре, по "
     "осьмнадцати и по двѣнадцати фунтовъ, а вѣсомъ въ нихъ мѣди тысяча пудовъ.</p>"
     "<p>Еще на пушечномъ дворѣ многихъ калибровъ припасы готовятъ, и литейному "
     "дѣлу ученики прилежно навыкаютъ, дабы впредь въ томъ художествѣ нужды не было.</p>"),
    ("v-ved2", "ВѢДОМОСТИ", None,
     "<p>Школы московскія умножаются, и сорокъ пять человѣкъ слушаютъ философію, "
     "и діалектику уже окончили. Въ математико-навигацкой школѣ учениковъ болѣе "
     "трехъ сотъ, и навыкаютъ изрядно.</p>"),
    ("v-msk1", "ИЗЪ МОСКВЫ", "Изъ Казани.",
     "<p>На рѣкѣ Сокѣ нашли много нефти и мѣдной руды; изъ той руды мѣдь "
     "выплавили изрядну, отчего чаютъ государству прибыль немалую.</p>"
     "<p>Его Величество указалъ изъ той мѣди и изъ иныхъ припасовъ лить колоколы "
     "и пушки, и мастеровъ къ тому дѣлу приставить искусныхъ.</p>"),
    ("v-msk2", "ИЗЪ МОСКВЫ", None,
     "<p>Изъ Сибири пишутъ: на рѣкахъ сысканы руды серебряныя и желѣзныя, и "
     "заводы вновь заводятъ. Хлѣбъ нынѣ родился доброй, и торгъ мягкою рухлядью "
     "противъ прежнихъ лѣтъ великъ.</p>"),
    ("v-pol1", "ИЗЪ ПОЛЬШИ", "Изо Львова.",
     "<p>Войска коронныя въ собраніи стоятъ, а о замиреніи доселѣ согласія нѣтъ. "
     "Изъ Цесарской земли вѣдомость, что полки въ походъ выступили и магазейны "
     "наполнены.</p>"),
    ("v-pol2", "ИЗЪ ПОЛЬШИ", "Изъ Амстрадама.",
     "<p>Корабли изъ Остъ-Индіи пришли съ богатымъ грузомъ, и купечество о томъ "
     "радуется. Пишутъ такожъ, что въ морѣ были бури великія, отъ чего нѣкоторымъ "
     "судамъ учинилась поруха.</p>"),
    ("v-trg1", "О ТОРГѢ", "Въ Архангельскомъ городѣ.",
     "<p>На ярмонкѣ торгъ былъ великъ: кораблей заморскихъ пришло болѣе ста, и "
     "товары рускіе — пеньку, ленъ, сало и юфть — раскупили съ охотою.</p>"),
    ("v-trg2", "О ТОРГѢ", None,
     "<p>Цѣны на Москвѣ: четверть ржи противъ осени подешевѣла, соль же "
     "вздорожала за дальнимъ провозомъ. О всемъ ономъ впредь обстоятельно "
     "вѣдомо будетъ чинено.</p>"),
]

# ---- Gazette de France (1762) — французский --------------------------------
_GDF_SECTIONS = ["DE PARIS", "D'ALLEMAGNE", "D'ITALIE", "D'ANGLETERRE", "AVIS DIVERS"]
_GDF_ROWS = [
    ("g-par1", "DE PARIS", "De Versailles, le 14 Octobre.",
     "<p>Le Roi a tenu cette semaine son Conseil, et a daigné recevoir les "
     "Ambassadeurs des Puissances étrangères, qui ont été présentés à Sa Majesté "
     "avec les cérémonies accoutumées.</p>"
     "<p>On a chanté un Te Deum dans la Chapelle du Château, en action de grâces "
     "des avantages que les armes du Roi ont remportés sur ses ennemis.</p>"),
    ("g-par2", "DE PARIS", None,
     "<p>L'Académie Royale des Sciences a tenu son assemblée publique, où "
     "plusieurs mémoires sur la navigation et l'astronomie ont été lus, et "
     "reçus avec applaudissement.</p>"),
    ("g-all1", "D'ALLEMAGNE", "De Vienne, le 28 Septembre.",
     "<p>L'Impératrice-Reine a donné audience aux Ministres étrangers. On mande "
     "de l'armée que les troupes ont pris leurs quartiers, et que la campagne "
     "passée s'est terminée sans action générale.</p>"),
    ("g-ita1", "D'ITALIE", "De Rome, le 21 Septembre.",
     "<p>Sa Sainteté a tenu Consistoire, où elle a pourvu plusieurs Églises "
     "vacantes. Le concours des étrangers est grand cette année, à l'occasion "
     "des fêtes solennelles.</p>"),
    ("g-ang1", "D'ANGLETERRE", "De Londres, le 8 Octobre.",
     "<p>Le Parlement doit s'assembler le mois prochain. La flotte qui était "
     "dans la Manche est rentrée dans ses ports, les vaisseaux ayant souffert "
     "des vents contraires.</p>"),
    ("g-avi1", "AVIS DIVERS", None,
     "<p>On fait savoir que la foire de Beaucaire a été cette année très "
     "fréquentée, et que le commerce des soieries y a été considérable.</p>"
     "<p>Il sera incessamment imprimé une nouvelle Carte du Royaume, dressée sur "
     "les dernières observations, que l'on trouvera chez le Sieur Imprimeur.</p>"),
]

# ---- The Pennsylvania Gazette (1750) — английский, колониальный -------------
_PEN_SECTIONS = ["PHILADELPHIA", "LONDON", "FOREIGN ADVICES", "SHIP NEWS", "ADVERTISEMENTS"]
_PEN_ROWS = [
    ("p-phi1", "PHILADELPHIA", "Philadelphia, October 16.",
     "<p>We hear from Lancaster, that the new settlers continue to come in "
     "apace, and that the back country fills with industrious families, to the "
     "great encouragement of trade in these parts.</p>"
     "<p>On Tuesday last the General Assembly met, and after the usual forms "
     "proceeded to the business of the province, the particulars whereof shall "
     "be communicated to our readers in our next.</p>"),
    ("p-phi2", "PHILADELPHIA", None,
     "<p>The new market was on Saturday well supplied with provisions, and the "
     "prices were reasonable; whereby the diligence of our country people is "
     "made manifest to all.</p>"),
    ("p-lon1", "LONDON", "London, August 2.",
     "<p>His Majesty has been pleased to appoint several officers of the "
     "household. The merchants trading to these colonies have presented an "
     "address, setting forth the increase of the American commerce.</p>"),
    ("p-for1", "FOREIGN ADVICES", "Paris, July 28.",
     "<p>The Court continues at Versailles. Letters from the southern provinces "
     "advise of a plentiful harvest, and the rivers being navigable, the "
     "carriage of goods is rendered easy.</p>"),
    ("p-shp1", "SHIP NEWS", "Custom-House, Philadelphia.",
     "<p>Entered inward, the snow Dolphin, Job Trueman, from Barbados; the sloop "
     "Betsey, from Antigua. Cleared out, the brigantine Hope, for Jamaica, and "
     "the ship Carolina, for Bristol.</p>"),
    ("p-adv1", "ADVERTISEMENTS", None,
     "<p>TO BE SOLD, a likely Plantation on the river, containing two hundred "
     "acres, with a good house, barn, and orchard thereon. Enquire of the "
     "Printer hereof.</p>"
     "<p>Just imported, and to be Sold by B. Franklin, a parcel of good Quills, "
     "Dutch Paper, and the best Crown Soap, at reasonable rates.</p>"),
    ("p-adv2", "ADVERTISEMENTS", None,
     "<p>RAN away from the subscriber, a servant man named John; whoever secures "
     "him so that his master may have him again, shall have Twenty Shillings "
     "reward, and reasonable charges.</p>"),
]

# ---- Wiener Zeitung (1703) — немецкий ---------------------------------------
_WIE_SECTIONS = ["Wien", "Aus dem Reiche", "Aus Welschland", "Frankreich", "Vermischte Nachrichten"]
_WIE_ROWS = [
    ("w-wie1", "Wien", "Wien, vom 13. October.",
     "<p>Ihro Kayserliche Majestät haben heute das Geheime Conseil gehalten, und "
     "denen fremden Ministris Audienz ertheilet. Von der Armee wird berichtet, "
     "daß die Völcker in die Winter-Quartiere verleget worden.</p>"
     "<p>Gestern ist der gantze Hof in die Hof-Capelle gegangen, allwo ein "
     "solennes Te Deum Laudamus wegen jüngst erhaltenen Vortheils gesungen worden.</p>"),
    ("w-wie2", "Wien", None,
     "<p>Es sind allhier Briefe aus Ungarn eingelauffen, welche melden, daß die "
     "Gräntz-Festungen wohl versehen, und die Läuffte daselbst ruhig seyen.</p>"),
    ("w-rei1", "Aus dem Reiche", "Regenspurg, vom 5. October.",
     "<p>Auf dem allgemeinen Reichs-Tag wird über die vorgebrachten Puncten "
     "fleißig deliberiret. Die Chur-Fürstlichen Gesandten halten täglich "
     "Conferenzen, und man verhoffet baldige Resolution.</p>"),
    ("w-wel1", "Aus Welschland", "Rom, vom 28. September.",
     "<p>Der Heilige Vater haben ein Consistorium gehalten, und unterschiedliche "
     "erledigte Kirchen besetzet. Der Zulauff fremder Nationen ist dieses Jahr "
     "ungemein groß.</p>"),
    ("w-fra1", "Frankreich", "Paris, vom 1. October.",
     "<p>Der König ist von Fontainebleau wieder anhero gekommen. Die Flotte, so "
     "in dem Canal gekreutzet, ist wegen widriger Winde in die Häfen "
     "eingelauffen.</p>"),
    ("w-ver1", "Vermischte Nachrichten", None,
     "<p>Man schreibet aus Hamburg, daß die Elbe wegen anhaltenden Regens "
     "dermaßen angeschwollen, daß das niedrige Land ringsum unter Wasser stehet.</p>"
     "<p>Aus Holland wird gemeldet, daß die Ost-Indische Compagnie reich "
     "beladene Schiffe glücklich eingebracht habe.</p>"),
]

# Registry of antique "columns" specimens, keyed by theme id. Each carries its
# masthead date line (the SVG masthead supplies the title/sub-title), the ordered
# small-caps section heads, and its period rows. London is the default fallback.
# In production the user's real (e.g. Russian) content flows into the SAME layout.
_SPECIMENS: dict[str, dict] = {
    "london-chronicle": {
        "title": "The London Chronicle", "locale": "en",
        "date": "From SATURDAY, October 13, to TUESDAY, October 16, 1759.",
        "sections": _CHRON_SECTIONS, "rows": _CHRON_ROWS,
    },
    "petrine-vedomosti": {
        "title": "Вѣдомости", "locale": "ru",
        "date": "Печатаны въ Москвѣ, лѣта 1703, генваря въ 2 день.",
        "sections": _VED_SECTIONS, "rows": _VED_ROWS,
    },
    "gazette-de-france": {
        "title": "Gazette de France", "locale": "fr",
        "date": "De Paris, le 16 Octobre 1762.",
        "sections": _GDF_SECTIONS, "rows": _GDF_ROWS,
    },
    "pennsylvania-gazette": {
        "title": "The Pennsylvania Gazette", "locale": "en",
        "date": "PHILADELPHIA: Printed by B. Franklin, October 16, 1750.",
        "sections": _PEN_SECTIONS, "rows": _PEN_ROWS,
    },
    "wiener-zeitung": {
        "title": "Wiener Zeitung", "locale": "de",
        "date": "Wien, den 16. October 1703.",
        "sections": _WIE_SECTIONS, "rows": _WIE_ROWS,
    },
}


def chronicle_render_document(theme_id: str, *, locale: str | None = None, style_overrides: dict | None = None):
    """The antique continuous-column specimen (layout == "columns").

    Picks a period- and language-correct specimen for the theme (Russian for
    petrine-vedomosti, French for gazette-de-france, etc.); unknown ids fall back
    to the London Chronicle. The masthead SVG carries the title; the meta line
    shows only the period date.
    """
    spec = _SPECIMENS.get(theme_id, _SPECIMENS["london-chronicle"])
    loc = locale or spec["locale"]
    cols = min(load_manifest(theme_id).grid.columns, 6)
    stories = [
        Story(id=cid, section=section, kind="standard", headline="",
              dateline=dateline, body_html=body, byline=None,
              source=spec["title"], source_url="#")
        for cid, section, dateline, body in spec["rows"]
    ]
    grid = GridPlan(
        page_format=load_manifest(theme_id).format.page,
        section_order=spec["sections"],
        slots=[
            GridSlot(story_id=cid, section=section, size="medium", columns=cols)
            for cid, section, _dl, _body in spec["rows"]
        ],
    )
    doc = build_render_document(
        issue_id=f"{theme_id}-specimen", theme_id=theme_id, locale=loc,
        title=spec["title"], stories=stories, grid_plan=grid,
        style_overrides=style_overrides or {},
    )
    # The masthead SVG carries the title/Nº; the meta line shows the period date.
    doc.masthead.date = spec["date"]
    return doc


def sample_render_document(theme_id: str, *, locale: str = "ru"):
    """Build a complete RenderDocument for a theme using sample content.

    Uses a fixed generic section_order so the sample GridSlots (which reference
    "world", "business", "tech", "culture") render consistently across every theme.
    Antique "columns" themes get a period-correct continuous-column specimen.
    """
    manifest = load_manifest(theme_id)
    if manifest.format.layout == "columns":
        return chronicle_render_document(theme_id)
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
