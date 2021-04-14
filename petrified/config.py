import re
from string import Template

from .color_codes import ANSI_CODES, ESCAPE_CODES
from .templates import LEVELS


def tag_convert(exp: str) -> str:
    ansied_exp = exp
    loci = {}
    tag_rgx = re.compile(r"\\?<((?:[fb]g\s)?[^<>/\s]*)>")

    for match in tag_rgx.finditer(exp):
        markup, tag = match.group(0), match.group(1)
        closing_tag = f'</{tag}>'
        close_start = exp.find(closing_tag, match.end())

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


# these are overriding styles
# if no overriding styles are provided, use default template
# ANSI codes are applied here
def apply_style(level: str, *styles) -> str:
    if styles:
        styled_template = get_styled_template(*styles)
        return Template(styled_template.substitute(
            logtemplate=(getattr(LEVELS, level))))
    else:
        return Template(tag_convert(getattr(LEVELS, level)))


def get_styled_template(*styles):
    codes = ';'.join([repr(ANSI_CODES[style]) for style in styles])
    wrapped = f'\x1b[{codes}m$logtemplate\x1b[0m\n'
    return Template(wrapped)
