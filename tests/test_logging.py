import sys
import pytest
sys.path.append('/mnt/d/projects/petrified/src')

from petrified._logger import Logger


@pytest.fixture
def logger():
    logger = Logger()
    return logger


def test_simple_debug(logger):
    logger.debug("debug doge")


if __name__ == '__main__':
    pass
