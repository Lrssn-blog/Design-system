#!/usr/bin/env python3
"""Builds the Lrssn design system from its tokens and components.

The colours come from the palettes of the Lrssn colour themes, in the
Color-theme repository, and every other token from tokens/tokens.toml.
This script writes the tokens as CSS, Sass and JSON, joins the base styles
and the components into one stylesheet, draws the logo files, writes the
preview page and the tables of Design.md, and checks that every pair of
colours the components use has enough contrast.

Usage:
    scripts/build.py                  Check that every generated file is up
                                      to date.
    scripts/build.py --write          Regenerate the files.
    scripts/build.py --artifact DIR   Also write the files of the claude.ai
                                      design system to DIR.
    scripts/build.py --palettes DIR   Read the palettes from DIR, such as
                                      ../Color-theme/palette, instead of
                                      fetching them from Color-theme's main.
"""

import argparse
from collections.abc import Iterable
import dataclasses
import difflib
import json
import pathlib
import re
import sys
import tomllib
from typing import Any
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = ROOT / 'tokens' / 'tokens.toml'
SOURCE = ROOT / 'src'
COMPONENTS = ROOT / 'components'
TEMPLATES = ROOT / 'templates'
SCRIPTS = ROOT / 'js'
GUIDE = ROOT / 'Design.md'

PALETTE_URL = (
    'https://raw.githubusercontent.com/Lrssn-blog/Color-theme/main/'
    'palette/{name}.toml'
)
REPOSITORY = 'https://github.com/Lrssn-blog/Design-system/blob/main/'

# The prefix of every custom property and class.
PREFIX = 'lrssn'

# The themes, as (id, palette): the id is the value of `data-theme`.
THEMES = (('light', 'shore'), ('dark', 'hearth'))

# The first website token of each group, in the order of Color-theme's maps.
WEBSITE_GROUPS = {
    'primary-color': 'Brand',
    'background': 'Surfaces',
    'text-color': 'Text',
    'border-color': 'Borders',
    'success-color': 'Status',
    'banner-info-background': 'Banners',
    'tag-background-hover': 'Tags & media',
}
COLOUR_GROUPS = (*WEBSITE_GROUPS.values(), 'Code')

# The families of tokens/tokens.toml other than colour, and their titles.
FAMILIES = {
    'font': 'Typefaces',
    'font-size': 'Font sizes',
    'line-height': 'Line heights',
    'space': 'Spacing',
    'radius': 'Radii',
    'shadow': 'Shadows',
    'transition': 'Motion',
    'z-index': 'Stacking',
    'layout': 'Layout',
}

# The components, in the order of the stylesheet, and their groups.
COMPONENT_LIST = (
    ('ledger', 'Layout'),
    ('logo', 'Brand'),
    ('button', 'Actions'),
    ('link', 'Actions'),
    ('theme-toggle', 'Actions'),
    ('form-field', 'Forms'),
    ('prose', 'Content'),
    ('code-block', 'Content'),
    ('callout', 'Content'),
    ('topic-pill', 'Content'),
    ('banner', 'Feedback'),
    ('header', 'Layout'),
    ('footer', 'Layout'),
    ('section-head', 'Site patterns'),
    ('post-card', 'Site patterns'),
    ('project-card', 'Site patterns'),
    ('release-card', 'Site patterns'),
    ('empty-state', 'Site patterns'),
    ('pagination', 'Site patterns'),
    ('carousel', 'Site patterns'),
    ('table-of-contents', 'Site patterns'),
)
COMPONENT_GROUPS = (
    'Brand',
    'Actions',
    'Forms',
    'Content',
    'Feedback',
    'Layout',
    'Site patterns',
)

# The components the preview shows one above the other, at the full width,
# because they fill the width of a page.
WIDE = frozenset(
    (
        'ledger',
        'header',
        'footer',
        'section-head',
        'post-card',
        'empty-state',
        'carousel',
        'table-of-contents',
    )
)

# The modules of js/ that js/index.js imports.
SCRIPT_MODULES = (
    'theme-toggle.js',
    'carousel.js',
    'code-copy.js',
    'table-of-contents.js',
)

# The logo mark, as the Lrssn website draws it (src/lib/brand.ts of
# Lrssn-com): a frame and one line, stroked on a 1024 grid.
LOGO_VIEWBOX = '0 0 1024 1024'
LOGO_RECT = 'x="1.996" y="1.996" width="1024" height="1024"'
LOGO_PATH = (
    'M 0,0 C 0,0 172.70142,400 300,400 427.29858,400 450,283.06338 '
    '450,200 450,116.93662 410.37878,32 300,32 189.62122,32 32,235.85662 '
    '32,400 32,564.14337 247.6061,800 400,800 552.3939,800 686.87474,'
    '736.95919 800,650 913.12526,563.04081 1000,386.02764 1000,250 '
    '1000,113.97236 975.41249,32 850,32 724.58751,32 602.70819,190.36077 '
    '600,400 c -2.70819,209.63923 144.31818,407.41557 250,500 '
    '100.29166,87.86228 174,124 174,124'
)
# The logo files the brand guide names: a colour, and its token and theme.
LOGO_FILES = {
    'orange': ('primary-color', 'light'),
    'dark': ('text-color', 'light'),
    'light': ('text-color', 'dark'),
}

