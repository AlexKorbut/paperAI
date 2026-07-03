# -*- coding: utf-8 -*-
"""English edition content for the two «Vedomosti» issues — captivating long-form
features (~6 paragraphs) plus a "Sundry News" miscellany, mirroring the Russian
issues. Authored offline in place of the LLM.

Each row: (id, section_id, headline, dateline, body_html).
"""

# --------------------------- ISSUE I — the 3rd of July ---------------------- #
ISSUE1 = [
    ("modeling", "life", "The Night Before the Show", "MILAN.",
     "<p>Three hours before the first look, the old Milanese atelier smelled of hot irons, "
     "coffee and fear. A girl of eighteen from a small town stood at the mirror, repeating "
     "the casting director's only instruction: \"Walk as if you have nothing to prove.\" She "
     "had a great deal to prove — and therein lay the whole difficulty.</p>"
     "<p>Ten years ago she would have been dismissed at a glance: not the right height, not "
     "the copybook regularity of feature. But fashion has tired of perfection. Houses now "
     "hunt for a face that is remembered, not one that dissolves into a row of identical "
     "others; a walk in which character shows, not drill.</p>"
     "<p>The change is driven, too, by the economy of attention. A show long ago ceased to "
     "be a closed rite for the few — it lives in streams and short clips, where what matters "
     "is not statuesque poise but the knack of seizing the eye in a second. Agencies rebuild "
     "portfolios, adding motion, voice and even a stance.</p>"
     "<p>\"The camera forgives much, but not emptiness,\" says an elderly photographer who "
     "has shot for the house for thirty years. He has seen dozens of flawless faces that "
     "left no trace, and one uneven one from which the eye could not be torn. It is such "
     "faces that are prized now.</p>"
     "<p>Behind the curtain a different labour boiled: tailors on their knees pinning a hem, "
     "the make-up artist touching a cheekbone one last time, and in a corner another girl "
     "weeping, not sent out today. Fashion is a feast paid for with someone's tears, and "
     "everyone backstage knows it.</p>"
     "<p>The show lasted eleven minutes. The girl went out, walked, returned — and, "
     "trembling behind the curtain, heard the director toss to his assistant: \"Remember "
     "that one.\" So everything in this trade begins, or ends, in eleven minutes that were "
     "worth a year of waiting.</p>"),

    ("beauty", "life", "The Empty Shelf", "PARIS.",
     "<p>One morning a Parisienne threw eighteen little jars into the bin. Serums, toners, "
     "creams \"for every occasion\" — everything hoarded over the years and promising a "
     "miracle by Friday. Three products remained, and a sudden feeling of freedom.</p>"
     "<p>This is \"skinimalism\" — a quiet revolt against excess. The shopper, worn out by "
     "multi-step rituals, has grown shrewd: she reads the ingredients more closely than the "
     "slogan, and asks not \"what do you promise\" but \"what is in here, and why.\"</p>"
     "<p>Sensing the shift, brands trim their formulas, print honest labels and move to "
     "refillable packaging. Sustainability has stopped being an ornament on the box — it has "
     "become a condition of trust. Make-up artists revive a taste for natural tone and "
     "\"skin that looks like skin.\"</p>"
     "<p>Behind the taste for simplicity lies fatigue with endless choice. When the counter "
     "offers everything at once, calm minimalism reads as luxury; giving up the superfluous "
     "turns out to be not a sacrifice but a relief.</p>"
     "<p>\"Skin is wiser than we are,\" says a cosmetician of twenty years' standing. \"It "
     "needs not thirty products but calm, water and a little sense.\" Her rooms are "
     "half-empty: she deliberately talks clients out of half their purchases — and for that "
     "they only multiply.</p>"
     "<p>Beauty is measured again not by the count of jars but by the feel of well-tended "
     "health. And, it seems, it is precisely that quiet confidence — not the glitter of the "
     "counter — that is the luxury everyone is chasing.</p>"),

    ("health", "life", "Sleep Dearer than Gold", "GENEVA.",
     "<p>The manager of a great firm was proud of sleeping four hours a night. He counted it "
     "a virtue — until one day he forgot the way home. The doctor he came to wrote out no "
     "pill at all. He prescribed sleep.</p>"
     "<p>Researchers rank sleep ever more firmly beside diet and movement. A steady "
     "schedule, morning light and a calm evening give an effect to rival many an advertised "
     "supplement — and cost nothing. Want of sleep, meanwhile, wears a person down quietly, "
     "as water wears stone.</p>"
     "<p>The formula for a long life proved vexingly plain: a few thousand steps a day, "
     "water, vegetables, living company and pauses from the screen. Nothing sensational — "
     "yet it works for years and needs no miracle cure.</p>"
     "<p>Attitudes to exertion are shifting too. The cult of punishing workouts yields to "
     "the idea of a durable habit: a little every day beats a record once a month. The body "
     "answers gratefully to constancy, not to feats.</p>"
     "<p>Physicians increasingly speak of simpler things, forgotten in the craze for "
     "supplements: of quiet, of a walk without a telephone, of talk at a shared table. "
     "\"Loneliness ages faster than sugar,\" one of them remarks — and it is not a metaphor "
     "but a finding.</p>"
     "<p>Six months on, the manager slept seven hours and, for the first time in years, "
     "remembered how yesterday had ended. \"I thought I was losing time,\" he admitted. \"I "
     "was losing myself.\" It is worth remembering, for anyone who wears insomnia like a "
     "medal.</p>"),

    ("trends", "life", "Silence at a Premium", "LONDON.",
     "<p>A wealthy man cut the last visible label from his coat and felt relief. He no "
     "longer needed to shout about himself with a logo — the quality of cloth and cut spoke "
     "more softly and more surely. So \"quiet luxury\" has slipped from runway jargon into "
     "an everyday habit.</p>"
     "<p>Restraint has come to the fore: good materials without monograms, long-lasting "
     "things, a calm palette. Status now reads in the seam and the fit, not in a loud "
     "cipher; showy luxury has become a mark of insecurity.</p>"
     "<p>Alongside it grows a digital asceticism. Deliberate pauses from the feeds, \"quiet\" "
     "telephones and paper notebooks have ceased to be eccentric. Attention is reckoned once "
     "more a precious resource, to be guarded like money and time.</p>"
     "<p>Tailors of the old school say the queues have returned: people mend and remake "
     "instead of throwing away. A thing with a history has suddenly become dearer than a new "
     "but faceless one.</p>"
     "<p>Both fashions are about one thing — a hunger for mastery over an overflowing world. "
     "People choose less, but better: in the wardrobe, in subscriptions, in the objects "
     "about them. And that choice, more and more, is not an abstinence but a pleasure.</p>"
     "<p>Perhaps the chief luxury of the coming age is not possession but freedom from the "
     "superfluous: an empty desk, a quiet evening, and the right not to answer at once. For "
     "that, unlike a logo, one need not be ashamed to pay.</p>"),

    ("china", "world", "A City Without Fumes", "SHENZHEN.",
     "<p>The newcomer steps out of the station and notices first not the towers but the "
     "quiet. The stream of traffic moves almost silently: the buses and taxis of an entire "
     "megacity long ago went over to electric power. The air, acrid not long since, has "
     "become fit for a deep breath.</p>"
     "<p>China electrifies transport with a rare speed. A dense web of high-speed trains has "
     "bound the cities so that medium-haul flights lose their sense: you set off in the "
     "morning and by dinner you are a thousand versts away.</p>"
     "<p>Makers have staked on affordable models, rapid charging and clever electronics. "
     "Exports climb, and with them a world-wide contest for the standards of tomorrow: from "
     "the plug to the very mind of the car.</p>"
     "<p>On the city's edge sprawls a works where the conveyor belts fall silent neither by "
     "day nor by night. Here a car is assembled faster than a guest can drink his tea; and "
     "there are dozens of such works, with more being built.</p>"
     "<p>The display has its underside: questions about the ecology of batteries, the mining "
     "of rare metals, the strain on the grids. The quiet streets of one city are paid for by "
     "the din of quarries in another — and this is said aloud ever more often.</p>"
     "<p>And yet the course is set firmly. It is recutting not only the streets of China but "
     "the sums of carmakers the world over, and whoever misses this train risks being left "
     "on an empty platform.</p>"),

    ("travel", "world", "The Train Instead of the Wing", "LISBON.",
     "<p>He could have flown in two hours, but chose twenty. The night train out of Lisbon "
     "ran along the ocean, and past the window changed fishing villages, vineyards and mist. "
     "By morning the traveller knew more of the country than he would have from a porthole.</p>"
     "<p>The fashion for the unhurried grows. More and more people choose night trains over "
     "flights, long walks over a gallop past the sights, one city over ten. They prize not "
     "the count of pins on the map but the depth of the impression.</p>"
     "<p>Smaller towns gain from the turn. The guest stays longer, spends more thoughtfully, "
     "meets the local kitchen and craft — and returns for the atmosphere, not for a box "
     "ticked on a list of musts.</p>"
     "<p>In the dining car conversations strike up such as never happen on a plane: fellow "
     "passengers manage to tell one another half a life while the time-zones change outside. "
     "The road becomes part of the journey again, not a tiresome pause in it.</p>"
     "<p>The industry adapts: \"no-rush\" routes appear, along with sustainable-travel marks "
     "and services to plan a journey overland. Slowness proves to be not a refusal but a "
     "more honest way of seeing the world.</p>"
     "<p>\"We have forgotten how to arrive,\" says the conductor who has run this train for "
     "thirty years. \"Everyone wants already to be there.\" The train objects with all its "
     "unhurried motion: to be on the way is also to be.</p>"),

    ("belarus", "belarus", "Dawn on the Braslav Lakes", "BRASLAW.",
     "<p>At four in the morning the lake was smooth as quicksilver. The kayak cut the mist "
     "without a sound, and the first ray kindled the water to copper. On the Braslav Lakes "
     "the dawn comes in such a way that one wishes to keep silent about it.</p>"
     "<p>The Braslav Lakes, Belovezhskaya Pushcha and Naroch remain the country's calling "
     "card. Farm-stays, cycling routes and kayaks gather force among those in search of "
     "quiet, clean water and a sky without the city's glare.</p>"
     "<p>Cultural travel rests on the restored castles at Mir and Nesvizh, on the old towns "
     "and monasteries. A short weekend trip has become a familiar rest — no visas, no "
     "flights, a road one can picture.</p>"
     "<p>The keeper of a lakeside farmstead recalls that ten years ago the house stood "
     "empty, and now there is not a free weekend all summer. \"People come for the quiet,\" "
     "he says, \"and carry it home with them, like jam in a jar.\"</p>"
     "<p>The table helps too: local dairies, craft bakeries and farmers' markets turn a "
     "journey into an unhurried tasting. What seemed a backwater proves a land with a taste "
     "and a character of its own.</p>"
     "<p>Domestic travel stops being a fallback and becomes a deliberate choice. It turns "
     "out one need not go to the ends of the earth for wonder — sometimes it is enough to "
     "rise before dawn and slip a boat onto the water.</p>"),

    ("realty", "belarus", "Beyond the Ring Road", "MINSK.",
     "<p>A family with two children saved three years for a flat in the centre, and bought a "
     "house out of town instead — and did not regret it. \"We traded twenty minutes to work "
     "for a yard of our own,\" says the owner. \"And it turned out the yard was worth "
     "more.\"</p>"
     "<p>The housing market stretches visibly beyond the ring road. A house or townhouse in "
     "the suburbs promises space and quiet within a reasonable drive of the centre — and "
     "ever more often beats a cramped flat in dense building.</p>"
     "<p>Within Minsk, compact flats near the metro and move-in-ready finishes hold their "
     "value. The buyer counts not only the price per square metre but the travel time, the "
     "district's amenities and the quality of the courtyard: housing is judged as a way of "
     "life.</p>"
     "<p>Developers answer the demand with new settlements by the forest and the lake, "
     "promising \"the city at arm's length, nature at the window.\" Not every promise comes "
     "true: somewhere the road will be laid late, and the school later still.</p>"
     "<p>Those who know advise weighing the fundamental — transport, schools, green space "
     "and the district's prospects years ahead. It is this, not a passing frenzy, that "
     "decides whether a purchase keeps its worth.</p>"
     "<p>\"A house is bought not for a year but for a life,\" an experienced agent reminds "
     "us. \"And life is lived not within the walls but around them.\" Old-fashioned advice — "
     "but no one has yet paid for taking it.</p>"),

    ("space", "science", "The Rocket That Came Back", "BAIKONUR.",
     "<p>A column of fire lifted the stage into the sky, and eight minutes later that same "
     "stage stood on the pad, whole and hot. Not long ago it seemed a fable; now the return "
     "of a rocket is a working day, to which the idlers have almost ceased to come.</p>"
     "<p>Reusable stages and swarms of small satellites have cut the road to orbit "
     "several-fold. Launches, once rare and bespoke, run now almost in a file, and the price "
     "of lifting a pood of cargo keeps falling.</p>"
     "<p>Scientists await a new generation of telescopes, lunar stations and interplanetary "
     "probes. Private companies vie for state orders, and that rivalry spurs the engineering "
     "mind more than the giant programmes of old.</p>"
     "<p>In the workshops, where yesterday's students assemble stages, there is a smell not "
     "of pathos but of work: solder, metal, strong coffee. Space has ceased to be the "
     "province of superpowers and become the business of stubborn crews.</p>"
     "<p>The boom has its price: near-Earth space empties ever more slowly, and the trouble "
     "of orbital debris moves to the fore. The sky, boundless only yesterday, turns out to "
     "be crowded.</p>"
     "<p>The next frontier is not only to fly but to learn to clean up after oneself. On "
     "whether we manage it depends whether the road to the stars stays open for those who "
     "come after us.</p>"),

    ("flora", "science", "The Trail of the Bison", "BELOVEZHSKAYA PUSHCHA.",
     "<p>The forester raised his hand — and all froze. Forty paces off, between the trunks, "
     "stood a bison: a mountain of muscle and calm, its warm breath a cloud in the morning "
     "chill. A hundred years ago the beast had all but gone. Today it is again the master of "
     "the forest.</p>"
     "<p>The European bison, once reduced almost to nothing, again grazes the protected "
     "woods. Patient recovery programmes have returned thousands of the animals to the wild "
     "— a rare example of a species pulled back from the very edge.</p>"
     "<p>Scientists speak of a wider turn to \"rewilding\": rivers returned to old beds, "
     "meadows and marshes restored, predators cautiously brought back, so that nature holds "
     "its own balance.</p>"
     "<p>The work is unseen and long. Behind each returned bison lie years of counting, of "
     "feeding through the cruel winters, of struggle with poacher and disease. Success is "
     "measured not in loud words but in the number of calves that live to spring.</p>"
     "<p>The forest answers with gratitude: after the great beast returns the small life "
     "too, the wood thickens, the streams revive. It proves enough not to hinder — and "
     "nature herself knows what to do.</p>"
     "<p>The bison shows the essential thing: losses are reversible, if one acts in time and "
     "with obstinacy. And while that warm mountain of muscle stands forty paces off, the "
     "forest — and we — have hope.</p>"),

    ("expeditions", "science", "Beneath the Ice", "ANTARCTICA.",
     "<p>The drill had gone down for three days, and the whole station lived by its hum. "
     "Under four kilometres of ice lay a lake, cut off from the world for hundreds of "
     "thousands of years. A single drop of its water might tell of life where none was "
     "looked for.</p>"
     "<p>International teams drill toward the subglacial lakes through a thickness no man has "
     "seen. Each sample is a message from a sealed world and a hint of where to seek life "
     "beyond the Earth.</p>"
     "<p>Life here is harsh. A short polar summer, frost, wind and fragile machinery dictate "
     "a strict order; a mistake is costly, and help is far. Here they prize not heroics but "
     "reckoning and reliability.</p>"
     "<p>In the evenings, when the drill falls silent, people of a dozen tongues gather in "
     "the mess and warm themselves by a single tea. At the world's edge nationalities blur "
     "faster than in any treatise on the brotherhood of peoples.</p>"
     "<p>It is here that instruments are tested which will one day work on the icy moons of "
     "the planets. Antarctica is a rehearsal of other worlds, not yet to be reached "
     "otherwise.</p>"
     "<p>The expeditions grow ever more open and shared: the data are printed, the samples "
     "divided among laboratories. The great science of the least accessible places rests on "
     "patience and fellowship, not on solitary records.</p>"),

    ("discoveries", "science", "A City Beneath the Dune", "CAIRO.",
     "<p>Overnight the wind blew a metre of sand from a dune — and bared the edge of a wall "
     "three thousand years old. By morning the archaeologists stood over a quarter of a city "
     "of which no chronicle had known. Once again the spade had outrun the books.</p>"
     "<p>Scholars have described the workshops, the seals and the vessels, and the finds "
     "sharpen the chart of ancient trade roads. It appears the links between distant lands "
     "were closer than supposed: things from foreign parts lay here as though at home.</p>"
     "<p>The methods change too. In the laboratories algorithms read faded scrolls, "
     "reassemble potsherds and make out inscriptions, speeding work that once took years. "
     "The dig goes ever more often hand in hand with survey from the air.</p>"
     "<p>Yet the romance has not grown less. The head of the dig confesses he still cannot "
     "sleep the night after a great find: \"You are holding a thing no one has touched for "
     "three thousand years. It is like a handshake across the ages.\"</p>"
     "<p>Behind each find lies not only a sensation but painstaking proof. A true discovery "
     "is born where the spade meets computation, and haste here is the first enemy of "
     "truth.</p>"
     "<p>The city beneath the dune keeps its secrets yet: only a corner has been dug. What "
     "lies under the rest of the sands will be learned, perhaps, not by these scholars but "
     "by those who come after — and in that, too, there is a justice of its own.</p>"),

    ("trends2", "life", "The Return of the Living Sound", "NEW YORK.",
     "<p>In a cramped shop on the corner it smells again of cardboard and dust: people have "
     "come for records. The young, raised on invisible music out of the air, have suddenly "
     "wished to hold it in their hands — a great sleeve, a black disc, the warm hiss of the "
     "needle.</p>"
     "<p>The pull toward the tangible grows with the fatigue of the fleeting. The paper "
     "book, the film photograph, the mechanical watch — everything one can touch, and that "
     "will not vanish at a single tap — is prized once more.</p>"
     "<p>\"People miss the rite,\" says the shopkeeper. \"To put on a record is a decision, "
     "not an accident. You chose to listen, rather than merely let the sound run past.\" In "
     "that choice is the whole of it.</p>"
     "<p>The living sound is imperfect — and dear for that. It asks attention and patience, "
     "and gives in return what convenience cannot buy: the feeling that the music belongs "
     "to you again, and not to the stream.</p>"),

    ("travel2", "world", "Islands Where Time Stands Still", "STOCKHOLM.",
     "<p>Only a small boat reaches the far island, and not every day at that. No cars, no "
     "haste — only wind, stone and the cry of gulls. Those who have once been here return, "
     "as if answering a call.</p>"
     "<p>The traveller nowadays seeks not the noisy capitals but the places where no one "
     "hurries him. Forgotten archipelagos, fishing villages, quiet farmsteads find a second "
     "life — people go to them for the silence, as once they went for luxury.</p>"
     "<p>The keepers of the few homesteads are glad of a guest but guard their way of life: "
     "here they build no hotels into the sky and pave no squares. \"Whoever came for the "
     "quiet,\" they say, \"for him we shall keep the quiet.\"</p>"
     "<p>The slow island teaches the simple things: to watch the water, to wait for the "
     "weather, to rejoice in little. Leaving, the guest carries away not photographs but a "
     "skill grown rare — to be where one stands.</p>"),

    ("space2", "science", "An Eye at the Edge of the Desert", "ATACAMA.",
     "<p>High in the Chilean desert, where the sky is blacker than anywhere on earth, a "
     "giant telescope has opened its eye. Its mirror is wider than a courtyard; the light it "
     "gathers comes to us from stars gone out before man appeared.</p>"
     "<p>A new generation of telescopes peers into such distance and antiquity as the old "
     "ones never dreamed. Scientists hope to see the first light of creation and to catch "
     "the air of alien planets — whether it smells of life.</p>"
     "<p>The work needs silence and darkness, and so observatories flee the city lights into "
     "deserts and mountains. Light pollution has become an enemy of science: to see farther, "
     "one must go farther.</p>"
     "<p>Every clear hour here is counted, and the astronomers guard it dearer than gold. In "
     "the silence of the desert is born a knowledge at which one feels both dread and joy: "
     "we are less and less alone in our ignorance.</p>"),
]

