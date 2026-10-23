# Carousel

A carousel shows a row of entries that scrolls sideways, such as the Articles on an author's profile.

## Use

- Use a carousel for a short row of entries beside other content, and link to the full list with `lrssn-carousel__more`.
  For the main list of a page, use the ledger and pagination instead.
- The entries are post cards in a stacked ledger.
- The track scrolls natively and snaps to each entry, so it works by touch, trackpad and Tab without JavaScript.
- `js/carousel.js` shows the Previous and Next buttons, scrolls one width at a time, and hides the buttons while every entry fits.

## Markup

```html
<section class="lrssn-carousel" aria-labelledby="author-articles">
  <header class="lrssn-carousel__head">
    <h2 class="lrssn-carousel__title" id="author-articles">Articles</h2>
    <div class="lrssn-carousel__controls" hidden>
      <button class="lrssn-button lrssn-button--small lrssn-button--ghost" type="button" data-carousel="prev" aria-label="Previous articles">Previous</button>
      <button class="lrssn-button lrssn-button--small lrssn-button--ghost" type="button" data-carousel="next" aria-label="Next articles">Next</button>
    </div>
    <a class="lrssn-carousel__more" href="/articles">All articles</a>
  </header>
  <ol class="lrssn-carousel__track lrssn-ledger lrssn-ledger--stacked">
    <li class="lrssn-carousel__slide"><article class="lrssn-ledger__row lrssn-post-card">…</article></li>
  </ol>
</section>
```

## Accessibility

- The buttons are `hidden` until the script runs, so a reader without JavaScript gets no dead buttons.
- At an end, a button gets `aria-disabled="true"` rather than `disabled`, so it keeps the keyboard focus.
- The scroll is smooth, unless the reader prefers reduced motion.
- On paper, the entries stack.

## Do not

- Do not move the carousel by itself.
- Do not put the only copy of something in a carousel.
