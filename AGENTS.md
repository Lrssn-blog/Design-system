# AGENTS.md

Instructions for AI coding agents working in this repository.
For people, see `README.md`.

## Overview

This repository holds the Lrssn design system: tokens, base styles and components in plain CSS, with a few scripts.
The colours come from the palettes of the Lrssn colour themes, in the Color-theme repository, and `scripts/build.py` generates everything in `dist/`, `assets/logo/` and `preview/`, and the tables of `Design.md`.

## Commands

- Check the generated files and the contrast: `scripts/build.py`
- Regenerate the files after a change: `scripts/build.py --write`
- Use a local copy of the palettes: `scripts/build.py --palettes ../Color-theme/palette`
- Write the files of the design system on claude.ai: `scripts/build.py --artifact build/artifact`
- Lint the Markdown: `npx markdownlint-cli2`
- Lint and type-check the build script: `ruff check && ruff format --check` and `mypy scripts`
- Check the scripts: `for file in js/*.js; do node --check "$file"; done`
- Check the links: `lychee --config .lychee.toml '**/*.md'`

Run `scripts/build.py`, the Markdown lint, Ruff and mypy, and `node --check` before you say a task is done.

## Layout

- `tokens/tokens.toml`: the tokens that are not colours, the colours added to the website's, and a usage note for every token.
- `src/base.css`: the defaults for plain elements.
- `components/<name>/`: `<name>.css`, `README.md` and `example.html` for each component, listed in `COMPONENT_LIST` in `scripts/build.py`.
- `js/`: ES modules for the components that need a script, and `theme-init.js`, a classic script.
- `templates/preview.html` and `templates/cover.html`: the preview page, and the cover on claude.ai.
- `dist/`, `assets/logo/`, `preview/index.html` and the tables of `Design.md`: generated.
- `.github/workflows/`: CI.

## Conventions

- Follow the [Markdown style guide](https://github.com/Lrssn-blog/Style-guide/blob/main/src/markdown/Markdown.md).
  Write one sentence per line.
- Follow the [Python style guide](https://github.com/Lrssn-blog/Style-guide/blob/main/src/python/Python.md) for the build script, and the [JavaScript style guide](https://github.com/Lrssn-blog/Style-guide/blob/main/src/javascript/Javascript.md) for `js/`.
- Never edit a generated file by hand.
  Change the source and run `scripts/build.py --write`.
  `.gitattributes` lists the generated files.
- Never type a colour in CSS: use a `--lrssn-` token.
  To change a colour, change the palettes in Color-theme.
- Name custom properties `--lrssn-<token>` and classes `lrssn-<component>`, with BEM elements and modifiers such as `lrssn-button--ghost`.
  A component's own custom properties, which a page sets, have no prefix, such as `--topic-color`.
- Give every token a usage note.
- A new component needs its three files, an entry in `COMPONENT_LIST`, and a line in the table of `README.md`.
- Take the structure and spacing of a component from the Lrssn website, and its colours from the tokens.
- Keep every component usable without its script.
- Write in British English, in the voice of the [brand guide](https://github.com/Lrssn-blog/Brand-guide/blob/main/src/brand/Brand.md#voice).
  Examples use real Lrssn wording, never invented figures.

## Git and pull requests

- Follow the [Git style guide](https://github.com/Lrssn-blog/Style-guide/blob/main/src/git/Git.md) and the [Agentic development style guide](https://github.com/Lrssn-blog/Style-guide/blob/main/src/agentic/Agentic.md).
- `main` is the root branch.
  Work on a branch from `main`, and never commit to `main`.
- Open a pull request only when asked, against `main`.

## Boundaries

Ask first:

- Changing CI, the contrast rules in `scripts/build.py` or the lint configuration.
- Adding a dependency.
- Removing a token or a component.
- Publishing to the design system on claude.ai.

Never:

- Skip, weaken or disable a check to make it pass.
- Commit secrets.