# Body text needs 4.5, and large text and graphics need 3 (WCAG 2.2).
TEXT = 4.5
GRAPHICS = 3.0

TEXT_TOKENS = (
    'text-color',
    'text-strong',
    'text-body',
    'text-muted',
    'text-subtle',
    'primary-text',
    'secondary-text',
    'link-color',
    'success-color',
    'danger-color',
    'warning-color',
    'info-color',
)
SURFACES = ('background', 'surface')
CODE_TOKENS = (
    'code-keyword',
    'code-function',
    'code-string',
    'code-number',
    'code-type',
    'code-builtin',
    'code-tag',
    'code-property',
    'code-parameter',
    'code-operator',
    'code-punctuation',
    'code-escape',
    'code-comment',
)
# A topic pill without a colour of its own: its text and its tint, as
# `topic-pill.css` mixes them.
TOPIC_TEXT = 'mix(secondary-text 55%, text-color)'
TOPIC_TINT = 'mix(secondary-text 14%, surface)'

# The pairs the components use, beyond every text token on the page and the
# surface. Each rule is (foregrounds, backgrounds, minimum ratio).
Rule = tuple[Iterable[str], Iterable[str], float]
PAIRS: tuple[Rule, ...] = (
    (
        ('text-color',),
        (
            'surface-muted',
            'surface-sunken',
            'surface-hover',
            'primary-soft',
            'secondary-soft',
        ),
        TEXT,
    ),
    (
        ('text-body',),
        (
            'surface-muted',
            'success-background',
            'primary-soft',
            'banner-warning-background',
            'danger-background',
        ),
        TEXT,
    ),
    (('text-on-primary',), ('primary-color',), TEXT),
    (('primary-text',), ('primary-soft',), TEXT),
    (('secondary-text',), ('secondary-soft',), TEXT),
    (('success-color',), ('success-background',), TEXT),
    (('danger-color',), ('danger-background',), TEXT),
    *(
        ((f'banner-{kind}-color',), (f'banner-{kind}-background',), TEXT)
        for kind in ('info', 'warning', 'error', 'success')
    ),
    ((TOPIC_TEXT,), (TOPIC_TINT,), TEXT),
    (CODE_TOKENS, ('surface-sunken',), TEXT),
    (('border-color-input', 'focus-color'), SURFACES, GRAPHICS),
)

HEX = re.compile(r'^#[0-9a-f]{6}$')
MIX = re.compile(r'^mix\(([\w-]+) (\d+)%, ([\w-]+)\)$')
TOKEN_REFERENCE = re.compile(r'var\(--' + PREFIX + r'-([\w-]+)')
PLACEHOLDER = re.compile(r'\{\{ ([\w-]+) \}\}')
MARKERS = re.compile(
    r'(<!-- generated:([\w-]+) -->\n).*?(<!-- end:\2 -->)', re.DOTALL
)
# The attributes that hold ids, which the preview makes unique per theme.
ID_ATTRIBUTE = re.compile(
    r'\b(id|for|aria-describedby|aria-labelledby|aria-controls)="([^"]+)"'
)
ID_LINK = re.compile(r'href="#([^"]+)"')
MARKDOWN_LINK = re.compile(r'\]\((?!https?:|#|mailto:)(?:\./)?([^)]+)\)')

# The font files already uploaded to the claude.ai design system.
ARTIFACT_FONTS = (
    ('Inter', 'Inter-Variable.ttf', 'normal'),
    ('Inter', 'Inter-Italic-Variable.ttf', 'italic'),
    ('Merriweather', 'Merriweather-Variable.ttf', 'normal'),
    ('Merriweather', 'Merriweather-Italic-Variable.ttf', 'italic'),
    ('Geist Mono', 'GeistMono-Variable.ttf', 'normal'),
    ('Geist Mono', 'GeistMono-Italic-Variable.ttf', 'italic'),
    ('Playfair Display', 'PlayfairDisplay-Variable.ttf', 'normal'),
    ('Playfair Display', 'PlayfairDisplay-Italic-Variable.ttf', 'italic'),
)
# The keys of the claude.ai design system's font families.
ARTIFACT_FAMILIES = {
    'font-display': 'display',
    'font-ui': 'ui',
    'font-serif': 'serif',
    'font-mono': 'mono',
}
# The families of the claude.ai design system, as {family: key}.
ARTIFACT_KEYS = {
    'space': 'spacing',
    'radius': 'radius',
    'shadow': 'shadow',
    'font-size': 'fontSize',
    'line-height': 'lineHeight',
    'transition': 'transition',
    'z-index': 'zIndex',
    'layout': 'layout',
}

GENERATED = 'Generated by scripts/build.py. Do not edit.'


@dataclasses.dataclass(frozen=True)
class Theme:
    """A theme: its id, its name, and the HEX value of each palette role.

    `roles` holds the roles of the palette's [colors] table, such as `bg`,
    and its website tokens, with `website.` before them.
    """

    id: str
    name: str
    roles: dict[str, str]
    website: list[str]


@dataclasses.dataclass(frozen=True)
class Token:
    """A token: its family, its group, its value in each theme and its use.

    A token whose value does not depend on the theme has the same value
    under every theme id.
    """

    name: str
    family: str
    group: str
    values: dict[str, str]
    usage: str
    themed: bool

    @property
    def value(self) -> str:
        """Returns the value in the first theme."""
        return self.values[THEMES[0][0]]