# --------------------------- ISSUE II — the 4th of July --------------------- #
ISSUE2 = [
    ("modeling", "life", "A Face Out of the Algorithm", "PARIS.",
     "<p>On the great screen smiled a girl who does not exist. Flawless skin, a measured "
     "symmetry, not a single pore — a digital avatar assembled overnight. The hall was "
     "silent: some in wonder, some in unease. The question hung of itself — and what now of "
     "the living?</p>"
     "<p>The tools of virtual fitting cheapen production and show a garment on dozens of "
     "types without a costly shoot. The temptation is great: the generation is never late, "
     "never ill, never argues over a fee. The industry tries the novelty warily, but "
     "greedily.</p>"
     "<p>And yet the professionals hold the line. \"The camera catches not a pixel but a "
     "presence,\" says the photographer. \"Until the machine has learned to breathe, it has "
     "no business in the frame.\" The living model answers with what cannot be faked: "
     "weariness, joy, character.</p>"
     "<p>The young models were frightened at first, then grew angry and came out in public: "
     "their faces, their labour, their imperfections had suddenly become a ware that could "
     "be copied. The quarrel over the digital double became, unawares, a quarrel over to "
     "whom a person belongs.</p>"
     "<p>The lawyers spread their hands: the law does not keep pace with the craft. Who owns "
     "a face assembled from a thousand others? And what is left to the living, if an exact "
     "copy can be hired cheaper and without caprice?</p>"
     "<p>It seems the future lies not in the machine replacing the human but in a division "
     "of labour: the routine to the algorithm, and that for which we look at faces at all — "
     "to the human. The rest will be decided not by engineers but by our own taste.</p>"),

    ("beauty", "life", "The Contents, Not the Promise", "GENEVA.",
     "<p>The chemist turned the jar over and smiled: on the label were twenty loud words and "
     "not one useful. \"A pretty box is not a recipe,\" he said. \"The recipe is here, in "
     "the small print that no one reads.\" More and more — they read it.</p>"
     "<p>The shopper has grown shrewd and demands transparency. Brands answer with trimmed "
     "formulas and honest labels; to promise \"eternal youth\" is becoming bad manners. In "
     "place of magic comes a plain chemistry.</p>"
     "<p>Sustainability, once an ornament, has become a condition of purchase. Refillable "
     "packaging, a clear origin of the raw stuff, a refusal of the superfluous — this is "
     "what a whole generation is ready to pay for and to ask after.</p>"
     "<p>\"Label translators\" have appeared — apps and enthusiasts who break down the "
     "contents into plain speech. An industry used to fog is forced to speak straight, and "
     "that heals it better than any cream.</p>"
     "<p>\"The best remedy is the one you did not need,\" the chemist likes to repeat, and "
     "in his mouth it is not coquetry but a professional honesty, rare in a market of "
     "promises.</p>"
     "<p>Behind the modesty of the new regimen lies respect for oneself and for the skin. "
     "Fewer means, more sense: beauty ceases to be a promise from the counter and becomes a "
     "quiet habit of care.</p>"),

    ("health", "life", "Ten Thousand Steps", "LONDON.",
     "<p>A doctor of the old school believes in no miracles, and so prescribes walks. \"The "
     "best medicine I know,\" he says, \"costs nothing and lies at your door.\" His "
     "patients, displeased at first, do not know themselves a month later.</p>"
     "<p>Movement takes back its primacy. The cult of punishing workouts yields to the idea "
     "of a durable habit: a little every day beats a record once a month. The body answers "
     "gratefully to constancy, not to a feat.</p>"
     "<p>To the steps are added the simple things: water, vegetables, living company and "
     "sleep. Nothing sensational — yet it adds up to years of health. Prevention proves "
     "again wiser than heroic cure.</p>"
     "<p>Cities turn slowly toward the walker: here they take a lane from the cars, there "
     "they plant trees and set out benches. It turns out the health of townsfolk is treated "
     "not only in the clinic but on the pavement.</p>"
     "<p>One patient, a retired engineer, took to counting not steps but meetings: with a "
     "neighbour, with the baker, with a duck on the pond. \"It is far merrier so,\" he "
     "laughs, \"and somehow the blood pressure is better.\"</p>"
     "<p>\"Health is not a sprint but a long road,\" the doctor repeats, seeing a patient to "
     "the door. And he counsels not to run after fashion but simply to go out — today, and "
     "not from Monday.</p>"),

    ("trends", "life", "The Telephone in the Drawer", "BERLIN.",
     "<p>On Friday evening she put the telephone in the desk drawer and turned the key. Two "
     "days without feeds, notifications and the opinions of others. By Sunday the world had "
     "not fallen in — instead there returned a quiet she had managed to forget.</p>"
     "<p>Digital asceticism grows as an answer to the fatigue of noise. \"Quiet\" "
     "telephones, paper notebooks and deliberate pauses have ceased to be eccentric. "
     "Attention is owned to be a precious resource, to be guarded.</p>"
     "<p>Beside it goes \"quiet luxury\": quality without logos, long-lasting things, a calm "
     "palette. Both fashions are about one thing — mastery over an overflowing world, and "
     "the right to choose less, but better.</p>"
     "<p>\"Digital monasteries\" have appeared — retreats where at the door one surrenders "
     "the telephone, as once one surrendered a weapon. The demand is such that the booking "
     "runs months ahead: people pay to have taken from them the very thing they paid "
     "for.</p>"
     "<p>Psychologists warn: the matter is not in the device but in the habit. The drawer is "
     "only a crutch; true freedom is to hold the telephone in one's hands and still remain "
     "master of one's attention.</p>"
     "<p>Giving up the superfluous proved not an abstinence but a pleasure. Freeing time and "
     "desk of clutter — digital and material alike — a person sees with wonder how much fits "
     "into a plain, uncluttered life.</p>"),

    ("china", "world", "The Rails of Tomorrow", "BEIJING.",
     "<p>The train set off so smoothly that the glass on the table did not stir, and a "
     "minute later the needle already showed above three hundred versts an hour. Past the "
     "window the fields ran together; cities neared and passed like stations of the "
     "underground. Distances in China have ceased to daunt.</p>"
     "<p>A dense web of high-speed roads has bound the megacities so that medium-haul "
     "flights lose their sense. Morning coffee in one city, dinner in another — a commonplace, "
     "not an adventure.</p>"
     "<p>With the rails comes electric transport too: silent buses, clean air, affordable "
     "cars. Exports climb, and with them the contest for the standards by which half the "
     "world will ride.</p>"
     "<p>They build on a scale the world has not seen: bridges across gorges, tunnels "
     "through mountains, stations the size of a town. Engineers speak of records as of "
     "everyday things, as though of laying a path in a garden.</p>"
     "<p>The scale has its reverse: debts, strain on the grids, questions about the ecology "
     "of production. Not every line will pay for itself, and of this there is ever more "
     "dispute even at home.</p>"
     "<p>And yet the course is set, and the rails of tomorrow are already laid. It remains "
     "only to accelerate along them — and those who chase will have to run very fast not to "
     "be left behind for good.</p>"),

    ("travel", "world", "One City", "VIENNA.",
     "<p>He came for a week and did not once leave the city bounds. No list of sights, no "
     "haste — only one city, learned to the crack in the pavement. By the week's end he knew "
     "his neighbours at the coffee-house by name.</p>"
     "<p>Deep travel comes into fashion. Instead of a gallop through ten capitals — one "
     "city, lived unhurriedly: the market in the mornings, the same park, talk with the "
     "locals. So one learns a place, not its postcards.</p>"
     "<p>From the turn the provinces gain, and the quiet quarters of great cities. The guest "
     "stays longer and spends more thoughtfully, and the hosts answer with a hospitality "
     "that cannot be bought in the tourist row.</p>"
     "<p>He took to returning to one café at one hour — and the city opened to him from "
     "within: the waiter became an adviser, a chance neighbour a friend, an unknown street "
     "his own. The journey turned into a short but real life.</p>"
     "<p>\"A tourist is always leaving, even when he stands still,\" the café's keeper "
     "remarked. \"And you, it seems, have arrived.\" Higher praise for a wanderer there is, "
     "perhaps, not.</p>"
     "<p>Slowness turns into a luxury of attention. One city truly seen gives more than ten "
     "run past in haste — and stays with you long after the return.</p>"),

    ("belarus", "belarus", "The Castle Comes to Life", "NESVIZH.",
     "<p>Under the vaults where music sounded three hundred years ago, an orchestra plays "
     "again. Nesvizh Castle, having outlived wars and desolation, meets its guests in "
     "restored halls. The past here is not behind glass — one may breathe it.</p>"
     "<p>Cultural travel rests on the restored castles at Mir and Nesvizh, on the old towns "
     "and monasteries. A short weekend trip has become a familiar rest — no visas and no "
     "flights, a road one can picture.</p>"
     "<p>Beside it the nature of the region revives too: the Braslav Lakes, Naroch, the "
     "forest. Farm-stays and cycling routes beckon those who seek quiet and clean water. The "
     "country proves more interesting than its own people had thought.</p>"
     "<p>The restorers work with an eye to antiquity: they match the paint to the fallen "
     "layers, rebuild the parquet by old drawings. \"We do not build the new,\" says a "
     "master, \"we wake the sleeping.\" And the castle answers.</p>"
     "<p>In the evenings plays and concerts are given in the courtyard; children run where "
     "once princes walked. History ceases to be a dull lesson and becomes a living place, to "
     "which one wishes to return.</p>"
     "<p>The table helps: dairies, bakeries, farmers' markets. Domestic travel stops being a "
     "fallback and becomes a deliberate choice — with a castle on the horizon and a lake "
     "round the bend.</p>"),

    ("realty", "belarus", "A Metre by the Metro", "MINSK.",
     "<p>A young couple chose between a roomy flat on the outskirts and a cramped one by the "
     "very station of the metro. They chose the cramped — and won an hour of life each day. "
     "\"We bought not metres,\" they laugh, \"but time.\"</p>"
     "<p>In the city, compact flats near the metro and turn-key finishes are prized. The "
     "buyer counts not only the price per metre but the road, the amenities and the quality "
     "of the courtyard: housing is ever more judged as a way of life.</p>"
     "<p>Meanwhile demand stretches visibly beyond the ring road too: a house or townhouse "
     "promises space and quiet. City and suburb seem to come to terms, dividing the buyer by "
     "cast of character.</p>"
     "<p>The young reckon otherwise than their fathers: nearness to work, café and park "
     "matters to them more than square metres. A flat has become not a fortress for life but "
     "a convenient point, easy to change at need.</p>"
     "<p>Agents note the buyer has grown particular over trifles — the light, the noise, the "
     "neighbours. \"Bare metres\" can no longer be sold; a way of life is sold, and whoever "
     "grasped this is the winner.</p>"
     "<p>Those who know counsel one thing: to weigh the fundamental — transport, schools, "
     "greenery, the district's prospects years ahead. It is this, not a passing frenzy, that "
     "decides whether a purchase keeps its worth.</p>"),

    ("space", "science", "Debris in Orbit", "BAIKONUR.",
     "<p>On the screen of the control centre a swarm of thousands of points circled the "
     "Earth — the fragments of rockets and dead satellites, each at the speed of a bullet. "
     "\"One day we may lock ourselves in,\" the engineer said quietly, and the hall grew "
     "uneasy.</p>"
     "<p>Cheap access to orbit has turned into its crowding. Reusable stages and swarms of "
     "small satellites have cheapened the road to space, but near-Earth space fills faster "
     "than it empties.</p>"
     "<p>The trouble of orbital debris moves to the fore. Engineers design \"scavengers\" — "
     "craft to catch fragments and bring them down from orbit. The task is harder than many "
     "a flight: to strike a target flying faster than a bullet.</p>"
     "<p>One blow breeds a cloud of splinters, each a new threat. Scientists fear a chain "
     "reaction after which certain orbits will be impassable for generations. It is no "
     "fancy but a reckoning, and it alarms.</p>"
     "<p>To agree is hard: the sky is common, the flags many. Who pays to clear away what "
     "all have launched? While the nations argue, the debris grows, and time works against "
     "them all at once.</p>"
     "<p>The next frontier is not only to fly but to learn to clean up after oneself. On "
     "whether we manage depends whether the sky above us stays a road — or turns to a "
     "rubbish heap under lock and key.</p>"),

    ("flora", "science", "The River Returns", "POLESIE.",
     "<p>The excavator took its last scoop — and the water, a hundred years locked in a "
     "straight canal, poured into the old winding bed. Within a year the birds, the fish and "
     "the beavers returned, as though they had waited round the bend. The river remembered "
     "what it had been.</p>"
     "<p>\"Rewilding\" gathers force: rivers returned to old beds, meadows and marshes "
     "restored, vanished beasts cautiously brought back. The idea is simple — to let nature "
     "herself hold the balance, rather than mend her by hand.</p>"
     "<p>The marshes, drained for a century, are owned again to be a treasure: they hold "
     "water, store carbon and feed a countless living. What seemed a waste proved a working "
     "heart of the land.</p>"
     "<p>Not all are glad of the change: one has lost a field, another a familiar road. "
     "Scientists learn to speak not only with nature but with people, for without the "
     "consent of the dwellers no river will flow in peace.</p>"
     "<p>And yet the examples multiply, and each persuades better than any report. Where the "
     "concrete retreats, within a few years returns a life that was thought lost for "
     "good.</p>"
     "<p>Success takes decades and patience. But example upon example proves the essential "
     "thing: losses are reversible, if one acts in time. Nature answers care faster than we "
     "dare to hope.</p>"),

    ("expeditions", "science", "A Summer a Month Long", "ANTARCTICA.",
     "<p>They had a month. Exactly a month of polar summer to do what elsewhere would be "
     "given a year. Every clear day was worth its weight in gold, every storm a stolen week. "
     "The expedition lived by a clock that nature herself wound.</p>"
     "<p>The logistics at the world's end are merciless. A short summer, frost, wind and "
     "fragile machinery dictate a strict order; the least mistake is costly, and help is "
     "far. Here they prize not heroics but reckoning and reliability.</p>"
     "<p>And still people go — for samples of subglacial water, for data on the climate, for "
     "the testing of instruments that will one day work on the icy moons. Every grain of "
     "knowledge is paid for in cold and patience.</p>"
     "<p>When a storm comes on, the station freezes for days: the link breaks, the windows "
     "drift over, and there is nothing to do but wait. In such hours one grasps how thin the "
     "line is between science and plain survival on this white silence.</p>"
     "<p>But let the sky clear — and all are at the instruments again, making up for lost "
     "time. In this race with the clock and the cold is born a knowledge not to be had in "
     "the warmth of a study.</p>"
     "<p>The expeditions grow ever more shared and open: the samples divided among "
     "laboratories, the data printed. The great science of the least accessible places rests "
     "on fellowship, not on solitary records — else here one does not survive.</p>"),

    ("discoveries", "science", "A Scroll Read by the Machine", "OXFORD.",
     "<p>The scroll was charred two thousand years ago and would crumble at a touch. It was "
     "not unrolled — it was \"read\" through, layer by layer, by beam and reckoning. On the "
     "screen there came out letters no one had seen since the days of Rome.</p>"
     "<p>Algorithms change archaeology more quietly, but more deeply, than the dig. They "
     "read faded texts, reassemble potsherds and make out inscriptions, speeding work that "
     "once took years. The past comes nearer by the distance of a computation.</p>"
     "<p>The finds sharpen the chart of ancient links: things and words travelled farther "
     "than was thought. The world of the past proves closer and more alive than the dry "
     "textbooks drew it.</p>"
     "<p>The young researchers argue with the old: some trust the machine, others only the "
     "spade and the eye. The truth, as ever, lies between, and is born in that honest "
     "quarrel, not in the hush of one mind.</p>"
     "<p>The first lines read out proved to be neither a poem nor a law, but a household "
     "note on a delivery of grain. And in that plainness is its own wonder: across two "
     "thousand years it is not a hero who addresses us, but a simple scribe.</p>"
     "<p>A true discovery is born where the ancient spade meets the newest machine. The "
     "scroll has spoken — and reminded us that the past waits patiently until we grow wise "
     "enough to overhear it.</p>"),

    ("health2", "life", "The Apothecary in the Garden Bed", "KYOTO.",
     "<p>A woman of a hundred years on the edge of Kyoto knows no medicines: her apothecary "
     "is the garden behind the house. Vegetables in their season, a little fish, a cup of "
     "tea and an unhurried day — that is the whole secret over which scholars write whole "
     "volumes.</p>"
     "<p>Science confirms ever more often the old wisdom: plain food, movement and measure "
     "keep a person surer than many a physic. Where people eat less and simpler, they live "
     "longer and merrier.</p>"
     "<p>The secret is not in rare herbs but in constancy and moderation. \"Rise from the "
     "table a little hungry,\" the old woman counsels, and in that rule is more good than in "
     "a dear apothecary.</p>"
     "<p>Long life, it turns out, grows not in the laboratory but in the garden bed and at "
     "the shared table. And perhaps the chief medicine has been one from of old — to live "
     "unhurriedly and with thanks.</p>"),

    ("china2", "world", "The City That Never Sleeps", "HONG KONG.",
     "<p>At midnight the city burns brighter than other capitals at noon. The shops are "
     "open, the kitchens smoke, the crowd flows along the streets as though it did not know "
     "that night exists. Here they trade, eat and toil at any hour.</p>"
     "<p>Night life is not idleness but a husbandry: whole trades are fed by the city's not "
     "going dark. Messengers, cooks, hawkers bear on their shoulders an unseen labour, "
     "without which the day would not have become the day.</p>"
     "<p>But the sleepless city has its price too: weariness, crowding, an eternal noise. "
     "Ever more voices are heard that the megacity also should learn to rest, and the human "
     "in it — to sleep.</p>"
     "<p>The East shows the world an image of the future — seething, bright and without "
     "respite. There remains the question they ask here too: does all that does not sleep "
     "live — or does the rest simply not dare to stop?</p>"),

    ("flora2", "science", "The Falcon's Return", "THE CARPATHIANS.",
     "<p>From a high crag a falcon threw itself and fell like a stone into the abyss — to "
     "spread its wings at the very ground and soar. Half a century ago these birds were gone "
     "from here entirely. Now they trace the sky above the ridge again.</p>"
     "<p>Birds of prey are returned patiently: the chicks are reared, the nests guarded, the "
     "young taught to hunt. The work is long and unseen, and the reward is the shadow of a "
     "wing gliding once more down the slope.</p>"
     "<p>With the upper hunter in place the whole forest comes into tune: the small beasts "
     "multiply, the slopes revive, the balance strengthens. Nature, like an orchestra, "
     "sounds true only when every voice is in its place.</p>"
     "<p>The falcon over the Carpathians is not merely a bird but a sign: where nature was "
     "given room, she returns of herself, fairer and faster than one dared to hope. One need "
     "only not hinder.</p>"),
]


