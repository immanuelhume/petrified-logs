from petrified import logger

if __name__ == '__main__':
    logger.debug('debug message')
    logger.error.blue.underline('blue underlined error message')
    logger.error.blue.underline.bold('blue bold underlined error message')
