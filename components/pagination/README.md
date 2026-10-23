# Pagination

Pagination moves between the pages of a long list, above it and below it.

## Use

- Show the pagination above and below every list that has more than one page, and leave it out when there is one.
- It starts with where the reader is: Page 2 of 5.
- Name the steps by what they lead to, such as Newer and Older for a blog, rather than Previous and Next.
- At the first or the last page, the step that leads nowhere stays in place, faded, so nothing shifts.
- Below the list, add `lrssn-pagination--bottom`, which moves the rule above it.

## Markup

```html
<nav class="lrssn-pagination" aria-label="Blog pages">
  <span class="lrssn-pagination__of">Page 2 of 5</span>
  <a href="/blog" aria-label="Newer posts">Newer</a>
  <ul class="lrssn-pagination__numbers">
    <li><a href="/blog">1</a></li>
    <li><a href="/blog/page/2" aria-current="page">2</a></li>
  </ul>
  <a href="/blog/page/3" aria-label="Older posts">Older</a>
</nav>
```

## Accessibility

- The two navigations of one list need different names, such as Blog pages and Blog pages, bottom.
- The current page has `aria-current="page"`.

## Do not

- Do not hide the page numbers on small screens: they wrap.
