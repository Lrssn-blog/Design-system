# Form field

A form field asks for one thing: its label, its control, and its hint or its error.

## Use

- Put the fields of a form in one column, in `lrssn-form`, with the button at the end.
- Write every label in sentence case, and say what to enter: Your name, Reply address, Message.
- Put a hint under the control when a field needs one, such as Optional.
- Write an error in words that say how to fix it: Write a message of at most 5,000 characters.
  Show it under the control, and mark the control `aria-invalid="true"`, which draws its border in `danger-color`.
- Group checkboxes or radio buttons that answer one question in `lrssn-fieldset`, with a `<legend>`.

## Markup

```html
<form class="lrssn-form" method="post" action="/contact">
  <div class="lrssn-form-field">
    <label class="lrssn-form-field__label" for="contact-email">Reply address</label>
    <input class="lrssn-input" id="contact-email" type="email" name="email" autocomplete="email" aria-describedby="contact-email-hint">
    <small class="lrssn-form-field__hint" id="contact-email-hint">Optional. Leave it empty if you don't need a reply.</small>
  </div>
  <label class="lrssn-check"><input type="checkbox" name="copy"> Send me a copy</label>
  <button class="lrssn-button" type="submit">Send message</button>
</form>
```

`lrssn-input` styles an `<input>`, a `<select>` and a `<textarea>`.

## Accessibility

- Every control has a `<label>`, and its hint and error are linked with `aria-describedby`.
- An error is text, not only the red border.
- A control's border reaches a contrast of 3 on the surface, in both themes.

## Do not

- Do not put the label inside the control as a placeholder.
- Do not mark a field as required only with a colour or an asterisk.
