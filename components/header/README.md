# Header

The header holds the logo, the links to each section and the tools, at the top of every page.

## Use

- The header sticks to the top of the window, on the page's background, with a hairline under it.
  Add `lrssn-header--static` for a header that scrolls away.
- The logo comes first and links home.
- The links name the sections, in sentence case: Blog, Articles, Projects, About.
  The link of the section the page is in has `aria-current="page"`, and an orange underline.
- The tools sit at the right: the theme toggle, then any account controls.
- On phones, the links get a row of their own under the logo and the tools.

## Markup

```html
<header class="lrssn-header">
  <div class="lrssn-header__bar">
    <nav class="lrssn-header__nav" aria-label="Site">
      <a class="lrssn-logo lrssn-logo--name-right" href="/">…</a>
      <ul class="lrssn-header__links">
        <li><a class="lrssn-header__link" href="/blog" aria-current="page">Blog</a></li>
        <li><a class="lrssn-header__link" href="/articles">Articles</a></li>
      </ul>
      <div class="lrssn-header__tools">
        <div class="lrssn-theme-toggle" role="group" aria-label="Colour theme">…</div>
      </div>
    </nav>
  </div>
</header>
```

## Accessibility

- The navigation is a `<nav>` named Site.
- The current section is marked with `aria-current`, not only with the underline.
- The header is left out of print.

## Do not

- Do not give the header a coloured band or a shadow: the hairline sets it apart.
- Do not put more than one orange fill in it.
