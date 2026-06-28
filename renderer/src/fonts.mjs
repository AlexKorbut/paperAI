// Generate @font-face declarations from a theme manifest's [[fonts]] entries.
// Fonts are bundled per theme (themes/<id>/fonts/) so there's no network
// dependency and no missing-glyph fallback at print time.

import { readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";

const MIME = {
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".ttf": "font/ttf",
  ".otf": "font/otf",
};

function formatFor(ext) {
  return (
    { ".woff2": "woff2", ".woff": "woff", ".ttf": "truetype", ".otf": "opentype" }[
      ext
    ] || "woff2"
  );
}

// Infer weight/style from the file name (e.g. "EBGaramond-BoldItalic.woff2").
// Without these descriptors every face of a family collapses onto the same
// normal/400 slot, and the LAST-declared file wins — so a "Regular, Bold" pair
// renders all body text bold, and "Regular, Italic" renders it italic. Tagging
// each face lets normal text pick Regular while bold/italic stay available.
function styleFor(file) {
  const n = file.toLowerCase();
  const italic = /italic|oblique/.test(n);
  let weight = 400;
  if (/black|heavy/.test(n)) weight = 900;
  else if (/extrabold|ultrabold/.test(n)) weight = 800;
  else if (/semibold|demibold/.test(n)) weight = 600;
  else if (/\bbold\b|bold/.test(n)) weight = 700;
  else if (/light/.test(n)) weight = 300;
  return { weight, style: italic ? "italic" : "normal" };
}

export async function fontFaceCss(manifest, themeDir) {
  const fonts = manifest.fonts || [];
  const blocks = [];
  for (const font of fonts) {
    for (const rel of font.files || []) {
      const abs = path.join(themeDir, rel);
      if (!existsSync(abs)) {
        // Missing font file: skip rather than fail; the body font stack falls back.
        continue;
      }
      const ext = path.extname(abs).toLowerCase();
      const buf = await readFile(abs);
      const dataUrl = `data:${MIME[ext] || "font/woff2"};base64,${buf.toString(
        "base64"
      )}`;
      const { weight, style } = styleFor(path.basename(rel));
      blocks.push(
        `@font-face {\n  font-family: "${font.family}";\n  font-weight: ${weight};\n  font-style: ${style};\n  src: url("${dataUrl}") format("${formatFor(
          ext
        )}");\n  font-display: swap;\n}`
      );
    }
  }
  return blocks.join("\n");
}
