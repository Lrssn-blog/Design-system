# Table of contents

A table of contents lists the sections of a long page in the ledger's margin, and marks the one being read.

## Use

- Show it once a page has at least two headings at levels 2 and 3.
- It sits in the margin of the page's body, and stays in view while the reader scrolls.
  Below 720px, it sits above the body and scrolls with it.
- Level 3 headings are indented under their level 2 heading, in `lrssn-table-of-contents__nested`.
- `js/table-of-contents.js` marks the section being read, with `aria-current="true"` and an orange bar.
  Without JavaScript, the list still links to every section.

## Markup

```html
<nav class="lrssn-table-of-contents" aria-labelledby="contents-title">
  <h2 class="lrssn-ledger__label" id="contents-title">Contents</h2>
  <ol class="lrssn-table-of-contents__list">
    <li><a href="#principles">Principles</a></li>
    <li class="lrssn-table-of-contents__nested"><a href="#clear-space">Clear space</a></li>
  </ol>
</nav>
```

## Accessibility

- The list is a `<nav>`, named by its label, Contents.
- The section being read is marked with `aria-current`, not only with the bar.
- The table of contents is left out of print.

## Do not

- Do not list level 4 headings.
- Do not use it on a short page.
