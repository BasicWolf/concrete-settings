import warnings

from typing import Callable

from .exceptions import SettingsValidationError


class Validator:
    def __call__(self, value):  # pragma: no cover
        pass

    def set_context(self, settings, setting, name):
        pass  # pragma: no cover


class DeprecatedValidator(Validator):
    __slots__ = ('msg', '_msg_template', 'validate_as_error')

    def __init__(self, msg, validate_as_error):
        self._msg_template = msg
        self.validate_as_error = validate_as_error

    def __call__(self, _):
        warnings.warn(self.msg, DeprecationWarning)

        if self.validate_as_error:
            raise SettingsValidationError(self.msg)


    def set_context(self, settings, setting, name):
        self.msg = self._msg_template.format(cls=type(settings), name=name)


class ValueTypeValidator(Validator):
    __slots__ = ('type_hint', 'strict')

    def __init__(self, type_hint=None, strict: bool = True):
        """
        :param strict: Indicates whether a strict type equivalence is required:
                       When True: type(value) == type_hint
                       When False: isinstance(value, type_hint)
        """
        self.type_hint = type_hint
        self.strict = strict

    def __call__(self, value):
        valid = True
        if self.strict:
            valid = type(value) == self.type_hint
        else:
            valid = isinstance(value, self.type_hint)

        if not valid:
            raise SettingsValidationError(f'Expected value of type `{self.type_hint}` got value of type `{type(value)}`')


    def set_context(self, settings, setting, _):
        if self.type_hint is None:
            self.type_hint = setting.type_hint