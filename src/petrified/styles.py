from string import Template

# what the heck I can't have a different style for every handler...


root_template = Template('$levelname - $message @ $lineno')


FORMATS = {
    'DEBUG': root_template,
    'INFO': root_template,
    'WARNING': root_template,
    'ERROR': root_template,
    'CRITICAL': root_template,
}

STYLES = {
    'GREEN': ''}
