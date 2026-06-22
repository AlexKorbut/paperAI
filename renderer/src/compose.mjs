// Compose a full HTML document from a RenderDocument + a theme bundle.
// Content is theme-agnostic; all visual decisions come from themes/<id>/.

import { readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { parse as parseToml } from "smol-toml";
import { fontFaceCss } from "./fonts.mjs";
import { prepareImages } from "./images.mjs";

const PAGE_SIZES = {
  a4: "210mm 297mm",
  a3: "297mm 420mm",
  letter: "8.5in 11in",
  broadsheet: "11in 22in",
  tabloid: "11in 17in",
};

function esc(s) {
  return String(s ?? "").replace(
    /[&<>"]/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
  );
}

function cssVarsBlock(manifest) {
  const g = manifest.grid || {};
  const t = manifest.type || {};
  const c = manifest.colors || {};
  const vars = {
    "--paper": c.paper || "#fff",
    "--ink": c.ink || "#000",
    "--accent": c.accent || "#000",
    "--masthead-font": `"${t.masthead_font}"`,
    "--headline-font": `"${t.headline_font}"`,
    "--body-font": `"${t.body_font}"`,
    "--columns": String(g.columns ?? 6),
    "--rule-weight": g.rule_weight || "1px",
    "--gutter": g.gutter || "10px",
  };
  // Optional per-theme type tokens (override base.css readability defaults).
  const typeTokens = {
    "--scale": t.scale_factor,
    "--leading": t.leading,
    "--body-size": t.body_pt,
    "--fs-masthead": t.masthead_pt,
    "--fs-lead": t.lead_pt,
    "--fs-headline": t.headline_pt,
    "--fs-dominant": t.dominant_pt,
    "--fs-feature": t.feature_pt,
  };
  for (const [k, v] of Object.entries(typeTokens)) {
    if (v !== undefined && v !== null && v !== "") vars[k] = String(v);
  }
  const body = Object.entries(vars)
    .map(([k, v]) => `  ${k}: ${v};`)
    .join("\n");
  // One theme per document, so plain :root (data-theme lives on <body>, which a
  // :root[data-theme] selector would NOT match — that was a latent no-op).
  return `:root {\n${body}\n}`;
}

// Per-user reading-comfort overrides — emitted AFTER theme CSS so the user wins.
const _OVERRIDE_VARS = {
  scale: "--scale",
  leading: "--leading",
  accent: "--accent",
  body_size: "--body-size",
  body_font: "--body-font",
  headline_font: "--headline-font",
  masthead_font: "--masthead-font",
};

function userVarsBlock(manifest, overrides) {
  if (!overrides || typeof overrides !== "object") return "";
  const lines = [];
  for (const [key, cssVar] of Object.entries(_OVERRIDE_VARS)) {
    const v = overrides[key];
    if (v === undefined || v === null || v === "") continue;
    lines.push(`  ${cssVar}: ${key.endsWith("_font") ? `"${v}"` : v};`);
  }
  if (overrides.dropcap === false) {
    lines.push("  --dropcap-size: 1em;", "  --dropcap-float: none;");
  }
  if (!lines.length) return "";
  return `:root {\n${lines.join("\n")}\n}`;
}

function pageRule(manifest) {
  const fmt = manifest.format || {};
  const size = PAGE_SIZES[fmt.page || "a4"] || PAGE_SIZES.a4;
  const orient = fmt.orientation === "landscape" ? " landscape" : "";
  const bleed = Number(fmt.bleed_mm || 0);
  const marks = bleed > 0 ? "\n  marks: crop cross;" : "";
  const bleedRule = bleed > 0 ? `\n  bleed: ${bleed}mm;` : "";
  return `@page {\n  size: ${size}${orient};${bleedRule}${marks}\n}`;
}

// Screen-only overrides for the responsive web edition: centre the "sheet", give
// it depth, and collapse the dense print columns as the viewport narrows so the
// same content reads comfortably on a phone. Print/PDF is unaffected (@media screen).
function webCss() {
  return `@media screen {
  html, body { background: #e9e9ee; -webkit-text-size-adjust: 100%; }
  main.paper {
    max-width: 1100px;
    margin: 24px auto;
    padding: 32px;
    background: var(--paper);
    box-shadow: 0 2px 28px rgba(0,0,0,0.18);
  }
  .story__photo img { max-width: 100%; height: auto; }
}
@media screen and (max-width: 820px) {
  .section__grid, .lead .story__body { column-count: 2 !important; }
  main.paper > .front { grid-template-columns: repeat(2, 1fr); }
  main.paper > .front > .story { grid-column: 1 / -1; }
  main.paper > .front > .story .story__body { column-count: 2 !important; }
}
@media screen and (max-width: 560px) {
  .section__grid, .lead .story__body { column-count: 1 !important; }
  main.paper > .front { grid-template-columns: 1fr; }
  main.paper > .front > .story .story__body { column-count: 1 !important; }
  main.paper { padding: 18px; margin: 0; }
  .masthead__title, .masthead__logo svg { font-size: 11vw; max-height: 14vw; }
  .lead .story__headline { font-size: 8vw; }
}`;
}

const SIZE_TO_ROLE = { lead: "feature", medium: "standard", brief: "brief" };

// Text columns INSIDE a story module (mirrors GridSlot.effective_story_cols).
function effStoryCols(slot) {
  if (slot.story_cols != null) return Math.max(1, slot.story_cols);
  const role = slot.role || SIZE_TO_ROLE[slot.size] || "standard";
  if (slot.dominant) return Math.max(1, Math.min(4, Math.floor(slot.columns / 2)));
  if (["brief", "teaser", "sidebar", "factbox"].includes(role)) return 1;
  return Math.max(1, Math.min(3, Math.floor(slot.columns / 2)));
}

function storyArticle(view, slot) {
  if (!view) return "";
  const role = slot.role || SIZE_TO_ROLE[slot.size] || "standard";
  // `lead` (bare) lets themes' `.lead ...` rules style the dominant module.
  const dominant = slot.dominant ? " story--dominant lead" : "";
  // Keep the legacy size class (themes style off it) + add role/furniture classes.
  const cls = `story story--${slot.size} story--role-${role}${dominant}`;
  const span = `--span:${slot.columns}; --row-span:${slot.row_span || 1}; --story-cols:${effStoryCols(slot)}`;

  const kicker = view.kicker
    ? `<p class="story__kicker">${esc(view.kicker)}</p>`
    : "";
  const headline = `<h2 class="story__headline">${esc(view.headline)}</h2>`;

  // A teaser ("анонс") is the same story rendered small: kicker + headline +
  // one teaser line + a refer arrow, no body or photo.
  if (role === "teaser" || slot.body_policy === "teaser_only") {
    const tt = view.teaser_text || view.deck || "";
    return `<article class="${cls} story--teaser" style="${span}">
  ${kicker}
  ${headline}
  ${tt ? `<p class="story__teaser">${esc(tt)}</p>` : ""}
  <p class="story__refer">${esc(view.byline || "Подробнее внутри")} <span class="story__refer-arrow">&#8594;</span></p>
</article>`;
  }

  const photo =
    slot.with_photo && view.image_ref
      ? `<figure class="story__photo"><img src="${esc(view.image_ref)}" alt=""/>${
          view.caption ? `<figcaption>${esc(view.caption)}</figcaption>` : ""
        }</figure>`
      : "";
  const deck = view.deck ? `<p class="story__deck">${esc(view.deck)}</p>` : "";
  const byline = view.byline ? `<p class="story__byline">${esc(view.byline)}</p>` : "";
  const quote = slot.pull_quote
    ? `<blockquote class="story__pull">${esc(slot.pull_quote)}</blockquote>`
    : "";
  // Dateline runs in to the first paragraph: "MINSK — The story begins…".
  let body = view.body_html || "";
  if (view.dateline) {
    const run = `<span class="story__dateline">${esc(view.dateline)}</span> `;
    body = /^\s*<p[^>]*>/i.test(body) ? body.replace(/^(\s*<p[^>]*>)/i, `$1${run}`) : run + body;
  }
  // body_html is trusted newspaper-register HTML produced by our own editorial stage.
  return `<article class="${cls}" style="${span}">
  ${kicker}
  ${headline}
  ${deck}
  ${byline}
  ${photo}
  ${quote}
  <div class="story__body">${body}</div>
</article>`;
}

function renderSections(doc) {
  const slots = doc.grid_plan.slots;
  const order =
    doc.grid_plan.section_order && doc.grid_plan.section_order.length
      ? doc.grid_plan.section_order
      : [...new Set(slots.map((s) => s.section))];

  const isFront = (s) => s.front !== false;
  const frontSlots = slots.filter(isFront);
  const flowSlots = slots.filter((s) => !isFront(s));

  // FRONT PAGE: one modular CSS-Grid mosaic. Dominant first (full-bleed), then
  // the rest tile by column span. Kickers carry the section, so no big section
  // bands here — it reads like a real front page. Kept to one page (break-after).
  const dominant = frontSlots.find((s) => s.dominant);
  const ordered = dominant ? [dominant, ...frontSlots.filter((s) => s !== dominant)] : frontSlots;
  const frontItems = ordered
    .map((s) => storyArticle(doc.stories[s.story_id], s))
    .join("\n");
  const frontHtml = frontSlots.length ? `<div class="front">${frontItems}</div>` : "";

  // FLOW continuation (pages 2+): remaining stories grouped into sections, each a
  // multi-column flow — Paged.js-safe (no grid cell spans a page break).
  const sections = order
    .map((sec) => {
      const ss = flowSlots.filter((s) => s.section === sec);
      if (!ss.length) return "";
      const items = ss.map((s) => storyArticle(doc.stories[s.story_id], s)).join("\n");
      return `<section class="section section--${esc(sec)}">
  <h3 class="section__title">${esc(sec)}</h3>
  <div class="section__grid">${items}</div>
</section>`;
    })
    .join("\n");
  const flowHtml = sections.trim() ? `<div class="flow">${sections}</div>` : "";

  return frontHtml + "\n" + flowHtml;
}

export async function composeHtml(doc, { themesDir, assetsDir, rendererDir, web = false }) {
  const warnings = [];
  const themeDir = path.join(themesDir, doc.theme_id);
  const manifestPath = path.join(themeDir, "theme.toml");
  if (!existsSync(manifestPath)) {
    throw new Error(`theme not found: ${doc.theme_id} (${manifestPath})`);
  }
  const manifest = parseToml(await readFile(manifestPath, "utf-8"));

  const baseCss = await readFile(
    path.join(themesDir, "_base", "base.css"),
    "utf-8"
  );
  const themeCssPath = path.join(themeDir, "theme.css");
  const themeCss = existsSync(themeCssPath)
    ? await readFile(themeCssPath, "utf-8")
    : "";

  const fontCss = await fontFaceCss(manifest, themeDir).catch((e) => {
    warnings.push(`fonts: ${e.message}`);
    return "";
  });

  // Resolve + treat images (bw/duotone), rewriting image_ref -> data/file URLs.
  await prepareImages(doc, { assetsDir, manifest }).catch((e) =>
    warnings.push(`images: ${e.message}`)
  );

  const mastheadSvg =
    manifest.assets && manifest.assets.masthead
      ? await readFile(path.join(themeDir, manifest.assets.masthead), "utf-8").catch(
          () => ""
        )
      : "";

  const m = doc.masthead || {};
  const mastheadHtml = `<header class="masthead">
  ${mastheadSvg ? `<div class="masthead__logo">${mastheadSvg}</div>` : `<h1 class="masthead__title">${esc(m.title)}</h1>`}
  <div class="masthead__meta">
    <span>${esc(m.date)}</span>
    ${m.issue_no ? `<span>№ ${esc(m.issue_no)}</span>` : ""}
    ${m.edition ? `<span>${esc(m.edition)}</span>` : ""}
  </div>
</header>`;

  const html = `<!doctype html>
<html lang="${esc(doc.locale || "ru")}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
${fontCss}
${pageRule(manifest)}
${cssVarsBlock(manifest)}
${baseCss}
${themeCss}
${web ? webCss() : ""}
${userVarsBlock(manifest, doc.style_overrides)}
</style>
</head>
<body data-theme="${esc(doc.theme_id)}">
${mastheadHtml}
<main class="paper">
${renderSections(doc)}
</main>
</body>
</html>`;

  return { html, warnings, baseUrl: themeDir };
}
