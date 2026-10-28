# Design-system

This repo holds the Lrssn design system: the tokens, base styles and components that make a page look like Lrssn, in plain CSS with no framework.
It is a companion to the [Lrssn brand guide](https://github.com/Lrssn-blog/Brand-guide), the [Lrssn colour themes](https://github.com/Lrssn-blog/Color-theme) and the [Lrssn style guides](https://github.com/Lrssn-blog/Style-guide).

The [design guide](./Design.md) explains the principles, the tokens, the components and how they fit together.
To see every component in Lrssn Shore and Lrssn Hearth, open [`preview/index.html`](./preview/index.html) in a browser.
The same system is on claude.ai as the [Lrssn design system](https://claude.ai/artifact/VYh8NPZg15HxgNvJkCzCVQ), for designs and decks made there.

## Use

Copy `dist/`, `js/` and, if you need them, `assets/logo/` into a project, and load them in each page:

```html
<script src="js/theme-init.js"></script>
<link rel="stylesheet" href="dist/lrssn.css">
<script type="module" src="js/index.js"></script>
```

Then use the classes, such as `lrssn-button`, as each component's README shows.
[Getting started](./Design.md#getting-started) covers the fonts, the themes and Sass.

## Components

| Group | Components |
| --- | --- |
| Brand | [Logo](./components/logo/README.md) |
| Actions | [Button](./components/button/README.md), [Links](./components/link/README.md), [Theme toggle](./components/theme-toggle/README.md) |
| Forms | [Form field](./components/form-field/README.md) |
| Content | [Prose](./components/prose/README.md), [Code block](./components/code-block/README.md), [Callout](./components/callout/README.md), [Topic pill](./components/topic-pill/README.md) |
| Feedback | [Banner](./components/banner/README.md) |
| Layout | [Ledger](./components/ledger/README.md), [Header](./components/header/README.md), [Footer](./components/footer/README.md) |
| Site patterns | [Section head](./components/section-head/README.md), [Post card](./components/post-card/README.md), [Project card](./components/project-card/README.md), [Release card](./components/release-card/README.md), [Empty state](./components/empty-state/README.md), [Pagination](./components/pagination/README.md), [Carousel](./components/carousel/README.md), [Table of contents](./components/table-of-contents/README.md) |

## Layout

- `tokens/tokens.toml`: the tokens that are not colours, and what every token is for.
- `src/base.css`: the defaults for plain elements, such as the body, headings, links and focus.
- `components/<name>/`: each component's CSS, its README and an example.
- `js/`: the scripts of the components that need one.
- `templates/`: the preview page, and the cover of the design system on claude.ai.
- `scripts/build.py`: generates the files below from the colour themes and the sources above, and checks the contrast.
- `dist/`, `assets/logo/` and `preview/`: the generated files.
- `Design.md`: the design guide, whose tables are generated.

The colours are not in this repository.
The build reads them from the palettes of the [colour themes](https://github.com/Lrssn-blog/Color-theme/tree/main/palette), so a colour changes there, and then here with `scripts/build.py --write`.

## Checks

Pull requests run these checks via GitHub Actions:

- [markdownlint](https://github.com/DavidAnson/markdownlint-cli2) on the Markdown files.
- [Ruff](https://docs.astral.sh/ruff/) and [mypy](https://mypy-lang.org/) on the build script.
- `scripts/build.py`, which fails if a generated file is out of date, if a pair of colours has too little contrast, or if a stylesheet names a token that does not exist.
  It also runs every week, so a change to the colour themes shows here.
- `node --check` on the scripts.
- A link check with [lychee](https://github.com/lycheeverse/lychee).

To run them locally:

```bash
npx markdownlint-cli2
ruff check && ruff format --check
mypy scripts
scripts/build.py
for file in js/*.js; do node --check "$file"; done
lychee --config .lychee.toml '**/*.md'
```

`scripts/build.py` fetches the palettes from the `main` branch of Color-theme.
Pass the folder of a local copy to use that instead, for example `scripts/build.py --palettes ../Color-theme/palette`.
After changing a token, a component or a template, run `scripts/build.py --write`.

## The design system on claude.ai

The [Lrssn design system](https://claude.ai/artifact/VYh8NPZg15HxgNvJkCzCVQ) on claude.ai is made from this repository.
`scripts/build.py --artifact build/artifact` writes its files: the tokens in the shape it reads, this guide as its README, each component's README and preview, the stylesheet and the cover.
Publish them to the same link with Claude, after a change here, so that both stay the same.

## Licence

Copyright (C) 2026 Lrssn-blog.

The design system is free software: you can redistribute it and modify it under the terms of the [GNU Affero General Public License](./LICENSE), either version 3 of the License or (at your option) any later version.
