# infographic — Font Downloads

All fonts are released under the SIL Open Font License 1.1 (OFL-1.1).

Run `python scripts/fetch_fonts.py --theme infographic` from the morning-paper/
directory to fetch these automatically (OFL-1.1), or download manually from the
Google Fonts links below. Both families are fetched with the `cyrillic` subset.

Expected files (names must match `theme.toml`):

- `IBMPlexSans-Regular.woff2`, `IBMPlexSans-Medium.woff2`,
  `IBMPlexSans-Bold.woff2`
- `PTSerif-Regular.woff2`, `PTSerif-Bold.woff2`, `PTSerif-Italic.woff2`

## IBM Plex Sans

A neutral, highly legible grotesque with full Cyrillic support, used for the
masthead, headlines, decks and section tabs — the modern infographic voice.

- License: OFL-1.1
- https://fonts.google.com/specimen/IBM+Plex+Sans

## PT Serif

A contemporary transitional serif with full Cyrillic support, used for body
text to keep long reads comfortable against the bold sans furniture.

- License: OFL-1.1
- https://fonts.google.com/specimen/PT+Serif

## Note

The renderer will warn (but not fail) if font files are absent. System
sans/serif fallbacks will be used instead.
