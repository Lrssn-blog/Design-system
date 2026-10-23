# Footer

The footer closes every page with the logo, columns of links, and a line for the copyright and the licence.

## Use

- The footer has no band of colour: a hairline above it sets it apart.
- The brand column holds the logo, the tagline, the next step, such as Get in touch, and the social links.
- Group the other links in columns with a heading each, such as Read, About and Feeds.
- The last line, in Geist Mono, names the copyright holder and the licence of the writing, as a link.
- Inside `lrssn-page`, the footer sits at the bottom of the window when the page is short.

## Markup

```html
<footer class="lrssn-footer">
  <div class="lrssn-footer__inner">
    <div class="lrssn-footer__brand">
      <a class="lrssn-logo lrssn-logo--name-right" href="/">…</a>
      <p class="lrssn-footer__tagline">Notes from a curious engineer.</p>
      <a class="lrssn-link lrssn-link--next" href="/contact">Get in touch <span class="lrssn-link__arrow" aria-hidden="true">→</span></a>
    </div>
    <nav aria-labelledby="footer-read">
      <h2 class="lrssn-footer__heading" id="footer-read">Read</h2>
      <ul class="lrssn-footer__list">
        <li><a href="/blog">Blog</a></li>
      </ul>
    </nav>
    <p class="lrssn-footer__legal">© 2026 lrssn.com. Made by Erik Larsson. Writing licensed under <a rel="license" href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
  </div>
</footer>
```

## Accessibility

- Each column is a `<nav>`, named by its heading.
- The licence link has `rel="license"`.
- The footer is left out of print.

## Do not

- Do not list every page: group the links, and leave the rest to the header.
- Do not put a coloured band or a gradient behind the footer.
