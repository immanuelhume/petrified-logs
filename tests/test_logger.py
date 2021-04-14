import sys

sys.path.append('/home/junyi/Projects/petrified')

import pytest
from petrified import config, logger


@pytest.fixture
def tagged_exp():
    return '<BLACK>hello <green>cruel</green> world</BLACK>'


def test_log_record(capsys):
    logger.test('test message')
    out, err = capsys.readouterr()
    assert out == 'test_logger /home/junyi/Projects/petrified/tests/test_logger.py test_log_record 15 TEST test message\n'


def test_logging(capsys):
    logger.debug('debug message')
    out, err = capsys.readouterr()
    assert out == '\x1b[42m\x1b[37mDEBUG\x1b[0m\x1b[42m\x1b[0m debug message @ 21 in test_logger\n'


def test_tag_conversion(tagged_exp):
    ansied_exp = '\x1b[40mhello \x1b[32mcruel\x1b[0m\x1b[40m world\x1b[0m'
    assert config.tag_convert(tagged_exp) == ansied_exp
