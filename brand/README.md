# Electify brand assets

All files are SVG (scalable, sharp at any size). Open them in any browser to view, or drag into Figma / Keynote / Google Slides.

## Files

- **`logo.svg`** — the main mark. Black rounded square with a white "E". Use this on light/white backgrounds. Works for social avatars, footer marks, GitHub README headers, etc.
- **`logo-inverted.svg`** — white square with a black "E". Use on black/dark backgrounds.
- **`logo-mark.svg`** — just the "E", no background. Color inherits from `currentColor` in CSS, so it takes on whatever text color you apply. Good for inline use next to the wordmark.
- **`wordmark.svg`** — horizontal lockup: E-mark + "Electify" text. Use for headers, letterheads, presentation title slides.
- **`favicon.svg`** — same as logo.svg, 1:1 crop. Already wired into the site's `<link rel="icon">`.

## Need PNG?

Open the SVG in a browser, right-click → Save as. Or use https://cloudconvert.com/svg-to-png — free, no signup, pick size (512×512 is standard for app icons).

## Colors

- Ink: `#0A0A0A` (almost-black)
- Paper: `#FAFAF9` (off-white, matches site background)

## Typography

- Geist (Google Fonts) — 600 weight for the mark, 600 for the wordmark
- Fallbacks: Inter, system-ui

If the mark ever looks boxy, the font is missing and it's falling back — install Geist locally or let Google Fonts load it.
