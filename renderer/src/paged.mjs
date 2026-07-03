// Run Paged.js inside Chromium to paginate the composed HTML, then print a PDF.

import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

async function pagedPolyfillSource() {
  // Bundled Paged.js polyfill — kept local so rendering works offline.
  // pagedjs' package.json `exports` blocks deep subpaths, so resolve the main
  // entry (allowed) and read the polyfill from the package root via fs.
  const entry = require.resolve("pagedjs"); // .../node_modules/pagedjs/src/index.js
  const pkgRoot = path.resolve(path.dirname(entry), "..");
  return readFile(path.join(pkgRoot, "dist", "paged.polyfill.js"), "utf-8");
}

export async function printPdf({ html, baseUrl, outPath, rendererDir }) {
  const { chromium } = await import("playwright");
  const polyfill = await pagedPolyfillSource();

  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    const page = await browser.newPage();
    // Set a base URL so theme-relative assets (fonts, masthead) resolve.
    const base = pathToFileURL(baseUrl + path.sep).href;
    const withBase = html.replace(
      /<head>/i,
      `<head><base href="${base}">`
    );

    await page.setContent(withBase, { waitUntil: "networkidle" });

    // Wait for the theme's @font-face files to load and register an `after`
    // hook so we know when Paged.js has FULLY finished. Without this the count
    // is read (and page.pdf can fire) mid-pagination, so the same input yields
    // a different page count run-to-run — and text is measured with fallback
    // font metrics. Paged.js still auto-runs once on inject.
    await page.evaluate(async () => {
      if (document.fonts && document.fonts.ready) {
        await document.fonts.ready;
      }
      window.PagedConfig = {
        after: (flow) => {
          window.__pagedTotal =
            (flow && flow.total) ||
            document.querySelectorAll(".pagedjs_page").length;
        },
      };
    });

    await page.addScriptTag({ content: polyfill });
    const pageCount = await page
      .waitForFunction(() => window.__pagedTotal || null, { timeout: 120000 })
      .then((h) => h.jsonValue());

    await page.pdf({
      path: outPath,
      printBackground: true,
      preferCSSPageSize: true,
    });

    return { pageCount };
  } finally {
    await browser.close();
  }
}