@dataclasses.dataclass(frozen=True)
class Component:
    """A component: its folder name, its group, and its three files."""

    name: str
    group: str
    css: str
    readme: str
    example: str

    @property
    def title(self) -> str:
        """Returns the title of the README, such as 'Topic pill'."""
        return self.readme.splitlines()[0].removeprefix('# ')

    @property
    def summary(self) -> str:
        """Returns the first sentence of the README, after its title."""
        lines = (line.strip() for line in self.readme.splitlines()[1:])
        return next(line for line in lines if line)

    @property
    def pascal(self) -> str:
        """Returns the name in PascalCase, such as 'TopicPill'."""
        return ''.join(part.title() for part in self.name.split('-'))


def resolve(
    value: str, colors: dict[str, str], seen: tuple[str, ...] = ()
) -> str:
    """Returns the HEX colour of a value, following `@role` references."""
    if not value.startswith('@'):
        if not HEX.match(value):
            raise SystemExit(f'{value!r} is not a colour such as #fc6600')
        return value
    role = value[1:]
    if role in seen:
        raise SystemExit(f'{role}: refers to itself')
    if role not in colors:
        raise SystemExit(f'{value}: there is no such role in [colors]')
    return resolve(colors[role], colors, (*seen, role))


def read_palette(name: str, directory: pathlib.Path | None) -> str:
    """Returns the text of a palette, from a directory or from Color-theme."""
    if directory is not None:
        return (directory / f'{name}.toml').read_text()
    url = PALETTE_URL.format(name=name)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return str(response.read().decode())
    except urllib.error.URLError as e:
        raise SystemExit(
            f'Could not fetch {url}: {e}\n'
            'Pass --palettes with the path of a local copy instead.'
        ) from e


def load_theme(
    theme_id: str, palette: str, directory: pathlib.Path | None
) -> Theme:
    """Reads a palette, and resolves the value of every role."""
    data = tomllib.loads(read_palette(palette, directory))
    colors = data['colors']
    roles = {}
    for table in ('colors', 'website'):
        prefix = '' if table == 'colors' else f'{table}.'
        for role, value in data[table].items():
            try:
                roles[prefix + role] = resolve(value, colors)
            except SystemExit as e:
                raise SystemExit(f'{palette}.toml: {role}: {e}') from e
    return Theme(theme_id, data['meta']['name'], roles, list(data['website']))


def with_alpha(hex_value: str, opacity: float) -> str:
    """Adds an opacity from 0 to 1 to a colour, such as '#fc6600b3'."""
    return hex_value + f'{round(opacity * 255):02x}'


def entry(family: str, name: str, data: object) -> tuple[str, str]:
    """Returns the value and the usage note of a token of tokens.toml."""
    if not isinstance(data, dict) or not {'value', 'usage'} <= data.keys():
        raise SystemExit(
            f'tokens.toml: [{family}] {name} needs a value and a usage note'
        )
    return str(data['value']), str(data['usage'])


def load_tokens(themes: list[Theme], config: dict[str, Any]) -> list[Token]:
    """Returns every token: the colours first, by group, then the others."""
    ids = [theme.id for theme in themes]
    usage: dict[str, str] = config['colour']['usage']
    colours: list[Token] = []
    group = ''
    for name in themes[0].website:
        group = WEBSITE_GROUPS.get(name, group)
        values = {t.id: t.roles[f'website.{name}'] for t in themes}
        colours.append(Token(name, 'colour', group, values, '', True))
    for name, data in config['colour']['roles'].items():
        role = data['role']
        if any(role not in theme.roles for theme in themes):
            raise SystemExit(f'tokens.toml: {name}: no role {role!r}')
        values = {theme.id: theme.roles[role] for theme in themes}
        colours.append(Token(name, 'colour', data['group'], values, '', True))
    for name, data in config['colour']['alpha'].items():
        source = next(t for t in colours if t.name == data['token'])
        values = {
            theme_id: with_alpha(source.values[theme_id], data['alpha'])
            for theme_id in ids
        }
        colours.append(Token(name, 'colour', data['group'], values, '', True))
    for token in colours:
        if token.name not in usage:
            raise SystemExit(
                f'tokens.toml: [colour.usage] has no note for {token.name}'
            )
    names = {token.name for token in colours}
    for name in usage:
        if name not in names:
            raise SystemExit(
                f'tokens.toml: [colour.usage] {name} is not a colour token'
            )
    colours = [dataclasses.replace(t, usage=usage[t.name]) for t in colours]
    colours.sort(key=lambda token: COLOUR_GROUPS.index(token.group))

    others = []
    for family, title in FAMILIES.items():
        for name, data in config[family].items():
            value, note = entry(family, name, data)
            if family == 'shadow':
                values = {
                    theme.id: f'{value} '
                    + with_alpha(theme.roles['shadow'], data['alpha'])
                    for theme in themes
                }
                token = Token(name, family, title, values, note, True)
            else:
                values = dict.fromkeys(ids, value)
                token = Token(name, family, title, values, note, False)
            others.append(token)
    tokens = colours + others
    seen: set[str] = set()
    for token in tokens:
        if token.name in seen:
            raise SystemExit(f'tokens.toml: {token.name} is defined twice')
        seen.add(token.name)
    return tokens


