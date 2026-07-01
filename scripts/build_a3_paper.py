#!/usr/bin/env python3
"""Full multi-page A3 newspaper with big feature articles, in the four antique
`columns` themes, Russian and English. Long-form editorial copy below is authored
in place of the LLM stage (offline, no API key).

The 12 interests are grouped into rubrics (section heads); under each rubric sit
several full articles (headline + dateline + long body) that flow across columns
and pages. Rendered on A3 via throwaway theme copies (committed themes stay A4).

Usage:  PYTHONPATH=src python scripts/build_a3_paper.py
Outputs: .data/showcase_a3/<theme>__<lang>.pdf  + dumps docs for previews.
"""
from __future__ import annotations

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

THEMES = ["petrine-vedomosti", "gazette-de-france", "pennsylvania-gazette", "wiener-zeitung"]
OUT = ROOT / ".data" / "showcase_a3"
OUT.mkdir(parents=True, exist_ok=True)
JSONDIR = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/a3docs")
JSONDIR.mkdir(parents=True, exist_ok=True)
A3_THEMES = Path("/tmp/claude-0/-home-user-paperAI/24fb00ed-6707-5b54-87ce-eaef729a0b30/scratchpad/themes_a3")

# Section rubrics, in reading order.
SECTIONS = [
    dict(id="life",    ru="СТИЛЬ ЖИЗНИ",     en="LIFESTYLE"),
    dict(id="world",   ru="МИР",             en="THE WORLD"),
    dict(id="belarus", ru="БЕЛАРУСЬ",        en="BELARUS"),
    dict(id="science", ru="НАУКА И ПРИРОДА", en="SCIENCE & NATURE"),
]

