# Lrssn design system

The tokens, styles and components that make a page look like Lrssn: an engineer's notebook, with warm sand and timber, one brand orange, and type that does the work.
It is for anyone who builds a page or an app that carries the brand, such as the Lrssn website.

The colours come from the [Lrssn colour themes](https://github.com/Lrssn-blog/Color-theme): Lrssn Shore, which is light, and Lrssn Hearth, which is dark.
The rules for the name, the logo and the voice are in the [brand guide](https://github.com/Lrssn-blog/Brand-guide/blob/main/src/brand/Brand.md), and this guide does not repeat them.
The tables below are generated from the themes and from [`tokens/tokens.toml`](./tokens/tokens.toml), and the build fails if they are out of date.

To see every component in both themes, open [`preview/index.html`](./preview/index.html) in a browser.

## Table of contents

[TOC]

## Principles

- **Have one source for each fact.**
  The colours are defined once, in the colour themes, and every other token once, in `tokens/tokens.toml`.
  Use the tokens, and never type a colour or a size that a token holds.
- **Be accessible.**
  Text reaches a contrast of 4.5 on its background, and borders, focus rings and icons reach 3, in both themes.
  The build checks every pair the components use.
- **Put whitespace first.**
  Separate things with space before a border, and with a border before a shadow.
- **Show one loud thing per view.**
  The brand orange is a fill at most once per screen.
  A thin rule or an underline in orange does not count as a fill.
- **Let type do the work.**
  Inter for the interface, Merriweather for reading, Playfair Display for the brand and Geist Mono for facts, with real contrast in size between headings and text.
- **Let structure show.**
  The ledger's margin and rule, hairlines and a faint dot grid are fine when they organise the content.
- **Leave out decoration.**
  Do not use gradients, decorative icons or emoji.
  An icon that carries meaning is fine, with a label.
- **Design both themes.**
  Shore and Hearth are each designed, and neither is the other inverted.
  Check every new screen in both, and on paper, which is always light.

When this guide does not cover something, choose the option that best serves these principles.

## Getting started

### On a page

Load the theme script first, in the `<head>`, so the saved theme applies before the first paint.
Then load the fonts and the stylesheet, and the scripts last, as a module:

```html
<head>
  <script src="js/theme-init.js"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap">
  <link rel="stylesheet" href="dist/lrssn.css">
  <script type="module" src="js/index.js"></script>
</head>
<body class="lrssn-page">
  <header class="lrssn-header">…</header>
  <main class="lrssn-container">…</main>
  <footer class="lrssn-footer">…</footer>
</body>
```

Every component works without the scripts, and loses only its controls: the theme toggle, the Copy button of a code block, the buttons of a carousel and the marked section of a table of contents.

### The files

| File | What it holds |
| --- | --- |
| [`dist/lrssn.css`](./dist/lrssn.css) | Everything: the tokens, the base styles and every component. |
| [`dist/tokens.css`](./dist/tokens.css) | The tokens only, as custom properties. |
| [`dist/_tokens.scss`](./dist/_tokens.scss) | The tokens as Sass variables, which point at the custom properties. |
| [`dist/tokens.json`](./dist/tokens.json) | The tokens as data, with their values in each theme and their use. |
| [`js/theme-init.js`](./js/theme-init.js) | Applies the saved theme before the first paint. |
| [`js/index.js`](./js/index.js) | Wires the components that need JavaScript. |
| [`assets/logo/`](./assets/logo) | The logo files the brand guide names: orange, dark and light. |

The custom properties are named `--lrssn-<token>`, and the classes `lrssn-<component>`, so they do not clash with a page's own.
All the CSS sits in cascade layers, `lrssn.tokens`, `lrssn.base` and `lrssn.components`, so a page's own styles win over it without a fight over specificity.

### With Sass

`dist/_tokens.scss` holds a variable for each token, such as `$lrssn-primary-color`, which points at its custom property.
Load `dist/tokens.css` as well, and mix colours with `color-mix()`, because Sass's colour functions cannot read a custom property:

```scss
@use 'lrssn/tokens' as *;

.note {
  background: color-mix(in srgb, #{$lrssn-primary-color} 10%, transparent);
}

@media (max-width: $lrssn-breakpoint-md-value) {
  …
}
```

### Themes

- **System** is the default, and follows the device.
  `data-theme="light"` on `<html>` chooses Lrssn Shore, and `data-theme="dark"` Lrssn Hearth.
  The [theme toggle](./components/theme-toggle/README.md) sets it, and saves the choice.
- `data-theme` works on any element, so a part of a page can wear the other theme.
- Print always uses Shore, because paper is light.

## Foundations

### Colour

- Write orange text in `primary-text`, and never in `primary-color`, which is too light to read on sand.
- Put `text-on-primary` on an orange fill, and never white.
- Use `primary-color` as a fill at most once per screen.
- Keep the surfaces warm: sand in Shore, and timber in Hearth.
  Do not bring in plain or cool greys.
- `secondary-color` is the cool accent, tropical teal in Shore and ice in Hearth: a fill, a border or a bar, and never text.
  Text in the cool accent is `secondary-text`.
- Always write a status in words, as well as showing it in a colour.
- Do not add colours that are not here.
  To change a colour, change it in the colour themes, whose build checks its contrast, and run `scripts/build.py --write` here.

The website's 51 tokens come first, in the groups of its stylesheet.
The status colours `warning-color` and `info-color`, the `code-*` colours and `margin-rule-color` are the design system's own, taken from the same palettes.

<!-- generated:colours -->
#### Brand

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `primary-color` | `#fc6600` | `#fc6600` | Brand orange: the primary button, the logo files, the underline of the current link and the margin rule. A fill at most once per screen. Never text. |
| `primary-text` | `#b04600` | `#ff8a3d` | Orange text: the logo on screen, links and text on `primary-soft`. |
| `primary-soft` | `#ffe3cc` | `#3a1f0e` | Apricot tint: text selection, the New badge and the Important callout. |
| `secondary-color` | `#00999a` | `#4d94b8` | The cool accent as a fill, a border or a bar: quotes and task-list boxes. Never text. |
| `secondary-text` | `#00737a` | `#8cc8e3` | Text in the cool accent: topic pills without a colour of their own, and breadcrumbs. |
| `secondary-soft` | `#d2f1ee` | `#142430` | Tint behind secondary text: the Tutorial badge and a project's status. |
| `link-color` | `#b04600` | `#ff8a3d` | Links in running text, always underlined. |
| `focus-color` | `#b04600` | `#fc6600` | The keyboard focus ring: a 2px outline, 2px away from the element. |

#### Surfaces

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `background` | `#fdf6ea` | `#1a1512` | The page, the header and the footer. |
| `surface` | `#fffbf4` | `#211a16` | Cards, panels, inputs and the copy button of a code block. |
| `surface-subtle` | `#f8efe0` | `#1d1714` | Tab strips and quiet panels. |
| `surface-muted` | `#f3e8d5` | `#28201b` | Table headings and the Note callout. |
| `surface-hover` | `#efe2cc` | `#2f2620` | A control under the pointer, and the pressed button of the theme toggle. |
| `surface-sunken` | `#f3e8d5` | `#120e0c` | Code blocks and inline code. |
| `header-background` | `#fdf6ea` | `#1a1512` | The sticky header: the same as the page, and set apart by `header-border`. |
| `header-border` | `#e3d3b9` | `#2e343c` | The hairline under the header. |
| `admin-header-background` | `#15323f` | `#0f0c0a` | The header of the website's admin area, with `text-on-dark`. |

#### Text

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `text-color` | `#13303d` | `#f0e3d0` | Interface text and labels, and the current link. |
| `text-strong` | `#0a1f29` | `#fff6e8` | Headings. |
| `text-body` | `#24404c` | `#e0d3c0` | Running text. |
| `text-muted` | `#4f6470` | `#a3aebb` | Secondary text: ledes, descriptions, and the links of the navigation and the footer. |
| `text-subtle` | `#5c6e77` | `#95a0ad` | Metadata: the ledger margin, dates, counts and labels. |
| `text-on-dark` | `#fffbf4` | `#fff6e8` | Text on `admin-header-background` and `notification-badge`. |
| `text-on-primary` | `#14171c` | `#14171c` | Text on a `primary-color` fill. Never white. |

#### Borders

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `border-color` | `#e3d3b9` | `#2e343c` | Borders and dividers: cards, ledger rows, tables and the footer. |
| `border-color-light` | `#ede2cf` | `#262b32` | Quiet borders, such as between the rows of an admin table. |
| `border-color-muted` | `#dccbb0` | `#363d47` | Sidebar rules, and the dots of the dot grid. |
| `border-color-fieldset` | `#dccbb0` | `#363d47` | The border of a fieldset. |
| `border-color-input` | `#8a7e6c` | `#76818f` | The border of an input, a select, a textarea and a secondary button. |
| `border-color-strong` | `#b5a588` | `#515b68` | The copy button of a code block, and page numbers under the pointer. |
| `border-color-tree` | `#bfe6e3` | `#1d3340` | The guide line of a nested list of topics. |
| `margin-rule-color` | `#fc6600b2` | `#fc6600b2` | The ledger's margin rule: `primary-color` at 70 % opacity. |

#### Status

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `success-color` | `#1c7448` | `#a9d48f` | Success, as text, and the Tip callout. Always with words. |
| `success-background` | `#e1f1e4` | `#1e2a18` | Behind a success message and the Tip callout. |
| `success-border` | `#b8d9c0` | `#34492a` | The border of a success message. |
| `danger-color` | `#c4262e` | `#ff6b5e` | Errors, as text: an error message, the border of an invalid field and the Caution callout. Always with words. |
| `danger-background` | `#fbe5e1` | `#361815` | Behind an error message and the Caution callout. |
| `danger-border` | `#f0c2ba` | `#5c2a24` | The border of an error message. |
| `notification-badge` | `#c4262e` | `#b8321e` | The count on the website's notification bell, with `text-on-dark`. |
| `warning-color` | `#965a00` | `#ffb547` | A warning, as text outside a banner. Always with words. |
| `info-color` | `#00629c` | `#7fcbe6` | Neutral information, as text. |

#### Banners

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `banner-info-background` | `#d2f1ee` | `#142430` | Behind an info banner. |
| `banner-info-color` | `#00646a` | `#a6d6ec` | The text of an info banner. |
| `banner-warning-background` | `#fdeccb` | `#33260f` | Behind a warning banner and the Warning callout. |
| `banner-warning-color` | `#7a4f00` | `#ffcf70` | The text of a warning banner, and the Warning callout. |
| `banner-error-background` | `#fbe0dc` | `#361815` | Behind an error banner. |
| `banner-error-color` | `#8a1f1f` | `#ffa196` | The text of an error banner. |
| `banner-success-background` | `#dff0e2` | `#1e2a18` | Behind a success banner. |
| `banner-success-color` | `#1e6b3c` | `#b8e0a0` | The text of a success banner. |

#### Tags & media

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `tag-background-hover` | `#ffe3cc` | `#3a1f0e` | A tag under the pointer in the website's admin area. |
| `image-placeholder-start` | `#f3e8d5` | `#28201b` | One end of the placeholder shown while an image loads. |
| `image-placeholder-end` | `#e3d3b8` | `#3a2f28` | The other end of the placeholder shown while an image loads. |
| `resource-icon-color` | `#00737a` | `#8cc8e3` | The icon beside a reference or a further-reading link. |
| `resource-kind-color` | `#4f6470` | `#a3aebb` | The kind of a reference, such as PDF or Video. |

#### Code

| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `code-keyword` | `#b04600` | `#fc6600` | Keywords in code. |
| `code-function` | `#00629c` | `#ffb547` | Functions and methods in code. |
| `code-string` | `#00756a` | `#a9d48f` | Strings in code. |
| `code-number` | `#c2215a` | `#ff88c8` | Numbers and constants in code. |
| `code-type` | `#3550b0` | `#7fcbe6` | Types and classes in code. |
| `code-builtin` | `#8a3fbf` | `#c4a5ff` | Built-in names in code. |
| `code-tag` | `#bd3722` | `#ff6b4f` | Tags in markup. |
| `code-property` | `#7a5000` | `#ebc69d` | Properties and attributes in code. |
| `code-parameter` | `#6a4b33` | `#f7d2aa` | Parameters in code. |
| `code-operator` | `#a4521c` | `#f09a62` | Operators in code. |
| `code-punctuation` | `#6b6152` | `#a8998b` | Punctuation in code. |
| `code-escape` | `#b02f86` | `#ffe08a` | Escapes and regular expressions in code. |
| `code-comment` | `#76664e` | `#8796aa` | Comments in code. |
<!-- end:colours -->

### Contrast

The ratios are calculated with the [WCAG 2.2 contrast formula](https://www.w3.org/TR/WCAG22/#contrast-minimum).
Text needs a ratio of at least 4.5, and large text, borders, focus rings and icons need at least 3.
`scripts/build.py` checks every pair below, and fails if one breaks.

Every text token, on the page and on the surface:

<!-- generated:contrast-text -->
| Token | Shore background | Shore surface | Hearth background | Hearth surface |
| --- | --- | --- | --- | --- |
| `text-color` | 12.88 | 13.41 | 14.31 | 13.56 |
| `text-strong` | 15.75 | 16.40 | 16.90 | 16.01 |
| `text-body` | 10.22 | 10.64 | 12.28 | 11.64 |
| `text-muted` | 5.77 | 6.01 | 8.04 | 7.62 |
| `text-subtle` | 4.95 | 5.15 | 6.82 | 6.46 |
| `primary-text` | 5.25 | 5.47 | 7.72 | 7.32 |
| `secondary-text` | 5.24 | 5.45 | 9.90 | 9.38 |
| `link-color` | 5.25 | 5.47 | 7.72 | 7.32 |
| `success-color` | 5.37 | 5.59 | 10.78 | 10.21 |
| `danger-color` | 5.34 | 5.56 | 6.48 | 6.14 |
| `warning-color` | 5.20 | 5.42 | 10.30 | 9.77 |
| `info-color` | 6.06 | 6.31 | 9.99 | 9.47 |
<!-- end:contrast-text -->

The other pairs the components use:

<!-- generated:contrast-pairs -->
| Text or graphic | On | Shore | Hearth | Needs |
| --- | --- | --- | --- | --- |
| `text-color` | `surface-muted` | 11.41 | 12.65 | 4.5 |
| `text-color` | `surface-sunken` | 11.41 | 15.18 | 4.5 |
| `text-color` | `surface-hover` | 10.82 | 11.70 | 4.5 |
| `text-color` | `primary-soft` | 11.27 | 12.01 | 4.5 |
| `text-color` | `secondary-soft` | 11.57 | 12.53 | 4.5 |
| `text-body` | `surface-muted` | 9.05 | 10.85 | 4.5 |
| `text-body` | `success-background` | 9.36 | 10.18 | 4.5 |
| `text-body` | `primary-soft` | 8.95 | 10.31 | 4.5 |
| `text-body` | `banner-warning-background` | 9.43 | 10.00 | 4.5 |
| `text-body` | `danger-background` | 9.10 | 10.97 | 4.5 |
| `text-on-primary` | `primary-color` | 6.02 | 6.02 | 4.5 |
| `primary-text` | `primary-soft` | 4.60 | 6.48 | 4.5 |
| `secondary-text` | `secondary-soft` | 4.70 | 8.67 | 4.5 |
| `success-color` | `success-background` | 4.92 | 8.93 | 4.5 |
| `danger-color` | `danger-background` | 4.75 | 5.79 | 4.5 |
| `banner-info-color` | `banner-info-background` | 5.79 | 10.15 | 4.5 |
| `banner-warning-color` | `banner-warning-background` | 6.12 | 10.11 | 4.5 |
| `banner-error-color` | `banner-error-background` | 7.31 | 8.31 | 4.5 |
| `banner-success-color` | `banner-success-background` | 5.49 | 10.15 | 4.5 |
| `mix(secondary-text 55%, text-color)` | `mix(secondary-text 14%, surface)` | 6.73 | 8.28 | 4.5 |
| `code-keyword` | `surface-sunken` | 4.65 | 6.44 | 4.5 |
| `code-function` | `surface-sunken` | 5.37 | 10.93 | 4.5 |
| `code-string` | `surface-sunken` | 4.61 | 11.43 | 4.5 |
| `code-number` | `surface-sunken` | 4.73 | 8.78 | 4.5 |
| `code-type` | `surface-sunken` | 5.92 | 10.59 | 4.5 |
| `code-builtin` | `surface-sunken` | 4.89 | 9.30 | 4.5 |
| `code-tag` | `surface-sunken` | 4.64 | 6.83 | 4.5 |
| `code-property` | `surface-sunken` | 5.82 | 11.97 | 4.5 |
| `code-parameter` | `surface-sunken` | 6.49 | 13.49 | 4.5 |
| `code-operator` | `surface-sunken` | 4.55 | 8.69 | 4.5 |
| `code-punctuation` | `surface-sunken` | 5.01 | 6.94 | 4.5 |
| `code-escape` | `surface-sunken` | 4.81 | 14.88 | 4.5 |
| `code-comment` | `surface-sunken` | 4.58 | 6.37 | 4.5 |
| `border-color-input` | `background` | 3.70 | 4.58 | 3.0 |
| `border-color-input` | `surface` | 3.85 | 4.34 | 3.0 |
| `focus-color` | `background` | 5.25 | 6.07 | 3.0 |
| `focus-color` | `surface` | 5.47 | 5.75 | 3.0 |
<!-- end:contrast-pairs -->

The text of a topic pill without a colour of its own, and its tint, are mixes, written as `mix(…)` above.
A topic's own colour is not checked, so check a new one in both themes.

### Typography

Four typefaces, each with one job.
Each has a generic fallback, so a page still reads while the fonts load.

<!-- generated:font -->
| Token | Value | Use |
| --- | --- | --- |
| `font-display` | `'Playfair Display', serif` | The logo, and brand moments: hero lines, section titles, Article titles and empty states. |
| `font-ui` | `'Inter', sans-serif` | The interface: headings, navigation, buttons, labels, forms and tables. |
| `font-serif` | `'Merriweather', serif` | Running text: articles, posts, summaries and ledes. |
| `font-mono` | `'Geist Mono', monospace` | Code, and small metadata: dates, counts, series parts and labels. |
<!-- end:font -->

<!-- generated:font-size -->
| Token | Value | Use |
| --- | --- | --- |
| `font-size-xs` | `0.75rem` | Mono metadata and labels. |
| `font-size-sm` | `0.875rem` | Small interface text, captions and code. |
| `font-size-base` | `1rem` | Interface text. |
| `font-size-lg` | `1.125rem` | Running text and ledes. |
| `font-size-xl` | `1.25rem` | Level 3 headings, and card titles. |
| `font-size-2xl` | `1.6rem` | Level 2 headings, and the line of an empty state. |
| `font-size-3xl` | `clamp(2rem, 4.5vw, 3rem)` | Level 1 headings. |
| `font-size-display` | `clamp(2.5rem, 6.5vw, 5.25rem)` | Playfair Display hero lines and section titles. |
<!-- end:font-size -->

<!-- generated:line-height -->
| Token | Value | Use |
| --- | --- | --- |
| `line-height-tight` | `1.15` | Headings. |
| `line-height-base` | `1.55` | Interface text. |
| `line-height-reading` | `1.8` | Running text. |
<!-- end:line-height -->

The type styles set the typefaces and sizes together:

<!-- generated:type-styles -->
| Style | Typeface | Size | Line height | Weight | Use |
| --- | --- | --- | --- | --- | --- |
| `display` | `font-display` | `font-size-display` | `1.02` | 700 | The one hero line of a page, and section titles. One per view. |
| `title` | `font-display` | `font-size-2xl` | `1.2` | 700 | The line of an empty state, series names and Article titles in lists. |
| `logo` | `font-display` | `font-size-base` | `1.1` | 700 | The name in the logo. Never retyped elsewhere: use the logo. |
| `h1` | `font-ui` | `font-size-3xl` | `line-height-tight` | 700 | Level 1 headings and Post titles. |
| `h2` | `font-ui` | `font-size-2xl` | `line-height-tight` | 600 | Level 2 headings. |
| `h3` | `font-ui` | `font-size-xl` | `line-height-tight` | 600 | Level 3 headings and card titles. |
| `ui` | `font-ui` | `font-size-base` | `line-height-base` | 400 | Interface text: navigation, buttons, labels and forms. |
| `ui-small` | `font-ui` | `font-size-sm` | `line-height-base` | 400 | Hints, captions and tables. |
| `body` | `font-serif` | `font-size-lg` | `line-height-reading` | 400 | Running text, at most 65 characters wide. |
| `lede` | `font-serif` italic | `font-size-lg` | `1.6` | 400 | The lede under the title of a Post or an Article, in `text-muted`. |
| `code` | `font-mono` | `font-size-sm` | `1.7` | 400 | Code blocks and inline code. |
| `meta` | `font-mono` | `font-size-xs` | `line-height-base` | 400 | Dates as YYYY-MM-DD, counts and series parts, in `text-subtle`. |
| `label` | `font-mono` | `0.7rem` | `line-height-base` | 500 | Uppercase labels: the ledger margin's headings and the footer's column headings. |
<!-- end:type-styles -->

- Use Playfair Display for one line per view, besides the logo: the hero line, the section title, or the title of an Article.
- Keep running text to about 65 characters wide, with the `measure` token.
- Write headings, buttons and labels in sentence case.
- Write dates as `YYYY-MM-DD`, in Geist Mono, and line up numbers with `font-variant-numeric: tabular-nums`.
- Set uppercase only for small labels, with a letter spacing of 0.1em.

### Spacing

<!-- generated:space -->
| Token | Value | Use |
| --- | --- | --- |
| `space-1` | `0.25rem` | Inside pills and badges, and between a heading and its # link. |
| `space-2` | `0.5rem` | Between the items of a row of pills, buttons or page numbers. |
| `space-3` | `0.75rem` | Between the fields of a form, and inside small controls. |
| `space-4` | `1rem` | The smallest page gutter, and the space between a title and its lede. |
| `space-5` | `1.25rem` | Between the entries of a carousel, and the padding of a card. |
| `space-6` | `1.5rem` | The padding above and below a ledger row, and the gap between cards. |
| `space-8` | `2rem` | Between groups, such as the columns of the footer, and under a section head. |
| `space-10` | `2.5rem` | Above the body of a Post or an Article, and the largest page gutter. |
| `space-12` | `3rem` | Between the sections of a page. |
| `space-16` | `4rem` | Above related items at the end of a page. |
| `space-18` | `4.5rem` | Above and below the head of a page on a large screen. |
<!-- end:space -->

- Space the blocks of a page with these steps.
  Inside small controls, the components keep the finer values of the website, such as the 0.35rem under a link of the header.
- Lay out a row or a column with `gap`, rather than a margin on each item.
- When in doubt, take the next step up.

### Layout

<!-- generated:layout -->
| Token | Value | Use |
| --- | --- | --- |
| `content-max-width` | `74rem` | The width of the header, the footer and the content of a page. |
| `layout-max-width` | `960px` | The width of narrower pages, such as a project or the admin area. |
| `page-gutter` | `clamp(1rem, 4vw, 2.5rem)` | The space at each side of a page. Never less than 16px. |
| `measure` | `65ch` | The widest a block of running text gets. |
| `ledger-margin-width` | `9.5rem` | The ledger's margin column, left of the rule. |
| `ledger-gap` | `clamp(1.25rem, 3vw, 2.25rem)` | The space at each side of the ledger's margin rule. |
| `breakpoint-sm` | `640px` | Below it, the navigation links get a row of their own and the footer's columns wrap. Media queries cannot read custom properties, so copy the value. |
| `breakpoint-md` | `720px` | Below it, the ledger stacks: the margin moves above the content. Media queries cannot read custom properties, so copy the value. |
<!-- end:layout -->

- Put the content of a page in `lrssn-container`: at most `content-max-width` wide, with `page-gutter` at each side.
- The [ledger](./components/ledger/README.md) is the signature layout: facts in a margin on the left, and the writing right of a thin orange rule.
  Below 720px, it stacks.
- Below 640px, the header's links get a row of their own, and the footer's columns wrap.
- Nothing scrolls sideways but a wide table, a code block or a carousel, each inside its own box.

### Shape and depth

<!-- generated:radius -->
| Token | Value | Use |
| --- | --- | --- |
| `radius-xs` | `3px` | Inline code, page numbers and the buttons inside the theme toggle. |
| `radius-sm` | `4px` | Buttons, inputs, code blocks, callouts and the theme toggle. |
| `radius-md` | `5px` | Small panels. |
| `radius-lg` | `6px` | Pictures in a grid. |
| `radius-xl` | `8px` | Cards and their covers. |
| `radius-pill` | `999px` | Topic pills, badges and a project's status. |
<!-- end:radius -->

<!-- generated:shadow -->
| Token | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `shadow-sm` | `0 2px 8px #6b4a2a1a` | `0 2px 8px #0000001a` | A small raised control. |
| `shadow-md` | `0 4px 12px #6b4a2a1a` | `0 4px 12px #0000001a` | Menus and dropdowns. |
| `shadow-lg` | `0 8px 30px #6b4a2a2e` | `0 8px 30px #0000002e` | A dialog. Use space, then a border, before a shadow. |
<!-- end:shadow -->

- Most things have no box at all: the ledger's rule and hairlines organise the page.
- A card, such as a project card, is the one element with a border, a fill and a radius together, because it is a separate object.
- A shadow is only for something that floats above the page, such as a menu.
  Its colour is the palette's `shadow`: warm brown on sand, and black on timber.

### Motion

<!-- generated:transition -->
| Token | Value | Use |
| --- | --- | --- |
| `transition-fast` | `0.15s ease` | A colour change under the pointer, and the arrow of a link that moves. |
| `transition-base` | `0.2s ease` | The theme toggle, the table of contents and a heading's # link. |
<!-- end:transition -->

- Motion is short, and only answers the reader: a colour under the pointer, an arrow that moves, the bar of the table of contents.
- Under `prefers-reduced-motion`, the base styles turn transitions off, and a carousel scrolls without easing.
- Nothing moves by itself.

### Stacking

<!-- generated:z-index -->
| Token | Value | Use |
| --- | --- | --- |
| `z-raised` | `1` | Above its siblings, such as the copy button of a code block. |
| `z-dropdown` | `10` | Menus inside the header. |
| `z-banner` | `900` | The sticky stack of banners, below the header. |
| `z-header` | `1000` | The sticky header. |
| `z-modal` | `2000` | A dialog, above everything. |
<!-- end:z-index -->

### States

- **Focus:** a 2px outline in `focus-color`, 2px away from the element, on every control, from the base styles.
  Never remove it.
- **Hover:** a link underlines, a quiet link turns `text-color`, and a control takes `surface-hover`.
- **Current:** the link to the current page or section has `aria-current`, and an orange underline or bar.
- **Disabled:** a control that cannot be used yet fades to 45 % opacity, and keeps its place.
- **Invalid:** a field with `aria-invalid="true"` has a border in `danger-color`, and an error in words under it.

### Print

- Paper is light whatever the theme, so print uses Shore's tokens.
- The header, the footer, banners and the controls that need a screen are left out: the theme toggle, the Copy buttons, the carousel's buttons, the pagination, the table of contents and the `#` links of headings.
- The ledger stacks, a callout gets a full border, and code wraps.

## Components

Each component has a README with its use, its markup, its variants, and notes on accessibility.
The [preview](./preview/index.html) shows each one in both themes.

<!-- generated:components -->
### Brand

| Component | Class | What it is for |
| --- | --- | --- |
| [Logo](./components/logo/README.md) | `.lrssn-logo` | The logo shows the Lrssn mark and name, and the username where it fits. |

### Actions

| Component | Class | What it is for |
| --- | --- | --- |
| [Button](./components/button/README.md) | `.lrssn-button` | A button starts an action, or leads to the one next step that matters. |
| [Links](./components/link/README.md) | `.lrssn-link` | A link takes the reader to another page, or to another place on this one. |
| [Theme toggle](./components/theme-toggle/README.md) | `.lrssn-theme-toggle` | The theme toggle lets the reader choose System, Light or Dark. |

### Forms

| Component | Class | What it is for |
| --- | --- | --- |
| [Form field](./components/form-field/README.md) | `.lrssn-form-field` | A form field asks for one thing: its label, its control, and its hint or its error. |

### Content

| Component | Class | What it is for |
| --- | --- | --- |
| [Prose](./components/prose/README.md) | `.lrssn-prose` | Prose sets running text, such as the body of a Post or an Article, and everything rendered Markdown can hold. |
| [Code block](./components/code-block/README.md) | `.lrssn-code-block` | A code block shows code, in Geist Mono on the sunken surface, highlighted in the Lrssn themes' own colours. |
| [Callout](./components/callout/README.md) | `.lrssn-callout` | A callout sets a note, a tip, an important point, a warning or a caution apart from the text around it. |
| [Topic pill](./components/topic-pill/README.md) | `.lrssn-topic-pill` | A topic pill names a topic of a Post or an Article, and links to the other writing on it. |

### Feedback

| Component | Class | What it is for |
| --- | --- | --- |
| [Banner](./components/banner/README.md) | `.lrssn-banner` | A banner tells every reader one thing across the top of the page, such as a change or an outage. |

### Layout

| Component | Class | What it is for |
| --- | --- | --- |
| [Ledger](./components/ledger/README.md) | `.lrssn-ledger` | The ledger is the signature layout of Lrssn: facts in a margin on the left, and the writing right of a thin orange rule, like a lab notebook. |
| [Header](./components/header/README.md) | `.lrssn-header` | The header holds the logo, the links to each section and the tools, at the top of every page. |
| [Footer](./components/footer/README.md) | `.lrssn-footer` | The footer closes every page with the logo, columns of links, and a line for the copyright and the licence. |

### Site patterns

| Component | Class | What it is for |
| --- | --- | --- |
| [Section head](./components/section-head/README.md) | `.lrssn-section-head` | A section head opens a section page, such as the Blog, with its title, a lede and links to its views. |
| [Post card](./components/post-card/README.md) | `.lrssn-post-card` | A post card is one entry in a list of Posts or Articles: a ledger row with the facts in the margin and the title, the description and the topics beside them. |
| [Project card](./components/project-card/README.md) | `.lrssn-project-card` | A project card shows one project in a grid: its name, a summary, its status and its links. |
| [Release card](./components/release-card/README.md) | `.lrssn-release-card` | A release card shows the latest release of a project: its version, what it changed, its project and its date. |
| [Empty state](./components/empty-state/README.md) | `.lrssn-empty-state` | An empty state shows in place of a list that is empty, or has no results, and says where to go instead. |
| [Pagination](./components/pagination/README.md) | `.lrssn-pagination` | Pagination moves between the pages of a long list, above it and below it. |
| [Carousel](./components/carousel/README.md) | `.lrssn-carousel` | A carousel shows a row of entries that scrolls sideways, such as the Articles on an author's profile. |
| [Table of contents](./components/table-of-contents/README.md) | `.lrssn-table-of-contents` | A table of contents lists the sections of a long page in the ledger's margin, and marks the one being read. |
<!-- end:components -->

## Patterns

The pages of the Lrssn website, put together from the components.

### The home page

1. The [header](./components/header/README.md).
2. The intro: one Playfair Display line at the display size over a faint dot grid, with one word in `primary-text` italics, then a lede and the counts in Geist Mono.
   It is the page's one brand moment.
3. A row of popular [topic pills](./components/topic-pill/README.md).
4. The latest Articles and Posts in two columns, each a stacked [ledger](./components/ledger/README.md) of [post cards](./components/post-card/README.md).
5. The [project cards](./components/project-card/README.md) beside the latest [release card](./components/release-card/README.md).
6. The [footer](./components/footer/README.md).

### A section listing

1. The [section head](./components/section-head/README.md): the section's path in the margin, its title, a lede and its views.
2. The [pagination](./components/pagination/README.md), then the list of [post cards](./components/post-card/README.md) in a [ledger](./components/ledger/README.md), then the pagination again with `lrssn-pagination--bottom`.
3. A list of topics beside the list, on a large screen, which moves the list into a stacked ledger.
4. An [empty state](./components/empty-state/README.md) in place of the list when it is empty, or has no results.

### A Post or an Article

1. The head as a ledger row: the facts in the margin, such as the date, the byline and the reading time, and the title and the lede beside them.
   A Post's title is Inter, and an Article's is Playfair Display.
2. The body as a ledger row: the [table of contents](./components/table-of-contents/README.md) in the margin, and the [prose](./components/prose/README.md) beside it, with [code blocks](./components/code-block/README.md) and [callouts](./components/callout/README.md).
3. The topics, the series and a link to the next entry at the end.

### An author's profile

1. A section head with the author's name as the title, and the counts in the margin.
2. A [carousel](./components/carousel/README.md) each of Articles and Posts.

## Anti-patterns

| Anti-pattern | Instead |
| --- | --- |
| A colour typed as a HEX value | Use its token. |
| Orange text in `primary-color` | Use `primary-text`. |
| White text on an orange fill | Use `text-on-primary`. |
| More than one orange fill on a screen | Keep one fill, and use a thin rule or an underline for the rest. |
| Plain or cool grey surfaces | Use the warm sand and timber of the themes. |
| A status shown by colour alone | Add words. |
| A shadow or a border on every block | Separate with space first. |
| Two Playfair Display lines in one view | Keep one, and set the rest in Inter. |
| Running text in Inter, or wider than 65 characters | Use the prose component. |
| A gradient, a decorative icon or an emoji | Let type and space do the work. |
| A dark theme made by inverting the light one | Use Lrssn Hearth. |

## See also

- [Lrssn brand guide](https://github.com/Lrssn-blog/Brand-guide)
- [Lrssn colour themes](https://github.com/Lrssn-blog/Color-theme)
- [Lrssn style guides](https://github.com/Lrssn-blog/Style-guide)
- [The design system on claude.ai](https://claude.ai/artifact/VYh8NPZg15HxgNvJkCzCVQ)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
