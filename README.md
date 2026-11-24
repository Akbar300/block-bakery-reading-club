# block-bakery-reading-club
Block Bakery Reading Club: Grade 3 reading game with baking and block building

## Big Reads (added Nov 2026)
Weekly SOL-length stories and articles plus a Word Lab (sound sort, Listen and Write spelling, Wow words, synonyms/antonyms/shades of meaning), one set per word-study week. Content comes from the Reading Academy weeks in `tools/academy_weeks.json`.
To add a week: append it to `tools/academy_weeks.json` (same shape as the others), then run `python3 tools/build_weeks.py tools/academy_weeks.json` from the repo root. Weeks appear on their start date.

## Story Corner (added Nov 2026)
Stories written by kid authors, pinned at the top of Big Reads (always open, not tied to a week). Each story is an entry in the `KIDM` array in `index.html` (title, `text` paragraphs, and `games` in the same format as the missions). The art is drawn by `kidArt()`. Current story: "Sparkle and the Squishies".

## Night mode (added Nov 2026)
The moon/sun button in the top bar switches between day and night colors for easier reading in the evening. The choice is saved on the device. All night colors live in the `DARK MODE` block at the end of the stylesheet and apply when `<html>` has the `dark` class.
