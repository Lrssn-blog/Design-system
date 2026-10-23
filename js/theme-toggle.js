/**
 * @fileoverview Wires the System, Light and Dark buttons of the theme
 * toggle. js/theme-init.js applies the saved choice before the first paint;
 * this only shows and changes it.
 */

/** The key the choice is saved under, as the Lrssn website saves it. */
const STORAGE_KEY = 'theme';

/**
 * Reads a value back into a choice. Anything unknown means "system".
 *
 * @param {string|null|undefined} value
 * @return {string} 'system', 'light' or 'dark'.
 */
function parseChoice(value) {
    return value === 'light' || value === 'dark' ? value : 'system';
}

/**
 * Applies a choice to the page and saves it. "System" removes the attribute
 * and the saved value, so the page follows the device.
 *
 * @param {string} choice 'system', 'light' or 'dark'.
 */
function applyChoice(choice) {
    const root = document.documentElement;
    if (choice === 'system') {
        delete root.dataset.theme;
    } else {
        root.dataset.theme = choice;
    }
    try {
        if (choice === 'system') {
            localStorage.removeItem(STORAGE_KEY);
        } else {
            localStorage.setItem(STORAGE_KEY, choice);
        }
    } catch {
        // Storage can be blocked. The choice then lasts until the page
        // changes.
    }
}

/**
 * Marks the pressed button of every toggle on the page.
 *
 * @param {string} choice 'system', 'light' or 'dark'.
 */
function markChoice(choice) {
    const buttons = document.querySelectorAll(
            '.lrssn-theme-toggle [data-theme-choice]');
    for (const button of buttons) {
        const pressed = button.dataset.themeChoice === choice;
        button.setAttribute('aria-pressed', String(pressed));
    }
}

/**
 * Wires every theme toggle in a root. A toggle already wired is skipped,
 * so a second call does nothing.
 *
 * @param {!ParentNode=} root Where to look for toggles.
 */
export function initThemeToggles(root = document) {
    const toggles = root.querySelectorAll('.lrssn-theme-toggle');
    for (const toggle of toggles) {
        if (toggle.dataset.ready) {
            continue;
        }
        toggle.dataset.ready = 'true';
        for (const button of toggle.querySelectorAll('[data-theme-choice]')) {
            button.addEventListener('click', () => {
                const choice = parseChoice(button.dataset.themeChoice);
                applyChoice(choice);
                markChoice(choice);
            });
        }
    }
    markChoice(parseChoice(document.documentElement.dataset.theme));
}
