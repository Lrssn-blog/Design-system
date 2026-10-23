# Prose

Prose sets running text, such as the body of a Post or an Article, and everything rendered Markdown can hold.

## Use

- Put the body of a page in `lrssn-prose`, and its elements need no classes of their own.
- Running text is Merriweather in `text-body`, at most 65 characters wide, with a line height of 1.8.
  Headings inside it are Inter.
- Links are orange and underlined.
- Quotes have a rule in the cool accent, and tables scroll sideways inside the column when they are wide.
- Code and callouts inside prose are styled by the [code block](../code-block/README.md) and the [callout](../callout/README.md).
- Task lists and footnotes follow the classes of GitHub Flavored Markdown, as `remark-gfm` writes them: `contains-task-list`, `task-list-item` and `footnotes`.

## Markup

```html
<div class="lrssn-prose">
  <p>It cut the build from 4 minutes to 50 seconds, at the cost of a bigger image.</p>
  <div class="lrssn-prose__heading">
    <h2 id="the-trade-off">The trade-off</h2>
    <a class="lrssn-prose__anchor" href="#the-trade-off" aria-label="Link to this section">#</a>
  </div>
  <p>…</p>
</div>
```

A heading can sit beside a `#` link to itself, in `lrssn-prose__heading`.
The link shows on hover and keyboard focus, and always on touch screens.

## Accessibility

- Keep the headings in order: one `h1` for the page, then `h2` and `h3`.
- Give every image an `alt` text that says what it shows.
- The `#` link has a label, because `#` alone says nothing.

## Do not

- Do not centre running text.
- Do not set running text in Inter or Playfair Display.
- Do not make it wider than 65 characters.
