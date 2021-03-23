import sys
import inspect
import logging
import logging.config
import yaml
from pathlib import Path
import time
from string import Template

CONFIG_FILE = Path(__file__).parent / 'conf.yaml'
with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def f():
    print(inspect.currentframe().f_globals)
    print()
    print(inspect.stack()[1])


class Logger:

    _attr_path = []

    def get_emitter(self, level):
        levels = {
            'debug': logging.debug
        }
        return levels[level]

    def __getattr__(self, attr):
        self._attr_path.append(attr)
        return self

    def __call__(self, msg):
        caller_info = inspect.stack()[1]

        log_record = {
            'module': caller_info[0].f_globals['__name__'],
            'pathname': caller_info.filename,
            'funcname': caller_info.function,
            'lineno': caller_info.lineno,
            'asctime': time.asctime(),
            'levelname': self._attr_path[0].upper(),
            'message': msg
        }

        formatted_msg = self._apply_format(*self._attr_path, **log_record)

        if self._attr_path[0] == 'debug':
            try:
                self._attr_path[1]
            except IndexError:
                formatted_msg = self._apply_format('debug', **log_record)
                sys.stdout.write(formatted_msg)

    def _apply_format(self, *styles, **log_record):
        #t = self.styles[style]
        return t.substitute(log_record)

    styles = {
        # contains mapping of styles
        # e.g. 'debug': Template(...)
        'debug': Template('$levelname - $message @ $lineno')
    }


if __name__ == '__main__':
    logger = Logger()
    logger.debug('debug message')
