#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the `aiovalidator` package.
# (c) 2016-2017 Kozlovski Lab <welcome@kozlovskilab.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
"""
:Authors:
    - `Vladimir Kozlovski <vladimir@kozlovskilab.com>`_
"""
from collections import Mapping, Sequence
from asyncio import iscoroutinefunction
import re

__all__ = ['Validator', 'ValidationError']


class ValidationError(ValueError):
    """
    Parameters
    ----------
    ...
    """
    def __init__(self, msg: str, issues=None):
        self.msg = msg
        self.issues = issues
        super().__init__(msg)

    # def __str__(self):
    #     return self._msg

    # def __iter__(self):
    #     return iter(self._msg.items())


class Validator:
    """
    """
    ERROR_BAD_TYPE = "must be of '{0}' type"
    ERROR_NOT_NULLABLE = "null value not allowed"
    ERROR_UNKNOWN_FIELD = "unknown field"
    ERROR_REQUIRED_FIELD = "required field"

    ERROR_DICT_SCHEMA = "dict contains some errors"
    ERROR_LIST_SCHEMA = "list contains some errors"

    ERROR_STR_MIN_LENGTH = "minimum length of the string is '{0}' characters"
    ERROR_STR_MAX_LENGTH = "maximum length of the string is '{0}' characters"
    ERROR_STR_REGEX = "value does not match regex '{0}'"

    ERROR_MIN_LENGTH = "min length is '{0}'"
    ERROR_MAX_LENGTH = "max length is '{0}'"
    ERROR_EMPTY_NOT_ALLOWED = "empty values not allowed"
    ERROR_UNALLOWED_VALUE = "unallowed value '{0}'"

    ERROR_MIN_VALUE = "min value is '{0}'"
    ERROR_MAX_VALUE = "max value is '{0}'"

    ERROR_UNALLOWED_VALUES = "unallowed values {0}"

    def __init__(self):
        pass


    async def validate(self, value, *, type: str, required: bool = True, strict_mode: bool = True, **kwargs):
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        type : str
            ...
        required : bool, optional
            ...
        strict_mode : bool, optional
            Enables strict type checking.
        kwargs : dict
            ...

        Returns
        -------

        """
        validate_func = getattr(self, 'validate_{type}'.format(type=type))
        if iscoroutinefunction(validate_func):
            value = await validate_func(value, **kwargs, strict_mode=strict_mode)
        else:
            value = validate_func(value, **kwargs, strict_mode=strict_mode)

        return value


    async def validate_dict(self, value, *, schema: dict = None, default: dict = None, nullable: bool = False,
                            allow_unknown: bool = False, strict_mode: bool = True):
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        schema : dict or None, optional
            ...
        default : dict or None, optional
            ...
        nullable : bool, optional
            ...
        schema : dict
            ...
        allow_unknown : bool, optional
            ...
        strict_mode : bool, optional
            Enables strict type checking.

        Returns
        -------
        dict
        """
        issues = {}

        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, Mapping):
            raise ValidationError(self.ERROR_BAD_TYPE.format('dict'))

        # schema
        if schema is not None:
            for key, validator_params in schema.items():
                try:
                    _value = value[key]
                except KeyError:
                    is_required = validator_params['required'] if 'required' in validator_params else True
                    if is_required is True:
                        issues[key] = self.ERROR_REQUIRED_FIELD
                    else:
                        # Returns default values
                        if 'default' in validator_params:
                            value[key] = validator_params['default']
                else:
                    try:
                        value[key] = await self.validate(_value, **validator_params, strict_mode=strict_mode)
                    except ValidationError as e:
                        issues[key] = e.msg if e.issues is None else e.issues

            # allow_unknown
            if allow_unknown is False:
                for key, _value in value.items():
                    if key not in schema.keys():
                        issues[key] = self.ERROR_UNKNOWN_FIELD
                        # del value[key]

        if len(issues.keys()):
            raise ValidationError(self.ERROR_DICT_SCHEMA, issues=issues)

        return value


    async def validate_list(self, value, *, schema: dict = None, default: str = None, nullable: bool = False,
                            minlength: int = None, maxlength: int = None, allowed: list = None,
                            strict_mode: bool = True):
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        schema : dict or None, optional
            ...
        default : str or None, optional
            ...
        nullable : bool, optional
            ...
        minlength : int, optional
            ...
        maxlength: int, optional
            ...
        allowed : list, optional
            ...
        strict_mode : bool, optional
            Enables strict type checking.

        Returns
        -------

        """
        issues = {}

        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, Sequence) or isinstance(value, str):
            raise ValidationError(self.ERROR_BAD_TYPE.format("list"))

        # minlength
        if minlength is not None:
            if len(value) < minlength:
                raise ValidationError(self.ERROR_MIN_LENGTH.format(minlength))

        # maxlength
        if maxlength is not None:
            if len(value) > maxlength:
                raise ValidationError(self.ERROR_MAX_LENGTH.format(maxlength))

        # allowed
        if allowed is not None:
            disallowed = set(value) - set(allowed)
            if disallowed:
                raise ValidationError(self.ERROR_UNALLOWED_VALUES.format(list(disallowed)))

        # schema
        if schema is not None:
            for i in range(0, len(value)):
                try:
                    value[i] = await self.validate(value[i], **schema, strict_mode=strict_mode)
                except ValidationError as e:
                    issues[i] = e.msg if e.issues is None else e.issues

        if len(issues.keys()):
            raise ValidationError(self.ERROR_LIST_SCHEMA, issues=issues)

        return value


    def validate_string(self, value, *, default: str = None, nullable: bool = False, minlength: int = None,
                        maxlength: int = None, empty: bool = False, allowed: list = None, regex: str = None,
                        strict_mode: bool = True) -> str:
        """
        `validate_string` validates a string.

        If value type is `int` or `float` then tries convert to string, otherwise raise an ValidatonError.

        Parameters
        ----------
        value : any
            Value, to be validated.
        default : str or None, optional
            ...
        nullable : bool, optional
            ...
        minlength : int or None, optional
            ...
        maxlength : int or None, optional
            ...
        empty : bool, optional
            ...
        allowed : list,  optional
            ...
        regex : str or None, optional
            ...
        strict_mode : bool, optional
            Enables strict type checking.

        Returns
        -------
        str
        """
        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, str):
            if strict_mode is True:
                raise ValidationError(self.ERROR_BAD_TYPE.format('string'))

            if isinstance(value, (int, float)) and not isinstance(value, bool):
                # Tries to convert value
                value = str(value)  # TODO: logging warning?
            else:
                raise ValidationError(self.ERROR_BAD_TYPE.format('string'))

        # minlength
        if minlength is not None:
            if len(value) < minlength:
                raise ValidationError(self.ERROR_STR_MIN_LENGTH.format(minlength))

        # maxlength
        if maxlength is not None:
            if len(value) > maxlength:
                raise ValidationError(self.ERROR_STR_MAX_LENGTH.format(maxlength))

        # empty
        if not empty and len(value) == 0:
            raise ValidationError(self.ERROR_EMPTY_NOT_ALLOWED)

        # allowed
        if allowed is not None:
            if value not in allowed:
                raise ValidationError(self.ERROR_UNALLOWED_VALUE.format(value))

        # regex
        if regex is not None:
            pattern = re.compile(regex)
            if not pattern.match(value):
                raise ValidationError(self.ERROR_STR_REGEX.format(regex))

        return value


    def validate_integer(self, value, *, default: int = None, nullable: bool = False, min: int = None, max: int = None,
                         allowed: list = None, strict_mode: bool = True) -> int:
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        default : int or None, optional
            ...
        nullable : bool, optional
            ...
        min : int or None, optional
            ...
        max : int or None, optional
            ...
        allowed : list or None, optional
            ...
        strict_mode : bool, optional
            ...

        Returns
        -------
        int
        """
        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, int):
            if strict_mode:
                raise ValidationError(self.ERROR_BAD_TYPE.format("integer"))

            # try to convert
            try:
                int_value = int(value)  # TODO: logging warning?
            except ValueError as e:
                raise ValidationError(self.ERROR_BAD_TYPE.format("integer"))
            except TypeError as e:
                raise ValidationError(self.ERROR_BAD_TYPE.format("integer"))

            if isinstance(value, float):
                if int_value != value:
                    raise ValidationError(self.ERROR_BAD_TYPE.format("integer"))

            value = int_value

        if isinstance(value, bool):
            if strict_mode:
                raise ValidationError(self.ERROR_BAD_TYPE.format("integer"))

            value = int(value)

        # min
        if min is not None:
            if value < min:
                raise ValidationError(self.ERROR_MIN_VALUE.format(min))

        # max
        if max is not None:
            if value > max:
                raise ValidationError(self.ERROR_MAX_VALUE.format(max))

        # allowed
        if allowed is not None:
            if value not in allowed:
                raise ValidationError(self.ERROR_UNALLOWED_VALUE.format(value))

        return value


    def validate_float(self, value, *, default: float = None, nullable: bool = False, min: float = None,
                       max: float = None, allowed: list = None, strict_mode: bool = True) -> float:
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        default : float or None, optional
            ...
        nullable : bool, optional
            ...
        min : float or None, optional
            ...
        max : float or None, optional
            ...
        allowed : list or None, optional
            ...
        strict_mode : bool, optional
            ...

        Returns
        -------
        float
        """
        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, float):
            if strict_mode:
                if not isinstance(value, int) or isinstance(value, bool):
                    raise ValidationError(self.ERROR_BAD_TYPE.format("float"))

            # try to convert
            if not isinstance(value, (int, str)):
                raise ValidationError(self.ERROR_BAD_TYPE.format("float"))

            try:
                value = float(value)
            except ValueError as e:
                raise ValidationError(self.ERROR_BAD_TYPE.format("float"))

        # min
        if min is not None:
            if value < min:
                raise ValidationError(self.ERROR_MIN_VALUE.format(min))

        # max
        if max is not None:
            if value > max:
                raise ValidationError(self.ERROR_MAX_VALUE.format(max))

        # allowed
        if allowed is not None:
            if value not in allowed:
                raise ValidationError(self.ERROR_UNALLOWED_VALUE.format(value))

        return value


    def validate_number(self, value, *, default: float = None, nullable: bool = False, min: float = None,
                        max: float = None, allowed: list = None, strict_mode: bool = True) -> float:
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        default : float, int or None, optional
            ...
        nullable : bool, optional
            ...
        min : float, int or None, optional
            ...
        max : float, int or None, optional
            ...
        allowed : list or None, optional
            ...
        strict_mode : bool, optional
            ...

        Returns
        -------
        float
        """
        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, (float, int)):
            if strict_mode:
                raise ValidationError(self.ERROR_BAD_TYPE.format("int or float"))

            # try to convert
            if not isinstance(value, str):
                raise ValidationError(self.ERROR_BAD_TYPE.format("int or float"))

            try:
                value = float(value)
            except ValueError as e:
                raise ValidationError(self.ERROR_BAD_TYPE.format("int or float"))

        if isinstance(value, bool) and strict_mode:
            raise ValidationError(self.ERROR_BAD_TYPE.format("int or float"))

        # min
        if min is not None:
            if value < min:
                raise ValidationError(self.ERROR_MIN_VALUE.format(min))

        # max
        if max is not None:
            if value > max:
                raise ValidationError(self.ERROR_MAX_VALUE.format(max))

        # allowed
        if allowed is not None:
            if value not in allowed:
                raise ValidationError(self.ERROR_UNALLOWED_VALUE.format(value))

        return value


    def validate_boolean(self, value, *, default: float = None, nullable: bool = False, allowed: list = None,
                         strict_mode: bool = True) -> bool:
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        default : int or None, optional
            ...
        nullable : bool, optional
            ...
        min : int or None, optional
            ...
        max : int or None, optional
            ...
        allowed : list or None, optional
            ...
        strict_mode : bool, optional
            ...

        Returns
        -------
        bool
        """
        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, bool):
            if strict_mode:
                raise ValidationError(self.ERROR_BAD_TYPE.format("boolean"))

            # try to convert
            if not isinstance(value, str):
                raise ValidationError(self.ERROR_BAD_TYPE.format("boolean"))

            # TODO: Move string values to params?
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            else:
                raise ValidationError(self.ERROR_BAD_TYPE.format("boolean"))

        # allowed
        if allowed is not None:
            if value not in allowed:
                raise ValidationError(self.ERROR_UNALLOWED_VALUE.format(value))

        return value


    async def validate_file(self, value, strict_mode: bool = True):
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        strict_mode : bool, optional
            ...

        Returns
        -------

        """
        print(value)

        return value


    async def validate_objectid(self, value, *, default: str = None, nullable: bool = False, data_relation: dict,
                                strict_mode: bool = True) -> str:
        """

        Parameters
        ----------
        value : any
            Value, to be validated.
        default : str or None, optional
            ...
        nullable : bool, optional
            ...
        data_relation : dict
            ...
        strict_mode : bool, optional
            Enables strict type checking.

        Returns
        -------
        str
        """
        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, str):
            raise ValidationError(self.ERROR_BAD_TYPE.format('objectid'))

        if len(value) != 36:
            raise ValidationError(self.ERROR_BAD_TYPE.format('objectid'))

        return value
