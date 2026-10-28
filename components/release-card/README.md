# Release card

A release card shows the latest release of a project: its version, what it changed, its project and its date.

## Use

- A release card is a project card with `lrssn-release-card` added, so it sits in the same grid and looks the same.
- The title is the version, such as `v1.0.0`, and links to the release.
- The summary says what changed, in one or two sentences.
- The meta line links to the project, then gives the date as `YYYY-MM-DD`, and the milestone the release completes, if any.

## Markup

```html
<article class="lrssn-project-card lrssn-release-card">
  <h3 class="lrssn-project-card__title"><a class="lrssn-release-card__version" href="/projects/color-theme/releases/v1.0.0">v1.0.0</a></h3>
  <p class="lrssn-project-card__summary">…</p>
  <p class="lrssn-project-card__meta">
    <a href="/projects/color-theme">Color-theme</a>
    <time class="lrssn-release-card__date" datetime="2026-10-20">2026-10-20</time>
  </p>
</article>
```

## Accessibility

- Mark up the date with `<time datetime="…">`.
- Give the version link a label that names the project when the version stands alone, such as `aria-label="Color-theme v1.0.0"`.

## Do not

- Do not show more than the latest release on a card: link to the list of releases instead.
