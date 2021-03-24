import sys
import inspect
import logging
import logging.config
import yaml
from pathlib import Path
import time
from string import Template
import config


def f():
    print(inspect.currentframe().f_globals)
    print()
    print(inspect.stack()[1])


class Logger:

    _attr_path = []

    def __getattr__(self, attr):
        self._attr_path.append(attr)
        return self

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

        sys.stdout.write(formatted_msg)

    def _apply_format(self, level, *styles, **log_record):
        t = config.apply_style(level, *styles)
        return t.substitute(log_record)


if __name__ == '__main__':
    logger = Logger()
    print('        ***normal logs***')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    print('        ***custom color logs***')
    logger.debug.bold.red('bold red debug message')
    logger.critical.cyan('cyan critical message')
    print('        ***custom font and color***')
    logger.debug.yellow.bold('bold yellow debug message')
    logger.error.underline.magenta('underlined magenta error message')
