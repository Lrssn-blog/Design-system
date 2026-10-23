/**
 * @fileoverview Applies the saved colour theme before the first paint.
 *
 * Load it in the head of every page, before the stylesheet, as a classic
 * script rather than a module: a module waits for the page to be parsed,
 * and the page would flash the wrong theme first.
 */

try {
    const theme = localStorage.getItem('theme');
    if (theme === 'light' || theme === 'dark') {
        document.documentElement.dataset.theme = theme;
    }
} catch {
    // Storage can be blocked, such as in a private window. Then the page
    // follows the device.
}
