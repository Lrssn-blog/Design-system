/**
 * @fileoverview Wires every component of the Lrssn design system that needs
 * JavaScript. Load it as a module, which runs once the page is parsed:
 *
 *     <script type="module" src="js/index.js"></script>
 *
 * Each component works without it, and loses only its controls.
 */

import {initCarousels} from './carousel.js';
import {initCodeCopy} from './code-copy.js';
import {initTablesOfContents} from './table-of-contents.js';
import {initThemeToggles} from './theme-toggle.js';

initThemeToggles();
initCarousels();
initCodeCopy();
initTablesOfContents();
