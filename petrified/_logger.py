# TODO emoji logging!!

import inspect
import time
from typing import List

from . import config
from .color_codes import ANSI_CODES
from .emojis import EMOJIS


class Logger:

    # maintains an list of attributes
    _attr_path = []

    def __getattr__(self, attr):
        if not attr[0] == '_':
            self._attr_path.append(attr)
        return self

    # this is ran on the last attribute
    def __call__(self, msg):
        caller_info = inspect.stack()[1]

        level = self._attr_path[0]

        log_record = {
            'module': caller_info[0].f_globals['__name__'],
            'pathname': caller_info.filename,
            'funcname': caller_info.function,
            'lineno': caller_info.lineno,
            'asctime': time.asctime(),
            'levelname': level.upper(),
            'message': config.tag_convert(msg)
        }

        tail_emojis, overriding_styles = [], []
        # now categorize the options
        for option in self._attr_path[1:]:
            if hasattr(EMOJIS, option):
                tail_emojis.append(option)
            elif option in ANSI_CODES:
                overriding_styles.append(option)

        self._attr_path = []  # reset the attrs

        formatted_msg = self._apply_format(level,
                                           *overriding_styles,
                                           **log_record)

        # TODO implement write to file capability
        print(formatted_msg, ' '.join(
            [getattr(EMOJIS, emoji) for emoji in tail_emojis]))

    def _apply_format(self,
                      level: str,
                      *styles: List,
                      **log_record) -> str:
        t = config.apply_style(level, *styles)
        return t.substitute(log_record)
