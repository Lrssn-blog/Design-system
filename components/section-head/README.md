# Section head

A section head opens a section page, such as the Blog, with its title, a lede and links to its views.

## Use

- The section head is a ledger row: the margin holds the label Section and the section's path, such as `/blog`.
- The title is Playfair Display at the display size: the one brand moment of the page.
- The lede says what the section holds, in one or two sentences.
- The views, such as All posts, Series and Topics, sit under the lede.
  The current view has `aria-current="page"`, and an orange underline.
- A button for the one action the section offers, such as Create new post, sits at the right of the views.

## Markup

```html
<header class="lrssn-section-head lrssn-ledger">
  <div class="lrssn-ledger__row">
    <div class="lrssn-ledger__margin">
      <span class="lrssn-ledger__label">Section</span>
      <span>/blog</span>
    </div>
    <div class="lrssn-ledger__content">
      <h1 class="lrssn-section-head__title">Blog</h1>
      <p class="lrssn-section-head__lede">…</p>
      <div class="lrssn-section-head__bar">
        <nav class="lrssn-section-head__views" aria-label="Blog views">
          <a href="/blog" aria-current="page">All posts</a>
          <a href="/blog/series">Series</a>
          <a href="/blog/tags">Topics</a>
        </nav>
      </div>
    </div>
  </div>
</header>
```

## Accessibility

- The title is the page's `h1`.
- The views are a `<nav>`, named after the section.

## Do not

- Do not put a second Playfair Display line on the page.
- Do not put the lede in the margin.