def load_components() -> list[Component]:
    """Reads the three files of every component, and checks the list."""
    folders = {path.name for path in COMPONENTS.iterdir() if path.is_dir()}
    listed = {name for name, _ in COMPONENT_LIST}
    for name in sorted(folders - listed):
        raise SystemExit(f'components/{name} is not in COMPONENT_LIST')
    components = []
    for name, group in COMPONENT_LIST:
        folder = COMPONENTS / name
        files = [folder / f'{name}.css', folder / 'README.md']
        files.append(folder / 'example.html')
        for path in files:
            if not path.exists():
                raise SystemExit(f'{path.relative_to(ROOT)} is missing')
        css, readme, example = (path.read_text() for path in files)
        components.append(Component(name, group, css, readme, example))
    return components


def luminance(hex_value: str) -> float:
    """Returns the WCAG relative luminance of a colour such as '#fc6600'."""
    channels = []
    for start in (1, 3, 5):
        value = int(hex_value[start : start + 2], 16) / 255
        if value <= 0.03928:
            channels.append(value / 12.92)
        else:
            channels.append(((value + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first: str, second: str) -> float:
    """Returns the WCAG contrast ratio of two colours."""
    lighter, darker = sorted((luminance(first), luminance(second)))[::-1]
    return (lighter + 0.05) / (darker + 0.05)


def colour(expression: str, values: dict[str, str]) -> str:
    """Returns the HEX value of a colour token or of a mix of two.

    A mix is written as CSS's `color-mix(in srgb, …)` mixes them, such as
    `mix(secondary-text 55%, text-color)`.
    """
    match = MIX.match(expression)
    if not match:
        return values[expression]
    first, percent, second = match.groups()
    weight = int(percent) / 100
    channels = []
    for start in (1, 3, 5):
        a = int(values[first][start : start + 2], 16)
        b = int(values[second][start : start + 2], 16)
        channels.append(round(a * weight + b * (1 - weight)))
    return '#' + ''.join(f'{value:02x}' for value in channels)


def rules() -> list[tuple[str, str, float]]:
    """Returns every contrast rule as (foreground, background, minimum)."""
    every = [(TEXT_TOKENS, SURFACES, TEXT), *PAIRS]
    return [
        (foreground, background, minimum)
        for foregrounds, backgrounds, minimum in every
        for foreground in foregrounds
        for background in backgrounds
    ]


def check_contrast(tokens: list[Token]) -> list[str]:
    """Checks every contrast rule in every theme."""
    errors = []
    for theme_id, _ in THEMES:
        values = {t.name: t.values[theme_id] for t in tokens if t.themed}
        for foreground, background, minimum in rules():
            ratio = contrast_ratio(
                colour(foreground, values), colour(background, values)
            )
            if ratio < minimum:
                errors.append(
                    f'{theme_id}: {foreground} on {background} is '
                    f'{ratio:.2f}, needs {minimum}'
                )
    return errors


def check_references(tokens: list[Token]) -> list[str]:
    """Checks that every `var(--lrssn-…)` in the sources names a token."""
    names = {token.name for token in tokens}
    paths = [
        *SOURCE.glob('*.css'),
        *COMPONENTS.glob('*/*.css'),
        *COMPONENTS.glob('*/*.html'),
        *TEMPLATES.glob('*.html'),
    ]
    errors = []
    for path in sorted(paths):
        for name in TOKEN_REFERENCE.findall(path.read_text()):
            if name not in names:
                errors.append(f'{path.relative_to(ROOT)}: no token {name!r}')
    return errors


def indent(text: str, spaces: int = 4) -> str:
    """Indents every line of a text that is not empty."""
    return ''.join(
        ' ' * spaces + line if line.strip() else line
        for line in text.splitlines(keepends=True)
    )


def declarations(tokens: Iterable[Token], theme_id: str) -> str:
    """Returns the custom properties of some tokens in one theme."""
    return ''.join(
        f'--{PREFIX}-{token.name}: {token.values[theme_id]};\n'
        for token in tokens
    )


def block(selectors: list[str], body: str) -> str:
    """Returns a CSS rule with an indented body."""
    return ',\n'.join(selectors) + ' {\n' + indent(body) + '}\n'


def tokens_css(tokens: list[Token]) -> str:
    """Returns the tokens as custom properties, without a header.

    Shore applies by default, Hearth when the device prefers dark and the
    page does not ask for light, and either one inside an element with
    `data-theme`. Paper is light, so print applies Shore again.
    """
    themed = [token for token in tokens if token.themed]
    plain = [token for token in tokens if not token.themed]
    (light, _), (dark, _) = THEMES
    light_body = 'color-scheme: light;\n' + declarations(themed, light)
    dark_body = 'color-scheme: dark;\n' + declarations(themed, dark)
    rules_text = [
        block([':root', f"[data-theme='{light}']"], light_body),
        '@media (prefers-color-scheme: dark) {\n'
        + indent(block([f":root:not([data-theme='{light}'])"], dark_body))
        + '}\n',
        block([f"[data-theme='{dark}']"], dark_body),
        '@media print {\n'
        + indent(
            block(
                [':root:not([data-theme])', ':root[data-theme]'],
                light_body,
            )
            + '\n'
            + block(['[data-theme]'], light_body)
        )
        + '}\n',
        block([':root'], declarations(plain, light)),
    ]
    return (
        f'@layer {PREFIX}.tokens {{\n' + indent('\n'.join(rules_text)) + '}\n'
    )


def css_header(title: str) -> str:
    """Returns the comment at the top of a generated stylesheet."""
    return (
        f'/* Lrssn design system: {title}.\n'
        ' * Colours from the Lrssn colour themes, Lrssn Shore (light) and\n'
        ' * Lrssn Hearth (dark), and the rest from tokens/tokens.toml.\n'
        f' * {GENERATED}\n'
        ' */\n\n'
    )


def stylesheet(tokens: list[Token], components: list[Component]) -> str:
    """Returns the whole design system as one stylesheet."""
    parts = [
        css_header('tokens, base styles and components'),
        f'@layer {PREFIX}.tokens, {PREFIX}.base, {PREFIX}.components;\n\n',
        tokens_css(tokens),
        f'\n@layer {PREFIX}.base {{\n',
        indent((SOURCE / 'base.css').read_text()),
        '}\n',
        f'\n@layer {PREFIX}.components {{\n',
    ]
    for index, component in enumerate(components):
        if index:
            parts.append('\n')
        parts.append(indent(component_css(component)))
    parts.append('}\n')
    return ''.join(parts)


def component_css(component: Component) -> str:
    """Returns a component's CSS under a heading comment."""
    rule = '-' * max(0, 72 - len(component.title))
    return f'/* --- {component.title} {rule} */\n\n' + component.css


def scss(tokens: list[Token]) -> str:
    """Returns the tokens as Sass variables."""
    lines = [
        '// Lrssn design system: the tokens as Sass variables.',
        f'// {GENERATED}',
        '//',
        '// Each variable points at a custom property, so load dist/tokens.css',
        '// or dist/lrssn.css as well. The breakpoints are plain values,',
        '// because media queries cannot read custom properties.',
        '',
    ]
    family = ''
    for token in tokens:
        title = token.group if token.family == 'colour' else token.family
        if title != family:
            if family:
                lines.append('')
            heading = FAMILIES.get(title, f'Colour: {title}')
            lines.append(f'// {heading}')
            family = title
        lines.append(f'${PREFIX}-{token.name}: var(--{PREFIX}-{token.name});')
    lines += ['', '// Breakpoints, for media queries']
    for token in tokens:
        if token.name.startswith('breakpoint-'):
            lines.append(f'${PREFIX}-{token.name}-value: {token.value};')
    return '\n'.join(lines) + '\n'


def tokens_json(tokens: list[Token], themes: list[Theme]) -> str:
    """Returns the tokens as JSON, as lists of name, value and usage."""
    data: dict[str, Any] = {
        'name': 'Lrssn',
        'about': f'The tokens of the Lrssn design system. {GENERATED}',
        'themes': [{'id': theme.id, 'name': theme.name} for theme in themes],
    }
    for token in tokens:
        family = data.setdefault(token.family, {'tokens': []})
        item: dict[str, Any] = {'name': token.name}
        if token.family == 'colour':
            item['group'] = token.group
        item['value'] = token.values if token.themed else token.value
        item['usage'] = token.usage
        family['tokens'].append(item)
    return json.dumps(data, indent=2, ensure_ascii=False) + '\n'


def logo_file(colour_value: str) -> str:
    """Returns the logo mark as an SVG file, stroked in one colour."""
    stroke = (
        f'fill="none" stroke="{colour_value}" stroke-width="64" '
        'stroke-linecap="round" stroke-linejoin="round"'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{LOGO_VIEWBOX}">'
        f'<rect {LOGO_RECT} {stroke}/><path d="{LOGO_PATH}" {stroke}/></svg>\n'
    )


def inline_mark(labelled: bool) -> str:
    """Returns the logo mark to put inside HTML, drawn by logo.css.

    Beside the name, the mark is hidden from screen readers, which read the
    name. On its own, it is an image named "Lrssn logo".
    """
    label = 'role="img" aria-label="Lrssn logo"'
    hidden = 'aria-hidden="true" focusable="false"'
    return (
        f'<svg class="{PREFIX}-logo__mark" viewBox="{LOGO_VIEWBOX}" '
        f'{label if labelled else hidden}>'
        f'<rect {LOGO_RECT}/><path d="{LOGO_PATH}"/></svg>'
    )


def expand(html: str, name: str) -> str:
    """Replaces the placeholders of an example or a template."""
    values = {'mark': inline_mark(False), 'mark-labelled': inline_mark(True)}

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise SystemExit(f'{name}: unknown placeholder {key!r}')
        return values[key]

    return PLACEHOLDER.sub(replace, html)


def scope_ids(html: str, suffix: str) -> str:
    """Adds a suffix to every id of an example, so two copies can coexist."""

    def attribute(match: re.Match[str]) -> str:
        name, value = match.groups()
        ids = ' '.join(f'{part}-{suffix}' for part in value.split())
        return f'{name}="{ids}"'

    html = ID_ATTRIBUTE.sub(attribute, html)
    return ID_LINK.sub(lambda m: f'href="#{m.group(1)}-{suffix}"', html)


def preview(components: list[Component], themes: list[Theme]) -> str:
    """Returns the preview page: every component, in both themes."""
    template = (TEMPLATES / 'preview.html').read_text()
    nav = []
    sections = []
    for component in components:
        example = expand(component.example, f'{component.name}/example.html')
        panes = []
        for theme in themes:
            panes.append(
                f'<div class="pane" data-theme="{theme.id}">\n'
                f'  <p class="pane-label">{theme.name}</p>\n'
                f'  <div class="pane-body">\n'
                + scope_ids(example, theme.id)
                + '  </div>\n</div>\n'
            )
        nav.append(
            f'<li><a href="#{component.name}">{component.title}</a></li>'
        )
        sections.append(
            f'<section class="component" id="{component.name}" '
            f'aria-labelledby="{component.name}-title">\n'
            '  <header class="component-head">\n'
            f'    <h2 id="{component.name}-title">{component.title}</h2>\n'
            f'    <p>{markdown_inline(component.summary)}</p>\n'
            f'    <a href="../components/{component.name}/README.md">'
            'Guidelines</a>\n'
            '  </header>\n'
            '  <div class="panes'
            + (' panes--wide' if component.name in WIDE else '')
            + '">\n'
            + ''.join(panes)
            + '  </div>\n</section>\n'
        )
    return (
        template.replace('{{ nav }}', indent('\n'.join(nav)) + '\n')
        .replace('{{ sections }}', '\n'.join(sections))
        .replace('{{ generated }}', GENERATED)
        .replace('{{ theme-init }}', (SCRIPTS / 'theme-init.js').read_text())
        .replace('{{ scripts }}', classic_scripts())
    )


def classic_scripts() -> str:
    """Returns the modules of js/ as one classic script, for the preview.

    Browsers do not load modules from a file opened from the disk, so the
    preview carries the modules inline, without their imports and exports,
    and runs what js/index.js runs.
    """
    parts = []
    for name in SCRIPT_MODULES:
        text = (SCRIPTS / name).read_text()
        parts.append(re.sub(r'^export ', '', text, flags=re.MULTILINE))
    calls = re.findall(
        r'^(init\w+\(\);)$', (SCRIPTS / 'index.js').read_text(), re.MULTILINE
    )
    script = '(() => {\n' + '\n'.join(parts) + '\n' + '\n'.join(calls)
    if '</script' in script:
        raise SystemExit('js/: a script holds </script, which ends the tag')
    return script + '\n})();'


def markdown_inline(text: str) -> str:
    """Turns the inline code of a Markdown line into HTML."""
    text = text.replace('&', '&amp;').replace('<', '&lt;')
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)


def table(header: list[str], rows: Iterable[list[str]]) -> str:
    """Returns a Markdown table."""
    lines = ['| ' + ' | '.join(header) + ' |']
    lines.append('| ' + ' | '.join('---' for _ in header) + ' |')
    lines += ['| ' + ' | '.join(row) + ' |' for row in rows]
    return '\n'.join(lines) + '\n'


def guide_tables(
    tokens: list[Token], themes: list[Theme], components: list[Component]
) -> dict[str, str]:
    """Returns the generated tables of Design.md, by marker."""
    names = [theme.name.removeprefix('Lrssn ') for theme in themes]
    by_name = {token.name: token for token in tokens}
    tables = {}

    colour_parts = []
    for group in COLOUR_GROUPS:
        rows = [
            [
                f'`{token.name}`',
                *(f'`{token.values[theme.id]}`' for theme in themes),
                token.usage,
            ]
            for token in tokens
            if token.family == 'colour' and token.group == group
        ]
        colour_parts.append(
            f'#### {group}\n\n' + table(['Token', *names, 'Use'], rows)
        )
    tables['colours'] = '\n'.join(colour_parts)

    values = {
        theme.id: {t.name: t.values[theme.id] for t in tokens if t.themed}
        for theme in themes
    }

    def ratio(foreground: str, background: str, theme_id: str) -> str:
        return format(
            contrast_ratio(
                colour(foreground, values[theme_id]),
                colour(background, values[theme_id]),
            ),
            '.2f',
        )

    tables['contrast-text'] = table(
        [
            'Token',
            *(f'{name} {place}' for name in names for place in SURFACES),
        ],
        (
            [
                f'`{token}`',
                *(
                    ratio(token, place, theme.id)
                    for theme in themes
                    for place in SURFACES
                ),
            ]
            for token in TEXT_TOKENS
        ),
    )
    tables['contrast-pairs'] = table(
        ['Text or graphic', 'On', *names, 'Needs'],
        (
            [
                f'`{foreground}`',
                f'`{background}`',
                *(ratio(foreground, background, t.id) for t in themes),
                str(minimum),
            ]
            for foregrounds, backgrounds, minimum in PAIRS
            for foreground in foregrounds
            for background in backgrounds
        ),
    )

    for family in FAMILIES:
        family_tokens = [t for t in tokens if t.family == family]
        if family == 'shadow':
            tables[family] = table(
                ['Token', *names, 'Use'],
                (
                    [
                        f'`{t.name}`',
                        *(f'`{t.values[theme.id]}`' for theme in themes),
                        t.usage,
                    ]
                    for t in family_tokens
                ),
            )
        else:
            tables[family] = table(
                ['Token', 'Value', 'Use'],
                (
                    [f'`{t.name}`', f'`{t.value}`', t.usage]
                    for t in family_tokens
                ),
            )

    def style_value(value: str) -> str:
        token = by_name.get(value)
        return f'`{token.name}`' if token else f'`{value}`'

    styles = load_config()['type-style']
    tables['type-styles'] = table(
        ['Style', 'Typeface', 'Size', 'Line height', 'Weight', 'Use'],
        (
            [
                f'`{style["name"]}`',
                f'`{style["family"]}`'
                + (' italic' if style.get('style') == 'italic' else ''),
                style_value(style['size']),
                style_value(style['line-height']),
                str(style['weight']),
                style['usage'],
            ]
            for style in styles
        ),
    )

    component_parts = []
    for group in COMPONENT_GROUPS:
        rows = [
            [
                f'[{c.title}](./components/{c.name}/README.md)',
                f'`.{PREFIX}-{c.name}`',
                c.summary,
            ]
            for c in components
            if c.group == group
        ]
        component_parts.append(
            f'### {group}\n\n'
            + table(['Component', 'Class', 'What it is for'], rows)
        )
    tables['components'] = '\n'.join(component_parts)
    return tables


def fill_guide(text: str, tables: dict[str, str]) -> str:
    """Replaces the text between each pair of markers with its table."""

    def replace(match: re.Match[str]) -> str:
        start, name, end = match.groups()
        if name not in tables:
            raise SystemExit(f'{GUIDE.name}: unknown marker {name!r}')
        return start + tables[name] + end

    return MARKERS.sub(replace, text)


def load_config() -> dict[str, Any]:
    """Reads tokens/tokens.toml."""
    return tomllib.loads(TOKENS.read_text())


def outputs(
    tokens: list[Token], themes: list[Theme], components: list[Component]
) -> dict[str, str]:
    """Returns every generated file, as {path: content}."""
    files = {
        'dist/tokens.css': css_header('tokens') + tokens_css(tokens),
        'dist/_tokens.scss': scss(tokens),
        'dist/tokens.json': tokens_json(tokens, themes),
        'dist/lrssn.css': stylesheet(tokens, components),
        'preview/index.html': preview(components, themes),
    }
    values = {
        theme.id: {t.name: t.values[theme.id] for t in tokens}
        for theme in themes
    }
    for name, (token, theme_id) in LOGO_FILES.items():
        files[f'assets/logo/lrssn-logo-{name}.svg'] = logo_file(
            values[theme_id][token]
        )
    files[GUIDE.name] = fill_guide(
        GUIDE.read_text(), guide_tables(tokens, themes, components)
    )
    return files


def unprefix(text: str) -> str:
    """Names the custom properties as the claude.ai design system does."""
    return text.replace(f'--{PREFIX}-', '--')


def absolute_links(markdown: str, base: str) -> str:
    """Turns the relative links of a Markdown file into GitHub links."""

    def replace(match: re.Match[str]) -> str:
        path = (pathlib.PurePosixPath(base) / match.group(1)).as_posix()
        parts: list[str] = []
        for part in path.split('/'):
            if part == '..' and parts:
                parts.pop()
            elif part not in ('', '.'):
                parts.append(part)
        return f']({REPOSITORY}{"/".join(parts)})'

    return MARKDOWN_LINK.sub(replace, markdown)


def artifact_size(value: str) -> str:
    """Returns a length the claude.ai design system reads: clamp's maximum."""
    if value.startswith('clamp('):
        return value.removeprefix('clamp(').removesuffix(')').split(', ')[-1]
    return value


def artifact_tokens(tokens: list[Token], themes: list[Theme]) -> str:
    """Returns tokens.json in the shape of the claude.ai design system."""
    by_name = {token.name: token for token in tokens}
    config = load_config()
    groups: dict[str, dict[str, Any]] = {}
    for style in config['type-style']:
        family = ARTIFACT_FAMILIES[style['family']]
        group = groups.setdefault(
            style['group'],
            {'name': style['group'], 'family': family, 'styles': []},
        )
        size = style['size']
        line_height = style['line-height']
        item: dict[str, Any] = {
            'name': style['name'],
            'family': family,
            'fontSize': artifact_size(
                by_name[size].value if size in by_name else size
            ),
            'lineHeight': (
                by_name[line_height].value
                if line_height in by_name
                else line_height
            ),
            'fontWeight': style['weight'],
        }
        if 'letter-spacing' in style:
            item['letterSpacing'] = style['letter-spacing']
        if 'style' in style:
            item['fontStyle'] = style['style']
        item['sample'] = style['sample']
        item['usage'] = style['usage']
        group['styles'].append(item)
    data: dict[str, Any] = {
        'name': 'Lrssn',
        'version': 2,
        'color': {
            'themes': [{'id': t.id, 'name': t.name} for t in themes],
            'tokens': [
                {'name': t.name, 'value': t.values, 'usage': t.usage}
                for t in tokens
                if t.family == 'colour'
            ],
        },
        'type': {
            'fonts': [
                {
                    'family': family,
                    'file': f'fonts/{file}',
                    'weight': '100 900',
                    'style': style,
                }
                for family, file, style in ARTIFACT_FONTS
            ],
            'families': {
                ARTIFACT_FAMILIES[t.name]: t.value.replace("'", '"')
                for t in tokens
                if t.family == 'font'
            },
            'groups': list(groups.values()),
        },
    }
    for family, key in ARTIFACT_KEYS.items():
        data[key] = {
            'note': FAMILIES[family] + ' of the Lrssn design system.',
            'tokens': [
                {
                    'name': t.name,
                    'value': t.values if t.themed else t.value,
                    'usage': t.usage,
                }
                for t in tokens
                if t.family == family
            ],
        }
    return json.dumps(data, indent=2, ensure_ascii=False) + '\n'


def artifact_preview(component: Component) -> str:
    """Returns a component's preview for the claude.ai design system.

    The preview shows the page with JavaScript, so it reveals the controls
    that a script reveals on the page.
    """
    example = expand(component.example, f'{component.name}/example.html')
    return unprefix(
        f'<!-- @dsCard group="{component.group}" height=160 -->\n'
        '<!doctype html>\n'
        '<html lang="en-GB">\n'
        '<head>\n'
        '<meta charset="utf-8">\n'
        f'<title>{component.title}</title>\n'
        '<style>\n'
        'body { margin: 0; padding: 24px; background: '
        f'var(--{PREFIX}-background); color: var(--{PREFIX}-text-color); '
        f'font-family: var(--{PREFIX}-font-ui); }}\n'
        '.demo-row { display: flex; flex-wrap: wrap; align-items: center; '
        'gap: 1rem 1.5rem; }\n'
        '.demo-stack { display: grid; gap: 1rem; }\n'
        '</style>\n'
        '</head>\n'
        '<body>\n' + example + '<script>\n'
        'for (const element of document.querySelectorAll("[hidden]")) {\n'
        '  element.hidden = false;\n'
        '}\n'
        '</script>\n'
        '</body>\n'
        '</html>\n'
    )


def artifact_files(
    tokens: list[Token], themes: list[Theme], components: list[Component]
) -> dict[str, str]:
    """Returns the files of the claude.ai design system, under project/."""
    guide = fill_guide(
        GUIDE.read_text(), guide_tables(tokens, themes, components)
    )
    guide = re.sub(r'\n## Table of contents\n\n\[TOC\]\n', '', guide)
    files = {
        'project/tokens.json': artifact_tokens(tokens, themes),
        'project/README.md': absolute_links(guide, '.'),
        'project/components/bundle.css': unprefix(
            (SOURCE / 'base.css').read_text()
            + '\n'
            + '\n'.join(component_css(c) for c in components)
        ),
        'project/components/Cover/preview.html': unprefix(
            expand((TEMPLATES / 'cover.html').read_text(), 'cover.html')
        ),
        'project/assets/Logos/README.md': (
            '# Logos\n\n'
            'The Lrssn mark on a transparent ground, as the brand guide '
            'names the files.\n'
            'Each is drawn in one colour: `lrssn-logo-orange.svg` in '
            '`primary-color` for light or dark grounds, '
            "`lrssn-logo-dark.svg` in Shore's `text-color` for light "
            "grounds, and `lrssn-logo-light.svg` in Hearth's `text-color` "
            'for dark grounds.\n'
            "Keep a quarter of the mark's height clear on every side, and "
            'never stretch, rotate or recolour it.\n'
        ),
    }
    for component in components:
        folder = f'project/components/{component.pascal}'
        files[f'{folder}/README.md'] = absolute_links(
            component.readme, f'components/{component.name}'
        )
        files[f'{folder}/preview.html'] = artifact_preview(component)
    return files


def compare(files: dict[str, str], write: bool) -> list[str]:
    """Writes the files that changed, or prints their diff; returns them."""
    stale = []
    for path, text in files.items():
        target = ROOT / path
        current = target.read_text() if target.exists() else ''
        if current == text:
            continue
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
            print(f'Wrote {path}')
        else:
            stale.append(path)
            sys.stdout.writelines(
                difflib.unified_diff(
                    current.splitlines(keepends=True),
                    text.splitlines(keepends=True),
                    f'a/{path}',
                    f'b/{path}',
                )
            )
    return stale


def main() -> None:
    """Checks or writes the generated files, and exits with 1 on an error."""
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] if __doc__ else None
    )
    parser.add_argument(
        '--write', action='store_true', help='regenerate the files'
    )
    parser.add_argument(
        '--palettes',
        type=pathlib.Path,
        help='read the palettes from this directory instead of fetching them',
    )
    parser.add_argument(
        '--artifact',
        type=pathlib.Path,
        help='write the files of the claude.ai design system here',
    )
    args = parser.parse_args()

    themes = [load_theme(i, palette, args.palettes) for i, palette in THEMES]
    if themes[0].website != themes[1].website:
        raise SystemExit('The palettes have different website tokens')
    tokens = load_tokens(themes, load_config())
    components = load_components()
    errors = check_contrast(tokens) + check_references(tokens)
    files = outputs(tokens, themes, components)
    stale = compare(files, args.write)
    if args.artifact:
        for path, text in artifact_files(tokens, themes, components).items():
            target = args.artifact / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        for name, (token, theme_id) in LOGO_FILES.items():
            value = next(t for t in tokens if t.name == token).values[theme_id]
            target = args.artifact / 'logos' / f'lrssn-logo-{name}.svg'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(logo_file(value))
        print(f'Wrote the claude.ai design system to {args.artifact}')
    for error in errors:
        print(error)
    if stale:
        print('Out of date: ' + ', '.join(stale))
        print('Run scripts/build.py --write to regenerate them.')
    if errors or stale:
        sys.exit(1)
    print(f'{len(files)} files are up to date, and every contrast rule holds.')


if __name__ == '__main__':
    main()