# id, section, ru/en {head, dl, body}. Bodies are 3–4 real paragraphs → big articles.
ARTICLES = [
    dict(id="modeling", section="life",
        ru=dict(head="Подиум учится у улицы", dl="МИЛАН.",
            body="<p>Модельный бизнес переживает тихую, но глубокую перестройку. Ещё десять лет "
                 "назад индустрия держалась на нескольких безупречных типажах; сегодня кастинг "
                 "стал заметно разнообразнее — по возрасту, росту, происхождению и фактуре лица. "
                 "Бренды всё чаще ищут не идеальные пропорции, а узнаваемую индивидуальность и "
                 "живую подачу, которая считывается в кадре за долю секунды.</p>"
                 "<p>Перемены подстёгивает и экономика внимания. Показ давно перестал быть закрытым "
                 "ритуалом для избранных: он живёт в трансляциях и коротких роликах, где важна не "
                 "столько статуарность, сколько характер и умение держать историю. Агентства "
                 "перестраивают портфолио, добавляя к классическим съёмкам движение, голос и даже "
                 "публичную позицию модели.</p>"
                 "<p>Отдельная тема — цифровые аватары и виртуальная примерка. Технологии удешевляют "
                 "производство и позволяют показать вещь на десятках типажей без дорогой съёмки. "
                 "Но профессионалы напоминают: камера по-прежнему ценит живого человека, и никакая "
                 "генерация пока не заменяет обаяния, которое возникает между моделью и объективом.</p>"),
        en=dict(head="The Runway Learns from the Street", dl="MILAN.",
            body="<p>The modelling trade is undergoing a quiet but deep reset. A decade ago the "
                 "industry rested on a handful of flawless types; today casting is markedly more "
                 "diverse — in age, height, origin and the texture of a face. Houses increasingly "
                 "seek a recognisable individuality and a living presence that reads on camera in a "
                 "fraction of a second, rather than perfect proportion.</p>"
                 "<p>The attention economy sharpens the shift. A show long ago ceased to be a closed "
                 "rite for the few: it lives in streams and short clips, where character and the "
                 "ability to carry a story matter more than statuesque poise. Agencies are rebuilding "
                 "portfolios, adding movement, voice and even a public stance to the classic shoot.</p>"
                 "<p>Digital avatars and virtual try-on are a chapter of their own. The technology "
                 "lowers production costs and shows a garment on dozens of body types without an "
                 "expensive shoot. Yet professionals caution that the camera still prizes a living "
                 "person, and no amount of generation replaces the charm that arises between a model "
                 "and the lens.</p>"),
    ),
    dict(id="beauty", section="life",
        ru=dict(head="Меньше значит лучше", dl="ПАРИЖ.",
            body="<p>На смену многоступенчатым ритуалам приходит «скинимализм»: короткий, честный "
                 "уход и внимание к барьеру кожи вместо десятка баночек. Покупатель поумнел — он "
                 "читает состав внимательнее, чем рекламный слоган, и спрашивает не «что обещаете», "
                 "а «что внутри».</p>"
                 "<p>Марки отвечают сокращёнными формулами, прозрачной маркировкой и перезаряжаемой "
                 "упаковкой. Экологичность перестала быть украшением на этикетке и стала условием "
                 "покупки для целого поколения. Визажисты тем временем возвращают моду на "
                 "естественный тон, мягкий блеск и «кожу, похожую на кожу».</p>"
                 "<p>За модой на простоту стоит и усталость от избытка. Когда витрина предлагает "
                 "бесконечный выбор, спокойный минимализм воспринимается как роскошь. Красота всё "
                 "чаще измеряется не количеством средств, а ощущением ухоженного здоровья.</p>"),
        en=dict(head="Less, but Better", dl="PARIS.",
            body="<p>Elaborate multi-step routines are giving way to \"skinimalism\": a short, honest "
                 "regimen and care for the skin barrier instead of a dozen jars. The shopper has "
                 "grown shrewd, reading the ingredient list more closely than the slogan and asking "
                 "not what is promised but what is inside.</p>"
                 "<p>Brands answer with pared-down formulas, transparent labelling and refillable "
                 "packaging. Sustainability has stopped being an ornament on the box and become a "
                 "condition of purchase for a whole generation. Make-up artists, meanwhile, revive a "
                 "taste for natural tone, a soft sheen and skin that looks like skin.</p>"
                 "<p>Behind the taste for simplicity lies fatigue with excess. When the shelf offers "
                 "endless choice, calm minimalism reads as luxury. Beauty is increasingly measured "
                 "not by the count of products but by the feel of well-tended health.</p>"),
    ),
    dict(id="health", section="life",
        ru=dict(head="Сон возвращает себе статус", dl="ЖЕНЕВА.",
            body="<p>Исследователи всё увереннее ставят сон в один ряд с питанием и движением. "
                 "Регулярный режим, утренний свет и спокойный вечер дают эффект, сравнимый с иными "
                 "разрекламированными добавками, — и достаются бесплатно.</p>"
                 "<p>Врачи повторяют простую формулу долголетия: несколько тысяч шагов в день, вода, "
                 "овощи, живое общение и паузы от экрана. Ничего сенсационного, зато работает годами "
                 "и не требует чудо-средств. Профилактика снова важнее героического лечения.</p>"
                 "<p>Меняется и отношение к нагрузке. На смену культу изнурительных тренировок "
                 "приходит идея устойчивой привычки: лучше немного и каждый день, чем рекорд раз в "
                 "месяц. Здоровье перестаёт быть проектом на спринт и становится длинной дистанцией.</p>"),
        en=dict(head="Sleep Reclaims Its Status", dl="GENEVA.",
            body="<p>Researchers increasingly rank sleep alongside diet and movement. A steady "
                 "schedule, morning light and a calm evening can rival many an advertised supplement "
                 "in effect — and cost nothing.</p>"
                 "<p>Physicians repeat a plain formula for a long life: a few thousand steps a day, "
                 "water, vegetables, real company and pauses from the screen. Nothing sensational, "
                 "yet it works over years and needs no miracle cure. Prevention again outranks "
                 "heroic treatment.</p>"
                 "<p>Attitudes to exertion are shifting too. The cult of punishing workouts yields to "
                 "the idea of a durable habit: a little every day beats a monthly record. Health "
                 "stops being a sprint project and becomes a long-distance one.</p>"),
    ),
    dict(id="trends", section="life",
        ru=dict(head="Тихая роскошь и цифровой аскетизм", dl="ЛОНДОН.",
            body="<p>На первый план выходит сдержанность: качественные материалы без логотипов, "
                 "долговечные вещи и спокойная палитра. «Тихая роскошь» из подиумного термина стала "
                 "бытовой привычкой — статус теперь считывается по крою и ткани, а не по яркой "
                 "монограмме.</p>"
                 "<p>Рядом крепнет цифровой аскетизм. Осознанные паузы от лент и уведомлений, "
                 "«тихие» телефоны и бумажные блокноты перестали быть чудачеством. Внимание снова "
                 "считают ценным ресурсом, который стоит беречь так же, как деньги или время.</p>"
                 "<p>Оба тренда об одном — о желании контроля над избыточным миром. Люди выбирают "
                 "меньше, но лучше: в гардеробе, в подписках, в вещах вокруг. И этот выбор всё чаще "
                 "становится не жертвой, а удовольствием.</p>"),
        en=dict(head="Quiet Luxury and Digital Restraint", dl="LONDON.",
            body="<p>Restraint is ascendant: good materials without logos, long-lasting pieces and a "
                 "calm palette. \"Quiet luxury\" has slipped from runway jargon into an everyday "
                 "habit — status now reads in cut and cloth, not a loud monogram.</p>"
                 "<p>Alongside it grows a digital asceticism. Deliberate pauses from feeds and "
                 "notifications, \"quiet\" phones and paper notebooks have ceased to be eccentric. "
                 "Attention is again treated as a resource to guard as carefully as money or time.</p>"
                 "<p>Both trends speak to one wish — control over an overflowing world. People choose "
                 "less but better: in the wardrobe, in subscriptions, in the objects around them. And "
                 "that choice is ever less a sacrifice and ever more a pleasure.</p>"),
    ),
    dict(id="china", section="world",
        ru=dict(head="Китай пересаживается на ток", dl="ШЭНЬЧЖЭНЬ.",
            body="<p>Городской транспорт Китая электрифицируется с редкой скоростью. Автобусы и такси "
                 "целых мегаполисов уже перешли на электротягу, а плотная сеть скоростных поездов "
                 "связала города так, что перелёты на средние расстояния теряют смысл.</p>"
                 "<p>Производители сделали ставку на доступные модели, быструю зарядку и умную "
                 "электронику. Экспорт растёт, и вместе с ним — глобальная конкуренция за стандарты "
                 "завтрашнего дня: от разъёмов до программного обеспечения автомобиля.</p>"
                 "<p>За технологической витриной стоит и обратная сторона — вопросы к экологии "
                 "производства батарей и к нагрузке на электросети. Но направление задано, и оно "
                 "меняет не только улицы Китая, но и расчёты автопрома по всему миру.</p>"),
        en=dict(head="China Switches to Current", dl="SHENZHEN.",
            body="<p>China's urban transport is electrifying at a rare pace. Buses and taxis of whole "
                 "megacities have already gone electric, and a dense web of high-speed trains has "
                 "bound cities so tightly that medium-haul flights lose their point.</p>"
                 "<p>Makers have bet on affordable models, rapid charging and clever electronics. "
                 "Exports climb, and with them a global contest to set tomorrow's standards — from "
                 "plugs to the software that runs the car.</p>"
                 "<p>Behind the technological display lies a flip side too: questions over the ecology "
                 "of battery making and the strain on power grids. But the direction is set, and it is "
                 "reshaping not only China's streets but the sums of carmakers worldwide.</p>"),
    ),
    dict(id="travel", section="world",
        ru=dict(head="Медленные маршруты входят в моду", dl="ЛИССАБОН.",
            body="<p>Путешественники всё чаще выбирают неспешность: ночные поезда вместо перелётов, "
                 "долгие прогулки вместо галопа по достопримечательностям, один город вместо десяти. "
                 "Ценят не количество отметок на карте, а глубину впечатления.</p>"
                 "<p>От такого поворота выигрывают малые города и провинция. Гость остаётся дольше, "
                 "тратит осмысленнее, знакомится с местной кухней и ремеслом — и возвращается за "
                 "атмосферой, а не за галочкой в списке обязательного.</p>"
                 "<p>Индустрия подстраивается: появляются маршруты «без спешки», сертификаты "
                 "устойчивого туризма и сервисы, которые помогают спланировать поездку по земле. "
                 "Медленность оказывается не отказом, а более честным способом видеть мир.</p>"),
        en=dict(head="Slow Routes Come into Fashion", dl="LISBON.",
            body="<p>Travellers increasingly choose to dawdle: night trains instead of flights, long "
                 "walks instead of a gallop past the sights, one city instead of ten. They prize "
                 "depth of impression over a tally of pins on the map.</p>"
                 "<p>Smaller towns and the provinces gain from the shift. The guest lingers, spends "
                 "more thoughtfully, meets the local kitchen and craft — and returns for atmosphere "
                 "rather than a box ticked on a list of musts.</p>"
                 "<p>The industry adapts: \"no-rush\" itineraries appear, along with sustainable-travel "
                 "labels and services that help plan a journey overland. Slowness turns out to be not "
                 "a refusal but a more honest way to see the world.</p>"),
    ),
    dict(id="belarus", section="belarus",
        ru=dict(head="Озёрный край зовёт", dl="МИНСК.",
            body="<p>Браславские озёра, Беловежская пуща и Нарочь остаются визитной карточкой "
                 "страны. Агроусадьбы, веломаршруты и байдарки набирают популярность у тех, кто ищет "
                 "тишину, чистую воду и небо без городской засветки.</p>"
                 "<p>Культурный туризм держится на восстановленных замках в Мире и Несвиже, на "
                 "старых местечках и монастырях. Короткая поездка на выходные становится привычным "
                 "форматом отдыха — без виз, без перелётов, с понятной дорогой.</p>"
                 "<p>Развитию помогает и гастрономия: локальные сыроварни, крафтовые пекарни и "
                 "фермерские рынки превращают путешествие по стране в неспешную дегустацию. "
                 "Внутренний туризм перестаёт быть запасным вариантом и становится осознанным "
                 "выбором.</p>"),
        en=dict(head="The Lakeland Beckons", dl="MINSK.",
            body="<p>The Braslav Lakes, Belovezhskaya Pushcha and Naroch remain the country's calling "
                 "card. Farm-stays, cycling routes and kayaks win over those in search of quiet, "
                 "clean water and a sky free of city glare.</p>"
                 "<p>Cultural travel rests on the restored castles at Mir and Nesvizh, on old towns "
                 "and monasteries. A short weekend trip becomes a familiar form of rest — no visas, "
                 "no flights, a road one can picture.</p>"
                 "<p>Food helps too: local dairies, craft bakeries and farmers' markets turn a journey "
                 "across the country into an unhurried tasting. Domestic travel stops being a fallback "
                 "and becomes a deliberate choice.</p>"),
    ),
    dict(id="realty", section="belarus",
        ru=dict(head="Спрос смещается за город", dl="МИНСК.",
            body="<p>Рынок жилья заметно тянется за кольцевую. Частный дом или таунхаус в пригороде "
                 "обещает пространство, двор и тишину при разумной дороге до центра — и всё чаще "
                 "выигрывает у тесной квартиры в плотной застройке.</p>"
                 "<p>В самом Минске ценятся компактные квартиры у метро и готовая отделка «под "
                 "ключ». Покупатель считает не только цену метра, но и время в пути, инфраструктуру "
                 "района и качество двора — жильё оценивают как образ жизни, а не как квадратные "
                 "метры.</p>"
                 "<p>Аналитики советуют не гнаться за модой, а смотреть на фундаментальное: транспорт, "
                 "школы, зелёные зоны и перспективу района на годы вперёд. Именно эти факторы, а не "
                 "сиюминутный ажиотаж, определяют, сохранит ли покупка ценность.</p>"),
        en=dict(head="Demand Shifts Out of Town", dl="MINSK.",
            body="<p>The housing market is stretching visibly beyond the ring road. A house or "
                 "townhouse in the suburbs promises space, a yard and quiet within a reasonable "
                 "commute of the centre — and ever more often beats a cramped flat in dense "
                 "development.</p>"
                 "<p>Within Minsk, compact flats near the metro and move-in-ready finishes hold their "
                 "value. The buyer counts not only the price per square metre but travel time, the "
                 "district's amenities and the quality of the courtyard — housing is judged as a way "
                 "of life, not as floor area.</p>"
                 "<p>Analysts advise chasing fundamentals rather than fashion: transport, schools, "
                 "green space and a district's prospects years ahead. Those factors, not a passing "
                 "frenzy, decide whether a purchase keeps its worth.</p>"),
    ),
    dict(id="space", section="science",
        ru=dict(head="Частные ракеты открывают орбиту", dl="БАЙКОНУР.",
            body="<p>Многоразовые ступени и рои малых спутников удешевили доступ к орбите в разы. "
                 "Запуски, ещё недавно редкие и штучные, идут теперь почти конвейером, а стоимость "
                 "вывода килограмма груза продолжает падать.</p>"
                 "<p>Учёные ждут нового поколения телескопов, лунных станций и межпланетных зондов. "
                 "Частные компании спорят за государственные контракты, и эта конкуренция ускоряет "
                 "инженерную мысль сильнее, чем прежние программы-гиганты.</p>"
                 "<p>У бурного роста есть и цена: околоземное пространство пустеет всё медленнее, а "
                 "проблема космического мусора и переполненных орбит выходит на первый план. "
                 "Следующий рубеж — не только долететь, но и научиться убирать за собой.</p>"),
        en=dict(head="Private Rockets Open the Orbit", dl="BAIKONUR.",
            body="<p>Reusable stages and swarms of small satellites have cut the cost of reaching "
                 "orbit several-fold. Launches, rare and bespoke not long ago, now run almost on a "
                 "conveyor, and the price of lifting a kilogram keeps falling.</p>"
                 "<p>Scientists await a new generation of telescopes, lunar stations and interplanetary "
                 "probes. Private firms vie for state contracts, and that rivalry speeds engineering "
                 "more than the giant programmes of old.</p>"
                 "<p>The boom has its price: near-Earth space empties ever more slowly, and the problem "
                 "of orbital debris and crowded lanes moves to the fore. The next frontier is not only "
                 "to fly but to learn to clean up after oneself.</p>"),
    ),
    dict(id="flora", section="science",
        ru=dict(head="Возвращение зубра", dl="БЕЛОВЕЖСКАЯ ПУЩА.",
            body="<p>Европейский зубр, некогда почти исчезнувший, снова пасётся в заповедных лесах. "
                 "Терпеливые программы восстановления вернули в природу тысячи животных — редкий "
                 "пример того, как вид удаётся вытащить с самого края.</p>"
                 "<p>Экологи говорят о более широком повороте к «переосвоению»: возвращают реки в "
                 "старые русла, восстанавливают луга и болота, осторожно возвращают хищников, чтобы "
                 "природа сама поддерживала равновесие без постоянного вмешательства человека.</p>"
                 "<p>Успех не гарантирован и требует десятилетий, но пример зубра показывает главное: "
                 "утраты обратимы, если действовать вовремя и настойчиво. Дикая природа отвечает на "
                 "заботу быстрее, чем принято думать.</p>"),
        en=dict(head="The Bison Returns", dl="BIALOWIEZA FOREST.",
            body="<p>The European bison, once nearly lost, again grazes the protected woods. Patient "
                 "recovery programmes have returned thousands of the animals to the wild — a rare "
                 "example of a species pulled back from the very edge.</p>"
                 "<p>Ecologists speak of a wider turn to \"rewilding\": rivers returned to old beds, "
                 "meadows and marshes restored, predators cautiously brought back, so that nature "
                 "keeps its own balance without constant human hand.</p>"
                 "<p>Success is not guaranteed and takes decades, yet the bison shows the essential "
                 "thing: losses are reversible if one acts in time and with persistence. Wild nature "
                 "answers care faster than is commonly thought.</p>"),
    ),
    dict(id="expeditions", section="science",
        ru=dict(head="Под лёд Антарктиды", dl="АНТАРКТИДА.",
            body="<p>Международные группы бурят к подлёдным озёрам, скрытым под многокилометровой "
                 "толщей. Каждая проба воды из мира, отрезанного от поверхности сотни тысяч лет, "
                 "может рассказать о жизни в экстремальных условиях — и о том, где её искать за "
                 "пределами Земли.</p>"
                 "<p>Логистика остаётся суровой. Короткое полярное лето, мороз, ветер и хрупкая "
                 "техника диктуют жёсткий график; ошибка стоит дорого. Именно здесь проверяют "
                 "приборы, которым однажды предстоит работать на ледяных спутниках планет.</p>"
                 "<p>Экспедиции всё чаще становятся международными и открытыми: данные публикуют, "
                 "образцы делят между лабораториями. Большая наука о самых недоступных местах Земли "
                 "держится на терпении и сотрудничестве, а не на одиночных рекордах.</p>"),
        en=dict(head="Beneath the Antarctic Ice", dl="ANTARCTICA.",
            body="<p>International teams drill toward subglacial lakes hidden under kilometres of ice. "
                 "Each sample of water from a world cut off from the surface for hundreds of thousands "
                 "of years may speak of life in extreme conditions — and of where to seek it beyond "
                 "Earth.</p>"
                 "<p>The logistics stay harsh. A short polar summer, frost, wind and fragile equipment "
                 "dictate a strict schedule; a mistake is costly. It is here that instruments are "
                 "tested which will one day work on the icy moons of the planets.</p>"
                 "<p>Expeditions are ever more international and open: data are published, samples "
                 "shared among laboratories. Big science about Earth's least accessible places rests "
                 "on patience and cooperation, not on solitary records.</p>"),
    ),
    dict(id="discoveries", section="science",
        ru=dict(head="Древний город под песками", dl="КАИР.",
            body="<p>Археологи описали кварталы поселения, скрытого под барханами. Мастерские, печати "
                 "и утварь уточняют карту древних торговых путей и показывают, что связи между "
                 "далёкими землями были теснее, чем считалось.</p>"
                 "<p>Меняются и методы. В лабораториях алгоритмы помогают читать выцветшие свитки, "
                 "складывать черепки и распознавать надписи, ускоряя работу, на которую прежде "
                 "уходили годы. Раскопки всё чаще сопровождаются съёмкой с воздуха и трёхмерными "
                 "моделями.</p>"
                 "<p>За каждой находкой — не только сенсация, но и кропотливая проверка. Настоящее "
                 "открытие рождается на стыке лопаты и вычислений, и именно этот союз делает "
                 "археологию одной из самых живых наук наших дней.</p>"),
        en=dict(head="An Ancient City Beneath the Sands", dl="CAIRO.",
            body="<p>Archaeologists have mapped the quarters of a settlement buried under the dunes. "
                 "Workshops, seals and vessels sharpen the chart of old trade roads and show that "
                 "links between distant lands were closer than supposed.</p>"
                 "<p>Methods are changing too. In the laboratories, algorithms help read faded "
                 "scrolls, reassemble potsherds and recognise inscriptions, speeding work that once "
                 "took years. Digs are ever more often paired with aerial survey and three-dimensional "
                 "models.</p>"
                 "<p>Behind each find lies not only a headline but painstaking verification. A true "
                 "discovery is born where the spade meets computation, and it is that union which "
                 "makes archaeology one of the liveliest sciences of our day.</p>"),
    ),
]

