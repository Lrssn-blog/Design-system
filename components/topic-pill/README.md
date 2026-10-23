# Topic pill

A topic pill names a topic of a Post or an Article, and links to the other writing on it.

## Use

- Readers see tags as topics, always as pills: on entries, on the item page, and in the home page's row of topics.
- A topic's own colour tints its pill: set it as `--topic-color` on the pill.
  The pill mixes it towards the theme's text colour, so it reads on light and dark.
- A topic without a colour of its own takes the cool accent, `secondary-text`.
- Put a row of pills in `lrssn-topic-pills`.

## Markup

```html
<ul class="lrssn-topic-pills">
  <li><a class="lrssn-topic-pill" href="/blog?tag=css">CSS</a></li>
  <li><a class="lrssn-topic-pill" href="/blog?tag=python" style="--topic-color: #3550b0">Python</a></li>
</ul>
```

## Accessibility

- The pill's name is its text, so the colour adds nothing a reader needs.
- A topic's own colour must keep the text at a contrast of 4.5 on the tint.
  The build checks the pill without a colour of its own; check a new topic colour in both themes.

## Do not

- Do not use pills for buttons or for a status.
- Do not write a topic in capitals.
