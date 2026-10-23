# Code block

A code block shows code, in Geist Mono on the sunken surface, highlighted in the Lrssn themes' own colours.

## Use

- Use `lrssn-code` for code inside a sentence, such as a file name: `scripts/build.py`.
  Inside prose, `<code>` needs no class.
- Wrap a block in `lrssn-code-block`.
  Inside prose, a bare `<pre>` looks the same.
- The highlighting uses the `code-*` tokens, which are the syntax colours of Lrssn Shore and Lrssn Hearth.
  The stylesheet reads the classes of [highlight.js](https://highlightjs.org/), and sets the variables of [Shiki](https://shiki.style/)'s `css-variables` theme.
- `js/code-copy.js` adds a Copy button to each block in `lrssn-code-block`, and to each `<pre>` in prose.
  Without JavaScript, there is no button.

## Markup

```html
<div class="lrssn-code-block">
  <pre><code class="language-bash">scripts/build.py --write</code></pre>
</div>
```

With Shiki, choose the theme `css-variables`.
With highlight.js, load no theme of its own: the design system colours its classes.

## Accessibility

- Every code colour reaches a contrast of 4.5 on `surface-sunken`, in both themes.
- The Copy button says Copied, or Copy failed, after a click, and screen readers hear the same.
- A long line scrolls sideways inside the block, and wraps on paper.

## Do not

- Do not use a highlighting theme with colours from outside the palettes.
- Do not put a screenshot of code where the code itself would do.
