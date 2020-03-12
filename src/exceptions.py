
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


class AmbiguousOverloadError(BuildException):
    pass


class InvalidOperationError(BuildException):
    pass


class UnknownTypeError(BuildException):
    pass


class UndefinedVariableError(BuildException):
    pass


class IncompatibleTypesError(BuildException):
    pass


class TooManyAlternativesError(BuildException):
    pass


class InvalidUnionTypeError(BuildException):
    pass


class DuplicateSymbolException(BuildException):
    pass


class DuplicateParamError(BuildException):
    pass


class MissingParamError(BuildException):
    pass


class ExtraParamError(BuildException):
    pass


class InvokeArgCountError(BuildException):
    pass


class UnusedParamError(BuildException):
    pass
