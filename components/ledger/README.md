# Ledger

The ledger is the signature layout of Lrssn: facts in a margin on the left, and the writing right of a thin orange rule, like a lab notebook.

## Use

- Put facts in the margin, in Geist Mono: dates as `YYYY-MM-DD`, bylines, reading time, series parts and the table of contents.
  Do not put sentences there.
- Put the writing in the content: titles, ledes, descriptions and the body of a page.
- Rows that follow each other share one unbroken rule, with a hairline between them.
- Use the stacked ledger where a sidebar leaves no room for the margin, such as a listing beside a list of topics, or a carousel.
- The post card, the section head and the empty state are ledger rows.

## Markup

```html
<div class="lrssn-ledger">
  <article class="lrssn-ledger__row">
    <div class="lrssn-ledger__margin">
      <time datetime="2026-10-23">2026-10-23</time>
      <span>Erik Larsson</span>
    </div>
    <div class="lrssn-ledger__content">
      …
    </div>
  </article>
</div>
```

`lrssn-ledger__label` is a small uppercase label for the margin, such as "Contents" or "Section".

## Variants

| Class | Use |
| --- | --- |
| `lrssn-ledger` | The margin on the left, and the rule between it and the content. |
| `lrssn-ledger lrssn-ledger--stacked` | The margin above the content, and the rule down the row's left edge. |

Below 720px, and on paper, every ledger stacks.

## Accessibility

- Mark up a date with `<time datetime="…">`, so it is read as a date.
- Keep the content's order the same as its reading order: the margin comes first in the markup and on the screen.

## Do not

- Do not draw the rule in another colour, or make it thicker than 1px.
- Do not put prose, buttons or images in the margin.
