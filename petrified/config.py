import re
from string import Template

from .color_codes import ANSI_CODES, ESCAPE_CODES
from .emojis import EMOJIS
from .templates import LEVELS

OPEN_TAG_RGX = r"\\?<((?:[fb]g\s)?[^<?>/\s]*)>"
TAG_RGX = r"\\?</?((?:[fb]g\s)?[^<>/\s]*)>"


def tag_convert(exp: str) -> str:
    ansied_exp = exp
    loci = {}

    for match in re.finditer(OPEN_TAG_RGX, exp):
        markup, tag = match.group(0), match.group(1)

        closing_tag = f'</{tag}>'
        close_start = exp.find(closing_tag, match.end())

        if close_start == -1:
            continue

        appends = []
        extra_ansi = ''

        for prev_tag in loci:
            if prev_tag > close_start:
                appends.append(loci[prev_tag])

        if appends:
            codes = ';'.join([f'{ANSI_CODES[tag]}' for tag in appends])
            extra_ansi = f'\x1b[{codes}m'

        loci[close_start] = tag

        ansied_exp = ansied_exp.replace(markup, ESCAPE_CODES[tag], 1)
        ansied_exp = ansied_exp.replace(closing_tag,
                                        f'\x1b[0m{extra_ansi}',
                                        1)

    return ansied_exp


def strip_tags(exp: str) -> str:
    return re.sub(TAG_RGX, '', exp)


def is_emoji(opt: str) -> bool:
    return hasattr(EMOJIS, opt)


# if styles are provided, will override default
def apply_style(level: str, *styles) -> Template:
    if styles:
        styled_template = get_styled_template(*styles)
        cleaned_template = strip_tags(getattr(LEVELS, level))
        return Template(styled_template.substitute(
            logtemplate=cleaned_template))
    else:
        return Template(tag_convert(getattr(LEVELS, level)))


def get_styled_template(*styles) -> Template:
    codes = ';'.join([repr(ANSI_CODES[style]) for style in styles])
    wrapped = f'\x1b[{codes}m$logtemplate\x1b[0m\n'
    return Template(wrapped)
