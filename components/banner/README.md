# Banner

A banner tells every reader one thing across the top of the page, such as a change or an outage.

## Use

- Put banners in `lrssn-banner-stack`, under the header.
  The stack sticks under the header: set `--header-height` on it to the header's height.
- Keep the message to one sentence, with at most one link.
- Choose the kind by what the message is, and say it in words as well: the colour alone is not enough.
- A reader can close a banner that has a close button.
  Remember that choice on the page, such as in `localStorage`, until the banner changes.

## Markup

```html
<div class="lrssn-banner-stack">
  <div class="lrssn-banner lrssn-banner--warning" role="region" aria-label="Site announcement">
    <p class="lrssn-banner__message">The comments are read-only while I move the database.</p>
    <button class="lrssn-banner__dismiss" type="button" aria-label="Dismiss announcement">×</button>
  </div>
</div>
```

## Variants

| Class | Use |
| --- | --- |
| `lrssn-banner` | Information: the default. |
| `lrssn-banner--warning` | Something that may get in the reader's way. |
| `lrssn-banner--error` | Something that is broken. |
| `lrssn-banner--success` | Something that is done, such as Brand guide updated. |

## Accessibility

- Every kind's text reaches a contrast of 4.5 on its background, in both themes.
- The close button has a label, because × alone says nothing.
- Banners are left out of print.

## Do not

- Do not show more than two banners at once.
- Do not use a banner for a message about one form or one field: put that by the form.
- Do not use exclamation marks.
