# Logo

The logo shows the Lrssn mark and name, and the username where it fits.

## Use

- Show the name and the username through the logo, and never retype them in another typeface.
- In the header and the footer, the logo links home.
- The mark and the name always share one colour: `primary-text` on screen.
  For one colour on its own, set `color` on the logo to `text-color`.
- The rules for clear space, minimum size and misuse are in the [brand guide](https://github.com/Lrssn-blog/Brand-guide/blob/main/src/brand/Brand.md#logo).
  The mark must be at least 16px tall, and at least 24px tall beside the name.
- For a file, such as an avatar or a slide, use one of the logo files in [`assets/logo/`](../../assets/logo).

## Markup

The mark is inline SVG, so it takes the colour of the text.
Beside the name, hide the mark from screen readers, which read the name:

```html
<a class="lrssn-logo lrssn-logo--name-right" href="/">
  <svg class="lrssn-logo__mark" viewBox="0 0 1024 1024" aria-hidden="true" focusable="false">
    <rect x="1.996" y="1.996" width="1024" height="1024"/>
    <path d="M 0,0 C 0,0 172.70142,400 300,400 427.29858,400 450,283.06338 450,200 450,116.93662 410.37878,32 300,32 189.62122,32 32,235.85662 32,400 32,564.14337 247.6061,800 400,800 552.3939,800 686.87474,736.95919 800,650 913.12526,563.04081 1000,386.02764 1000,250 1000,113.97236 975.41249,32 850,32 724.58751,32 602.70819,190.36077 600,400 c -2.70819,209.63923 144.31818,407.41557 250,500 100.29166,87.86228 174,124 174,124"/>
  </svg>
  <span class="lrssn-logo__name">Lrssn</span>
</a>
```

On its own, give the mark `role="img"` and `aria-label="Lrssn logo"` instead.

## Variants

| Class | Use |
| --- | --- |
| `lrssn-logo--name-right` | The mark and the name: the default, as in the header and the footer. |
| `lrssn-logo--name-user-right` | The mark, with the name over the username in `lrssn-logo__text`: the header, for someone signed in. |
| `lrssn-logo--name-below` | The name under the mark: square spaces, such as a profile card or a slide. |
| `lrssn-logo--icon-only` | The mark only: small spaces, such as an avatar. |

## Accessibility

- A logo that links home is named by its text, "Lrssn".
- A mark on its own is an image named "Lrssn logo".

## Do not

- Do not stretch, squash or rotate the logo.
- Do not draw it in a colour other than the orange, `text-color` or `primary-text`.
- Do not add a shadow, an outline or a gradient.
- Do not write the name in another typeface, or in capitals.