# ------------------------- "Sundry News" — issue I -------------------------- #
MISC1 = [
    ("m1a", "misc", "Silk Grows Cheaper", "LYON.", "<p>At the autumn fair the price of good silk fell for the first time in years: the weavers grumble, the buyers rejoice, and the knowing advise no haste — by spring it may all turn about.</p>"),
    ("m1b", "misc", "A Full House", "VIENNA.", "<p>The new opera plays to packed halls a third week running; tickets are sought from hand to hand, and their price climbs faster than that of bread.</p>"),
    ("m1c", "misc", "A Bridge Is Raised", "PRAGUE.", "<p>A new foot-bridge has opened over the river; the townsfolk came in a throng to be the first across, and till evening it was more crowded than the square.</p>"),
    ("m1d", "misc", "Coffee in Vogue", "PARIS.", "<p>Coffee-houses multiply on every street; in some they sit past midnight over disputes of politics and verse, and the keepers do not complain.</p>"),
    ("m1e", "misc", "A Good Harvest", "HAMBURG.", "<p>From the country round they write of a bountiful harvest of rye and barley; the granaries are full, and the price of flour promises to fall by winter.</p>"),
    ("m1f", "misc", "A Striking Clock", "GENEVA.", "<p>A master has shown a pocket-watch of unheard-of accuracy; it loses, they say, no more than a minute a week, which none before would credit.</p>"),
    ("m1g", "misc", "The Birds Return", "NAROCH.", "<p>To the lakes the migrant birds have come before their time; the fishermen count it a good sign and foretell a warm autumn.</p>"),
    ("m1h", "misc", "The Road Is Stuck", "SMOLENSK.", "<p>After the rains the high-road is so churned that the wagons stand a third day; the merchants are vexed, while the innkeepers by the road are, on the contrary, content.</p>"),
    ("m1i", "misc", "A Book Sold Out", "LEIPZIG.", "<p>A new learned work sold out in a week; the press hastily prepares a second run, and the author, they say, is himself astonished.</p>"),
    ("m1j", "misc", "A Garden Opened", "MINSK.", "<p>In the town a new public garden has been laid with avenues and benches; of an evening half the town already walks there, from the least to the greatest.</p>"),
    ("m1k", "misc", "The Fish Run Large", "BRASLAW.", "<p>The fishermen boast an uncommon catch; some pike, they say, are an arm's length long, which at market some believe and some laugh at.</p>"),
    ("m1l", "misc", "Learning in Fashion", "MOSCOW.", "<p>The number eager for the sciences grows; not only youths but men of years ask to enter the schools, which once was held a marvel.</p>"),
    ("m1m", "misc", "Mild Weather", "RIGA.", "<p>Days uncommonly warm hold on; the old folk do not recall the like at this season and wonder what winter will bring.</p>"),
    ("m1n", "misc", "Craft Is Prized", "TULA.", "<p>For a good smith there is now a queue; masters are paid in advance, if only the work be sound and not swift — the taste for the solid has returned.</p>"),
    ("m1o", "misc", "A Star Is Seen", "OXFORD.", "<p>The astronomers announce a new comet; on clear nights it is seen with the naked eye low above the horizon, and the curious do not sleep.</p>"),
    ("m1p", "misc", "The Honey Yields", "POLESIE.", "<p>The bee-keepers praise an abundant flow; there is so much honey that the price has fallen, and housewives hasten to lay in a store for all the winter.</p>"),
    ("m1q", "misc", "Flax Thrives", "VITEBSK.", "<p>The flax stands tall and clean this year; buyers from over the sea already price it, and the owners are in no haste to yield, awaiting a better rate.</p>"),
    ("m1r", "misc", "A Toll Lifted", "GRODNO.", "<p>From certain dues at market there came relief; the shopkeepers cheered, and the row that stood empty has come alive again with the cries of hawkers.</p>"),
    ("m1s", "misc", "A Mill Set Going", "MOGILEV.", "<p>On the river a new mill of three runs of stone has been set going; it grinds the flour quickly, and the queue to it stands from daybreak.</p>"),
    ("m1t", "misc", "A Physician Praised", "VIENNA.", "<p>A young physician heals without bleeding, by rest and herbs, and, to the wonder of his elders, his patients rise the sooner.</p>"),
    ("m1u", "misc", "A Ship Comes In", "ARKHANGELSK.", "<p>From distant lands a ship has come with spice and cloth; on the quay there is a press, and the price of the curiosities bites.</p>"),
    ("m1v", "misc", "A Fire Put Out", "DRESDEN.", "<p>By night a granary caught; the folk who ran up saved the neighbouring roofs. The loss is great, but of lives, by good fortune, there are none.</p>"),
    ("m1w", "misc", "Music Is Printed", "LEIPZIG.", "<p>The press has taken up the notes of new music; amateurs snatch up the sheets, and of an evening there sounds in homes what yesterday was only in the halls.</p>"),
    ("m1x", "misc", "A Cheese in Fame", "NESVIZH.", "<p>The local dairy took the prize at the fair; for its cheese they now come from afar, and the mistress scarcely keeps up with the orders.</p>"),
    ("m1y", "misc", "A Road Is Paved", "POLOTSK.", "<p>The high-road is being clad in stone, verst upon verst; the wagons will go the faster, and the merchants already count the days it saves.</p>"),
    ("m1z", "misc", "Chicks Hatched", "NAROCH.", "<p>Among the rare birds of the lakes chicks have hatched; the wardens rejoice and ask guests to leave those places undisturbed till autumn.</p>"),
    ("m1aa", "misc", "A Mason in Demand", "REVAL.", "<p>For a good mason the demand is great; the towns are building, and the master chooses his commission, not the commission its master.</p>"),
    ("m1bb", "misc", "Salt Grows Cheap", "STARAYA RUSSA.", "<p>New salt-works gave so much salt that the price has fallen; the housewives are glad, and the salters seek new buyers over the sea.</p>"),
    ("m1cc", "misc", "Pigeons Bred", "BRUGES.", "<p>The merchants have bred carrier pigeons and send their news swifter than a courier; some wonder, and some already take up the custom.</p>"),
    ("m1dd", "misc", "A Tree Is Set Up", "NUREMBERG.", "<p>For the winter feasts a decked little tree is set up in the homes; the custom is young but has been taken quickly to heart by old and small alike.</p>"),
    ("m1ee", "misc", "A Dyke Is Strengthened", "LEIDEN.", "<p>After the high water the dyke is mended by the whole town; old and young work at it, for the sea does not care to jest.</p>"),
    ("m1ff", "misc", "Hops Thrive", "ZATEC.", "<p>The hops this year are fragrant and plentiful; the brewers rub their hands and promise by winter a drink such as has not been tasted in an age.</p>"),
    ("m1gg", "misc", "Horses Are Shod", "KHOLMOGORY.", "<p>Before the sledge-road the forges do not stand idle; the horse is shod to the frost-nail, that it may go over the ice surely and not to its rider's fright.</p>"),
    ("m1hh", "misc", "Weavers Dispute", "GHENT.", "<p>Between the guilds there arose a dispute over the price of cloth; the elders met in council and, they say, made peace by evening.</p>"),
]

