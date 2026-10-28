/**
 * @fileoverview Adds a Copy button to each code block, and to each block of
 * code in prose.
 */

/** How long "Copied" or "Copy failed" stays before the button resets. */
const RESET_DELAY_MS = 1800;

/**
 * Sets a button's visible text and its label for screen readers together.
 *
 * @param {!HTMLButtonElement} button
 * @param {string} text
 * @param {string} label
 */
function setLabel(button, text, label) {
    button.textContent = text;
    button.setAttribute('aria-label', label);
}

/**
 * Returns the Copy button of a block, and makes one if it has none.
 *
 * @param {!Element} block A `.lrssn-code-block`.
 * @return {!HTMLButtonElement}
 */
function copyButton(block) {
    let button = block.querySelector('.lrssn-code-block__copy');
    if (!button) {
        button = document.createElement('button');
        button.type = 'button';
        button.className = 'lrssn-code-block__copy';
        block.append(button);
    }
    setLabel(button, 'Copy', 'Copy code');
    button.hidden = false;
    return button;
}

/**
 * Wires the code blocks in a root. A bare `<pre>` in prose is wrapped in a
 * `.lrssn-code-block` first. A click copies the code with the Clipboard API,
 * says Copied or Copy failed, and resets. A block already wired is skipped,
 * so a second call does nothing.
 *
 * @param {!ParentNode=} root Where to look for code.
 */
export function initCodeCopy(root = document) {
    for (const pre of root.querySelectorAll('.lrssn-prose pre')) {
        if (pre.parentElement.classList.contains('lrssn-code-block')) {
            continue;
        }
        const block = document.createElement('div');
        block.className = 'lrssn-code-block';
        pre.before(block);
        block.append(pre);
    }
    for (const block of root.querySelectorAll('.lrssn-code-block')) {
        const pre = block.querySelector('pre');
        if (block.dataset.ready || !pre) {
            continue;
        }
        block.dataset.ready = 'true';
        const button = copyButton(block);
        button.addEventListener('click', async () => {
            const code = pre.querySelector('code') ?? pre;
            try {
                await navigator.clipboard.writeText(code.textContent ?? '');
                setLabel(button, 'Copied', 'Copied code');
            } catch {
                setLabel(button, 'Copy failed', 'Copy failed');
            }
            window.setTimeout(
                () => setLabel(button, 'Copy', 'Copy code'), RESET_DELAY_MS);
        });
    }
}
