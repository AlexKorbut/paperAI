# victorian — Font Downloads

All fonts are released under the SIL Open Font License 1.1 (OFL-1.1).

Run `python scripts/fetch_fonts.py --theme victorian` from the morning-paper/
directory to fetch these automatically (OFL-1.1), or download manually from the
Google Fonts links below.

Expected files (names must match `theme.toml`):

- `UnifrakturCook-Bold.woff2`
- `PlayfairDisplay-Regular.woff2`, `PlayfairDisplay-Bold.woff2`,
  `PlayfairDisplay-Italic.woff2`
- `IMFellEnglish-Regular.woff2`, `IMFellEnglish-Italic.woff2`

## UnifrakturCook

A bold blackletter (Fraktur) face used for the masthead, giving the authentic
mid-Victorian engraved nameplate. Only a bold weight exists.

- License: OFL-1.1
- https://fonts.google.com/specimen/UnifrakturCook

## Playfair Display

A high-contrast Didone-style serif used for the dramatic centred headlines and
drop caps, echoing Victorian fat-face display type.

- License: OFL-1.1
- https://fonts.google.com/specimen/Playfair+Display

## IM Fell English

A revival of the 17th–19th century Fell types, used for body text, decks and
captions to achieve an authentic antique letterpress texture.

- License: OFL-1.1
- https://fonts.google.com/specimen/IM+Fell+English

## Note

The renderer will warn (but not fail) if font files are absent. System serif
fallbacks (Georgia, Times New Roman) will be used instead.