# ------------------------- "Sundry News" — issue II ------------------------- #
MISC2 = [
    ("m2a", "misc", "A Manufactory Grows", "MANCHESTER.", "<p>A new manufactory has taken on another hundred hands; work grows, and with it the dispute whether the workmen are paid enough.</p>"),
    ("m2b", "misc", "A Noisy Fair", "NIZHNY.", "<p>The autumn fair has gathered merchants from sea to sea; so much ware has been brought that the rows have no visible end, nor the trading a beginning.</p>"),
    ("m2c", "misc", "A Canal Is Dug", "AMSTERDAM.", "<p>A new canal has opened, and the barges take the shorter way; the merchants reckon the gain, the boatmen the loss, for the roundabout had fed them.</p>"),
    ("m2d", "misc", "Bread Grows Cheap", "DANZIG.", "<p>After a good harvest the price of bread has fallen; the poor breathe easier, while the corn-dealers are downcast — not to every man is a boon a boon.</p>"),
    ("m2e", "misc", "A Swift Mare", "NEWMARKET.", "<p>At the races a young mare passed all by three lengths; her owner is in glory, and those who laid against her in loss and vexation.</p>"),
    ("m2f", "misc", "Clearer Glass", "MURANO.", "<p>The glass-blowers have shown a glass of unheard-of clearness; through it, they say, one sees as through the air, and the price of the wonder is no small one.</p>"),
    ("m2g", "misc", "The Rain Refreshes", "POLTAVA.", "<p>After the drought good rains have passed; the fields revived, and the tillers, but yesterday downcast, are now full of hope for the winter corn.</p>"),
    ("m2h", "misc", "A Street Is Paved", "KIEV.", "<p>The main street is being clothed in stone; there is less dust and mire, yet such a din of the work that the neighbours count the days to its end.</p>"),
    ("m2i", "misc", "A Singer Is Sought", "NAPLES.", "<p>A young singer is sought by one court after another; his voice, they say, is such that even stern hearts are not left dry.</p>"),
    ("m2j", "misc", "The Forest Guarded", "BELOVEZHA.", "<p>New protected tracts have been proclaimed; felling there is forbidden, that beast and bird may multiply without hindrance.</p>"),
    ("m2k", "misc", "Mills Multiply", "LODZ.", "<p>The town grows with mills so fast that housing is short; they build in haste, and the price of a corner climbs month upon month.</p>"),
    ("m2l", "misc", "A Bridge Is Raised", "LONDON.", "<p>For the first time a lifting span of the bridge was tried; the crowd gaped as the mass rose, letting a ship through, and clapped the masters.</p>"),
    ("m2m", "misc", "The Grape Ripens", "BORDEAUX.", "<p>The vintage promises a glorious year; the vine-growers are content, and the knowing already dispute which is to be the better — last year's or this.</p>"),
    ("m2n", "misc", "Swifter Print", "NUREMBERG.", "<p>An improved press prints twice as fast as before; more books come out, and their price, to the joy of the learners, slowly falls.</p>"),
    ("m2o", "misc", "The Canal Freezes", "STOCKHOLM.", "<p>Early ice has stood on the canals; children already try their skates, while the boatmen have put by their oars till spring and mend their tackle.</p>"),
    ("m2p", "misc", "A Chapel Raised", "VILNA.", "<p>On a hill by the road a chapel has been set up; wayfarers stop to rest, and the place, once desolate, has come alive with human talk.</p>"),
    ("m2q", "misc", "Tobacco Dearer", "BREMEN.", "<p>The price of foreign tobacco has risen; the smokers grumble, and some, with a wave of the hand, give up the harmful habit — to the joy of their households.</p>"),
    ("m2r", "misc", "A Clock on the Tower", "BRUGES.", "<p>On the town tower a new clock with chimes has been set; every hour a music floats over the square, and the townsfolk gather to hear it.</p>"),
    ("m2s", "misc", "Oats Grow Cheap", "KOVNO.", "<p>After a good mowing the price of oats has fallen; the drivers are content, for the horse's feed is cheaper, and the road more profitable.</p>"),
    ("m2t", "misc", "A School Opened", "PINSK.", "<p>A new school has opened in the town; so many are eager for letters that a second teacher had to be hired before the first snow.</p>"),
    ("m2u", "misc", "A Bridge Mended", "ORSHA.", "<p>The old bridge, which threatened to fall, has been strengthened with new piles; the wagons go straight across again, sparing the distant ford.</p>"),
    ("m2v", "misc", "A New Rose", "HAARLEM.", "<p>A gardener has bred a rose of an unheard-of colour; for its cuttings there is a queue, and the price asked is fit for a rare stone.</p>"),
    ("m2w", "misc", "The Catch Is Good", "GDANSK.", "<p>The fishermen boast a rich run of herring; the barrels are full, and the merchants hasten to salt a store while the cool weather holds.</p>"),
    ("m2x", "misc", "A Library Given", "VILNA.", "<p>A wealthy burgher has given the town his collection of books; henceforth any may read, and the hall does not stand empty from the morning.</p>"),
    ("m2y", "misc", "Copper Is Found", "FALUN.", "<p>In the old mine they have struck a new vein of copper; work has grown, and with it the hopes of a whole small town for a good year.</p>"),
    ("m2z", "misc", "The Stork Returns", "POLESIE.", "<p>To the old nest by the village a stork has returned; the peasants count it a lucky sign and guard the nest more dearly than before.</p>"),
    ("m2aa", "misc", "Lanterns Are Lit", "PARIS.", "<p>On the main streets night lanterns have been set; the passers-by go bolder in the dark, and to the footpad it is no longer a joy.</p>"),
    ("m2bb", "misc", "The River Opens", "NARVA.", "<p>The ice on the rapids has passed, and the floating is open; the logs go down with the water, and on the wharves it is loud and busy again.</p>"),
    ("m2cc", "misc", "An Apothecary Founded", "UPPSALA.", "<p>At the college an apothecary with rare herbs has opened; the students learn the trade, and the townsfolk come for counsel and for physic.</p>"),
    ("m2dd", "misc", "A Bell Is Cast", "MOSCOW.", "<p>The masters have cast a bell of unheard-of weight; to raise it to the belfry they gather the folk, and the work promises to be no quick one.</p>"),
    ("m2ee", "misc", "Sheepskin in Use", "CRACOW.", "<p>Toward the cold the demand for sheepskin has risen; the furriers toil day and night, and the price of a good coat has come to bite.</p>"),
    ("m2ff", "misc", "The Orchard Bears", "ALMA.", "<p>The young orchards have given their first heavy fruit; there are so many apples they are carted by the load, and the scent stands over a whole district.</p>"),
    ("m2gg", "misc", "A Shipyard Laid", "TOULON.", "<p>A new shipyard has been laid, and the knock of axes does not fall silent; the shipwrights gather from every quarter to a good wage.</p>"),
    ("m2hh", "misc", "A Spring Blessed", "ZHYROVICHY.", "<p>By the abbey a new spring has been blessed; for its clean water they come from afar, and the path to the source does not grow over.</p>"),
]


