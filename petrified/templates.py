class TEMPLATES:
    root = '<GREEN><white>$levelname</white></GREEN> $message @ $lineno in $module'
    test = '$module $pathname $funcname $lineno $levelname $message'


class LEVELS:
    test = TEMPLATES.test
    debug = TEMPLATES.root
    info = TEMPLATES.root
    warning = TEMPLATES.root
    error = TEMPLATES.root
    critical = TEMPLATES.root