_SEC_NAME = {s["id"]: s for s in SECTIONS}


def prepare_a3_themes() -> Path:
    if A3_THEMES.exists():
        shutil.rmtree(A3_THEMES)
    shutil.copytree(ROOT / "themes", A3_THEMES)
    for t in THEMES:
        toml = A3_THEMES / t / "theme.toml"
        txt = toml.read_text(encoding="utf-8")
        txt = re.sub(r'(?m)^(page\s*=\s*)"a4"', r'\1"a3"', txt)
        toml.write_text(txt, encoding="utf-8")
    return A3_THEMES


def stories_for(lang: str) -> tuple[list[Story], list[str]]:
    order = [s[lang] for s in SECTIONS]
    src = "Утренняя газета" if lang == "ru" else "The Morning Paper"
    out: list[Story] = []
    for a in ARTICLES:
        c = a[lang]
        sec_name = _SEC_NAME[a["section"]][lang]
        out.append(
            Story(id=a["id"], section=sec_name, kind="feature",
                  headline=c["head"], dateline=c["dl"], body_html=c["body"],
                  byline=None, source=src, source_url="#")
        )
    # keep article order grouped by section order
    out.sort(key=lambda s: order.index(s.section))
    return out, order


def build(theme: str, lang: str, renderer: NodeRenderer):
    man = load_manifest(theme)
    sts, order = stories_for(lang)
    cols = min(man.grid.columns, 6)
    grid = GridPlan(
        page_format="a3", section_order=order,
        slots=[GridSlot(story_id=s.id, section=s.section, size="medium", columns=cols) for s in sts],
    )
    title = "Утренняя газета" if lang == "ru" else "The Morning Paper"
    edition = "Выпуск по интересам" if lang == "ru" else "Interests Edition"
    doc = build_render_document(
        issue_id=f"{theme}-{lang}-a3", theme_id=theme, locale=lang,
        title=title, stories=sts, grid_plan=grid, edition=edition,
    )
    (JSONDIR / f"{theme}__{lang}.json").write_text(doc.model_dump_json(), encoding="utf-8")
    res = renderer.render(doc, out_path=OUT / f"{theme}__{lang}.pdf")
    print(f"{theme:22} {lang}  -> {theme}__{lang}.pdf  ({res.page_count} pp A3)")


def main() -> None:
    a3 = prepare_a3_themes()
    renderer = NodeRenderer(themes_dir=a3)
    for theme in THEMES:
        for lang in ("ru", "en"):
            build(theme, lang, renderer)


if __name__ == "__main__":
    main()
