/**
 * @fileoverview Marks the section being read in each table of contents.
 */

/**
 * The watched box, as an IntersectionObserver `rootMargin`: from far above
 * the window down to a reading line 30% of the way down it. A heading only
 * enters or leaves the box by crossing the line, so a jump straight past
 * it, such as with the End key, still counts.
 */
const PASSED_LINE_MARGIN = '100000px 0px -70% 0px';

/**
 * Watches the headings a table of contents links to, and marks the link of
 * the last heading that has passed the reading line. Above the first
 * heading, no link is marked. Without IntersectionObserver, or without the
 * headings, it does nothing, and the list still links.
 *
 * @param {!Element} toc A `.lrssn-table-of-contents`.
 */
function watch(toc) {
    const links = new Map();
    for (const link of toc.querySelectorAll('a[href*="#"]')) {
        const id = decodeURIComponent(link.hash.slice(1));
        const heading = document.getElementById(id);
        if (heading) {
            links.set(heading, link);
        }
    }
    if (links.size === 0 || !('IntersectionObserver' in window)) {
        return;
    }
    const headings = [...links.keys()];
    const passed = new Set();
    const observer = new IntersectionObserver((entries) => {
        for (const entry of entries) {
            if (entry.isIntersecting) {
                passed.add(entry.target);
            } else {
                passed.delete(entry.target);
            }
        }
        const current = headings.findLast((heading) => passed.has(heading));
        for (const [heading, link] of links) {
            if (heading === current) {
                link.setAttribute('aria-current', 'true');
            } else {
                link.removeAttribute('aria-current');
            }
        }
    }, {rootMargin: PASSED_LINE_MARGIN});
    headings.forEach((heading) => observer.observe(heading));
}

/**
 * Wires every table of contents in a root. One already wired is skipped,
 * so a second call does nothing.
 *
 * @param {!ParentNode=} root Where to look for tables of contents.
 */
export function initTablesOfContents(root = document) {
    for (const toc of root.querySelectorAll('.lrssn-table-of-contents')) {
        if (toc.dataset.ready) {
            continue;
        }
        toc.dataset.ready = 'true';
        watch(toc);
    }
}
