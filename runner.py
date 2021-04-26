import sys

from petrified import logger


def main():
    logger.test('test message')
    logger.debug('debug message')
    logger.critical('this <red>word</red> should be red')


if __name__ == '__main__':
    sys.exit(main())
