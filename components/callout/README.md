# Callout

A callout sets a note, a tip, an important point, a warning or a caution apart from the text around it.

## Use

- Use the kind that fits, and use callouts sparingly: a page full of them sets nothing apart.
- The title names the kind in words, with an icon beside it, so the kind never relies on the colour.
- In Markdown, write a callout as GitHub's alerts are written: a quote that opens with `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` or `[!CAUTION]` on its own line.
- A note is neutral, in `text-color` on `surface-muted`, because the cool accent is too close to a tip.

## Markup

```html
<aside class="lrssn-callout lrssn-callout--tip">
  <p class="lrssn-callout__title">
    <svg class="lrssn-callout__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg>
    Tip
  </p>
  <p>Pass the path of a local copy to check the colours without the network.</p>
</aside>
```

## Variants

| Class | Title | Colours |
| --- | --- | --- |
| `lrssn-callout--note` | Note | `text-color` on `surface-muted` |
| `lrssn-callout--tip` | Tip | `success-color` on `success-background` |
| `lrssn-callout--important` | Important | `primary-text` on `primary-soft`, with a rule in `primary-color` |
| `lrssn-callout--warning` | Warning | `banner-warning-color` on `banner-warning-background` |
| `lrssn-callout--caution` | Caution | `danger-color` on `danger-background` |

The icons are the line icons of the Lrssn website, drawn on a 24px grid:

| Kind | Paths |
| --- | --- |
| Note | `M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z`, `M12 16v-5M12 8h.01` |
| Tip | `M9 18h6M10 21h4`, `M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z` |
| Important | `M5 4h14a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-5 4V5a1 1 0 0 1 1-1z`, `M12 7.5v4M12 14h.01` |
| Warning | `M12 3.5 21.5 20h-19z`, `M12 9.5v4.5M12 17h.01` |
| Caution | `M8.3 3h7.4L21 8.3v7.4L15.7 21H8.3L3 15.7V8.3z`, `M12 8v5M12 16h.01` |

## Accessibility

- Hide the icon from screen readers with `aria-hidden="true"`: the title says the kind.
- On paper, the box gets a full border, because printers leave out the tint.

## Do not

- Do not use a callout for the main point of a page.
- Do not put a callout inside another one.
