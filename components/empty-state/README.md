# Empty state

An empty state shows in place of a list that is empty, or has no results, and says where to go instead.

## Use

- An empty state is one ledger row: the margin says Empty, or No results.
- The title is one Playfair Display line that says what is missing: No papers yet.
- A sentence under it says why, as one person: I haven't put up a Paper yet.
- Then come links elsewhere, each with an arrow, and the one action the reader can take, if there is one.
- Use it on every list a reader can see, rather than a lone muted line.

## Markup

```html
<div class="lrssn-ledger">
  <section class="lrssn-ledger__row lrssn-empty-state" aria-labelledby="empty-state-title">
    <div class="lrssn-ledger__margin"><span class="lrssn-ledger__label">Empty</span></div>
    <div class="lrssn-ledger__content">
      <h2 class="lrssn-empty-state__title" id="empty-state-title">No papers yet.</h2>
      <p class="lrssn-empty-state__text">I haven't put up a Paper yet.</p>
      <ul class="lrssn-empty-state__links">
        <li><a href="/blog">Blog <span aria-hidden="true">→</span></a></li>
      </ul>
    </div>
  </section>
</div>
```

## Accessibility

- The section is named by its title.
- The links say where they go, and their arrows are hidden from screen readers.

## Do not

- Do not apologise, or blame the reader: say what is missing and where to go.
- Do not add an illustration or an emoji.
