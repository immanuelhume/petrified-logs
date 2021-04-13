import os
import sys
from string import Template
from typing import List

# `root` is the default format
root = '$levelname - $message @ line $lineno of $module'


# levels are specified as tuples of format followed by styles
LEVELS = {
    'debug': {
        'template': root,
        'styles': ['cyan']
    },
    'info': {
        'template': root,
        'styles': ['green']
    },
    'warning': {
        'template': root,
        'styles': ['yellow', 'underline']
    },
    'error': {
        'template': root,
        'styles': ['red']
    },
    'critical': {
        'template': root,
        'styles': ['red', 'bold']
    }
}

# ANSI escape codes for styles are specified here
STYLES = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,

    'bold': 1,
    'underline': 4,
}


def apply_style(level: str, *styles: List) -> str:
    if not styles:
        # styles list is empty, get default styles
        default_styles = LEVELS[level]['styles']
        style_template = get_styled_template(*default_styles)
    else:
        style_template = get_styled_template(*styles)

    return Template(style_template.substitute(logtemplate=LEVELS[level]['template']))


def get_styled_template(*styles):
    codes = ';'.join([repr(STYLES[style]) for style in styles])
    wrapped = f'\x1b[{codes}m$logtemplate\x1b[0m\n'
    return Template(wrapped)


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty
