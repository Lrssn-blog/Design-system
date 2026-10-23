/**
 * @fileoverview Shows and wires the Previous and Next buttons of each
 * carousel. The tracks scroll natively, with CSS scroll snapping, so they
 * already work by touch, trackpad and Tab without JavaScript.
 */

/**
 * Tells whether a track is scrolled to its start and to its end. Zoomed and
 * high-density screens scroll by fractions of a pixel and can stop just
 * short, hence the pixel of slack.
 *
 * @param {!Element} track
 * @return {{atStart: boolean, atEnd: boolean}}
 */
function scrollEnds(track) {
    return {
        atStart: track.scrollLeft <= 1,
        atEnd: track.scrollLeft + track.clientWidth >= track.scrollWidth - 1,
    };
}

/**
 * Wires every carousel in a root. A click scrolls the track by its visible
 * width, smoothly unless the reader prefers reduced motion. A button at its
 * end gets `aria-disabled`, not `disabled`, which would drop the keyboard
 * focus. The buttons stay hidden while every entry fits. A carousel already
 * wired is skipped, so a second call does nothing.
 *
 * @param {!ParentNode=} root Where to look for carousels.
 */
export function initCarousels(root = document) {
    for (const carousel of root.querySelectorAll('.lrssn-carousel')) {
        if (carousel.dataset.ready) {
            continue;
        }
        const track = carousel.querySelector('.lrssn-carousel__track');
        const controls = carousel.querySelector('.lrssn-carousel__controls');
        const previous = carousel.querySelector('[data-carousel="prev"]');
        const next = carousel.querySelector('[data-carousel="next"]');
        if (!track || !controls || !previous || !next) {
            continue;
        }
        carousel.dataset.ready = 'true';

        const update = () => {
            const {atStart, atEnd} = scrollEnds(track);
            controls.hidden = atStart && atEnd;
            previous.setAttribute('aria-disabled', String(atStart));
            next.setAttribute('aria-disabled', String(atEnd));
        };
        const page = (direction) => {
            const reduceMotion = window.matchMedia(
                    '(prefers-reduced-motion: reduce)').matches;
            track.scrollBy({
                left: direction * track.clientWidth,
                behavior: reduceMotion ? 'auto' : 'smooth',
            });
        };

        previous.addEventListener('click', () => page(-1));
        next.addEventListener('click', () => page(1));
        track.addEventListener('scroll', update, {passive: true});
        new ResizeObserver(update).observe(track);
        update();
    }
}
