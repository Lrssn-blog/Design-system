# Project card

A project card shows one project in a grid: its name, a summary, its status and its links.

## Use

- Put the cards in `lrssn-project-list`, a grid that fills the width with cards at least 18rem wide.
  Each card is as tall as its row.
- A card is the one element on the page with a border, a fill and a radius together, because it is a separate object.
- A cover image, if the project has one, runs the card's full width at 16:9 above the title.
- The summary is serif, like other writing.
- The meta line holds the status, as a pill in words, and the dates.
- The release card is a project card for one release.

## Markup

```html
<ul class="lrssn-project-list">
  <li>
    <article class="lrssn-project-card">
      <img class="lrssn-project-card__cover" src="cover.webp" alt="…" width="1600" height="900">
      <h2 class="lrssn-project-card__title"><a href="/projects/color-theme">Color-theme</a></h2>
      <p class="lrssn-project-card__summary">…</p>
      <p class="lrssn-project-card__meta"><span class="lrssn-project-card__status">Active</span><span>Since 2026</span></p>
      <ul class="lrssn-project-card__links"><li><a href="https://github.com/Lrssn-blog/Color-theme">Repository</a></li></ul>
    </article>
  </li>
</ul>
```

## Accessibility

- Give the cover an `alt` text, or `alt=""` when the title says it all.
- The status is a word, so it does not rely on its tint.

## Do not

- Do not add a shadow to a card.
- Do not put a coloured band behind a cover.
