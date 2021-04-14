from typing import Dict


def to_ansi_escape(codes: Dict) -> Dict:
    """Wraps numbers with the escape characters"""
    return {name: f'\x1b[{code}m' for name, code in codes.items()}


ANSI_CODES = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,

    # these are for backgrounds
    'BLACK': 40,
    'RED': 41,
    'GREEN': 42,
    'YELLOW': 43,
    'BLUE': 44,
    'MAGENTA': 45,
    'CYAN': 46,
    'WHITE': 47,

    'bold': 1,
    'underline': 4,
}


ESCAPE_CODES = to_ansi_escape(ANSI_CODES)
