class TEMPLATES:
    root = '$levelname $message @ $lineno in $module'
    debug = '<YELLOW>$levelname</YELLOW> $message @ $lineno in $module'
    info = '<GREEN>$levelname</GREEN> $message @ $lineno in $module'
    warning = '<MAGENTA>$levelname</MAGENTA> $message @ $lineno in $module'
    error = '<RED>$levelname</RED> $message @ $lineno in $module'
    critical = '<RED>$levelname</RED> $message @ $lineno in $module'
    test = '$module $pathname $funcname $lineno $levelname $message'


class LEVELS:
    debug = TEMPLATES.debug
    info = TEMPLATES.info
    warning = TEMPLATES.warning
    error = TEMPLATES.error
    critical = TEMPLATES.critical
    test = TEMPLATES.test
