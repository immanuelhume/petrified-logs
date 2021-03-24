from string import Template
import sys
import os

root = '$levelname - $message @ line $lineno of $module'

LEVELS = {
    'debug': (root, 'cyan'),
    'info': (root, 'green'),
    'warning': (root, 'yellow', 'underline'),
    'error': (root, 'red'),
    'critical': (root, 'red', 'bold')
}

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


def apply_style(level, *styles):

    if not styles:
        default_styles = get_default(level)
        style_template = get_style_template(*default_styles)
    else:
        style_template = get_style_template(*styles)

    return Template(style_template.substitute(logtemplate=LEVELS[level][0]))


def get_default(level):
    return LEVELS[level][1:]


def get_style_template(*styles):
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


if __name__ == '__main__':
    print(supports_color())
