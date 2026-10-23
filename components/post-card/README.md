# Post card

A post card is one entry in a list of Posts or Articles: a ledger row with the facts in the margin and the title, the description and the topics beside them.

## Use

- The margin holds the date as `YYYY-MM-DD`, the byline and any badges, such as New.
- A Post's title is Inter.
  An Article's title is Playfair Display, with a serif description, because Articles are the longer pieces: add `lrssn-post-card--article`.
- The foot holds the series and its part, then the topic pills.
- Entries have no cover image.
- Put the entries in a `lrssn-ledger`, so their rows share one rule.
  In a carousel, the ledger is stacked.

## Markup

```html
<div class="lrssn-ledger">
  <article class="lrssn-ledger__row lrssn-post-card">
    <div class="lrssn-ledger__margin">
      <time datetime="2026-10-23">2026-10-23</time>
      <a class="lrssn-post-card__byline" href="/authors/erik-larsson">Erik Larsson</a>
      <span class="lrssn-post-card__badges"><span class="lrssn-badge lrssn-badge--new">New</span></span>
    </div>
    <div class="lrssn-ledger__content">
      <h2 class="lrssn-post-card__title"><a href="/blog/hearth-and-shore-for-homarr">Hearth and Shore for Homarr</a></h2>
      <p class="lrssn-post-card__description">…</p>
      <div class="lrssn-post-card__foot">
        <a class="lrssn-post-card__series" href="/blog/series/colour-themes"><span class="lrssn-post-card__series-name">Colour themes</span> · part 3</a>
        <ul class="lrssn-topic-pills">…</ul>
      </div>
    </div>
  </article>
</div>
```

## Variants

| Class | Use |
| --- | --- |
| `lrssn-post-card` | A Post. |
| `lrssn-post-card--article` | An Article. |
| `lrssn-badge--new`, `lrssn-badge--tutorial`, `lrssn-badge--article` | The badges in the margin. |

## Accessibility

- The title is the entry's heading, and its link names the entry.
- The badges are words, so they do not rely on their tint.

## Do not

- Do not add a cover image or a shadow to an entry.
- Do not put the description in the margin.
