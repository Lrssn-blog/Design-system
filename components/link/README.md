# Links

A link takes the reader to another page, or to another place on this one.

## Use

- A link says where it goes: Download the CV (PDF, 120 KB), not Click here.
- In running text, a link is orange and underlined, so it does not rely on colour alone.
  Inside the prose component, every link looks like this without a class.
- In lists, the navigation and the footer, a link is quiet: muted, and underlined under the pointer.
- The title of an entry is a link in `text-color`, underlined in orange under the pointer.
- A link to the next step, such as Get in touch, ends with an arrow that moves under the pointer.

## Markup

```html
<a class="lrssn-link" href="https://lrssn.com/brand">Brand guide</a>
<a class="lrssn-link lrssn-link--next" href="/contact">Get in touch <span class="lrssn-link__arrow" aria-hidden="true">→</span></a>
```

## Variants

| Class | Use |
| --- | --- |
| `lrssn-link` | A link in running text. |
| `lrssn-link--quiet` | A link in a list, the navigation or the footer. |
| `lrssn-link--title` | The title of an entry, such as a post in a list. |
| `lrssn-link--next` | The next step, with `lrssn-link__arrow`. |

## Accessibility

- Hide the arrow from screen readers with `aria-hidden="true"`.
- Mark the link to the current page with `aria-current="page"`.

## Do not

- Do not write orange text in `primary-color`, which is too light to read on sand.
- Do not underline text that is not a link.
