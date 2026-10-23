# Button

A button starts an action, or leads to the one next step that matters.

## Use

- Use the primary button for the one main action of a view, such as Send message.
  It is the brand orange as a fill, so use it at most once per screen.
- Use the secondary button for the actions beside it, and the ghost button for quiet ones, such as Previous and Next.
- Write the label in sentence case, and start it with a verb: Send message, Download the CV (PDF, 120 KB).
- Use `<button>` for an action and `<a>` for a page to go to, with the same classes.

## Markup

```html
<button class="lrssn-button" type="submit">Send message</button>
<a class="lrssn-button lrssn-button--secondary" href="/cv.pdf">Download the CV (PDF, 120 KB)</a>
```

## Variants

| Class | Use |
| --- | --- |
| `lrssn-button` | The primary action: an orange fill with `text-on-primary`. |
| `lrssn-button--secondary` | A supporting action: a border in `border-color-input`. |
| `lrssn-button--ghost` | A quiet action: orange text and an orange border, which do not count as a fill. |
| `lrssn-button--small` | A smaller button, such as Create new post in a section head. |

A button that cannot be used yet has the `disabled` attribute, or `aria-disabled="true"` when it must keep the keyboard focus.

## Accessibility

- A button is at least 40px tall, and a small one 32px.
- Its label says what happens, without the icon or the colour.
- Keyboard focus shows the focus ring, as everywhere.

## Do not

- Do not put white text on the orange fill.
- Do not put two primary buttons on one screen.
- Do not make a link in running text into a button.
