#!/usr/bin/env node
// Web edition entry point. Reads a RenderDocument JSON and writes a single,
// self-contained, responsive HTML file (fonts + images inlined) — the same
// content as the PDF, readable on a phone. No Chromium/Paged.js needed.
//
// Usage: node web.mjs --in doc.json --out issue.html --themes ../themes --assets ../.data/objects
// On success prints a single JSON line: {"out": "...", "warnings": [...]}

import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { composeHtml } from "./src/compose.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i]?.replace(/^--/, "");
    if (key) args[key] = argv[i + 1];
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  for (const r of ["in", "out"]) {
    if (!args[r]) {
      process.stderr.write(`missing --${r}\n`);
      process.exit(2);
    }
  }
  const themesDir = args.themes
    ? path.resolve(args.themes)
    : path.resolve(__dirname, "..", "themes");
  const assetsDir = args.assets ? path.resolve(args.assets) : process.cwd();

  const doc = JSON.parse(await readFile(args.in, "utf-8"));
  const { html, warnings } = await composeHtml(doc, {
    themesDir,
    assetsDir,
    rendererDir: __dirname,
    web: true,
  });

  const outPath = path.resolve(args.out);
  await writeFile(outPath, html, "utf-8");
  process.stdout.write(JSON.stringify({ out: outPath, warnings }) + "\n");
}

main().catch((err) => {
  process.stderr.write(String(err?.stack || err) + "\n");
  process.exit(1);
});
