import inspect
import sys
import time
from typing import List

from . import config


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
            'message': msg
        }

        styles = self._attr_path[1:]
        self._attr_path = []

        formatted_msg = self._apply_format(level, *styles, **log_record)

        # TODO implement write to file capability
        print(formatted_msg)

    def _apply_format(self,
                      level: str,
                      *styles: List,
                      **log_record) -> str:
        t = config.apply_style(level, *styles)
        return t.substitute(log_record)