MISC2 += [
    ("m2ii", "misc", "A Lighthouse Lit", "BREST.", "<p>On the headland a new lighthouse has been lit; the fishermen bless it, for many a boat was lost on that shoal in the dark of autumn nights.</p>"),
    ("m2jj", "misc", "Amber on the Shore", "PALANGA.", "<p>After the storms the sea threw much amber on the sand; the gatherers were out by dawn, and by noon not a clear piece was left for a latecomer.</p>"),
    ("m2kk", "misc", "A Fair for Horses", "LEIPZIG.", "<p>The horse-fair drew dealers from three lands; a good trotter went for a price that set the whole row talking till evening.</p>"),
    ("m2ll", "misc", "New Locks Fitted", "WOLVERHAMPTON.", "<p>A smith has shown locks no picklock, they say, can master; the cautious order them for their coffers, and the price is no small one.</p>"),
    ("m2mm", "misc", "The Vintage Casked", "OPORTO.", "<p>The new wine is casked and set to rest; the growers promise a year to be remembered, and the cellars are full to the vaults.</p>"),
    ("m2nn", "misc", "A Weathervane Set", "ROSTOCK.", "<p>On the town hall a gilded weathervane has been set; the children below name the winds by it, and the old sailors nod their approval.</p>"),
    ("m2oo", "misc", "Paper Grows Cheaper", "BASLE.", "<p>New mills have brought the price of paper down; the printers rejoice, and pamphlets multiply so that the criers scarce keep up.</p>"),
    ("m2pp", "misc", "A Menagerie Shown", "THE HAGUE.", "<p>A travelling menagerie has come to town; folk crowd to see beasts of far lands, and the keeper counts his coppers with a smile.</p>"),
    ("m2qq", "misc", "The Marsh Drained", "ELY.", "<p>A stretch of fen has been drained for tillage; some praise the new fields, others mourn the fowl, and the dispute is not yet settled.</p>"),
    ("m2rr", "misc", "A Comet Named", "GREENWICH.", "<p>The astronomers have given the new comet a name and reckon its course; the almanacs are reprinted, and the curious watch the eastern sky.</p>"),
    ("m2ss", "misc", "Wool Fetches High", "SEGOVIA.", "<p>Fine wool fetches a high price this season; the shepherds are content, and the clothiers grumble that good cloth will cost the dearer for it.</p>"),
]
