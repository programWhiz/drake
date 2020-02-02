
class BuildException(Exception):
    pass


class MissingAttribute(BuildException):
    pass


class UndeclaredIdentifier(BuildException):
    pass


class SymbolNotFound(BuildException):
    pass


class ParseException(BuildException):
    pass
