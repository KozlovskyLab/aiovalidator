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
    Raised when the target dictionary is missing or has the wrong format.
    """
    def __init__(self, msg: str, issues={}):
        self._msg = msg
        # self._issues = issues
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

    ERROR_MIN_LENGTH = "min length is '{0}'"
    ERROR_MAX_LENGTH = "max length is '{0}'"
    ERROR_EMPTY_NOT_ALLOWED = "empty values not allowed"
    ERROR_UNALLOWED_VALUE = "unallowed value '{0}'"
    ERROR_REGEX = "value does not match regex '{0}'"

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
        errors = {}

        # default
        if value is None and default is not None:
            value = default

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
                        errors[key] = ValidationError(self.ERROR_REQUIRED_FIELD)
                    else:
                        # Returns default values
                        if 'default' in validator_params:
                            value[key] = validator_params['default']
                        else:
                            value[key] = None
                else:
                    try:
                        value[key] = await self.validate(_value, **validator_params, strict_mode=strict_mode)
                    except ValidationError as e:
                        errors[key] = e

            # allow_unknown
            if allow_unknown is False:
                for key, _value in value.items():
                    if key not in schema.keys():
                        errors[key] = ValidationError(self.ERROR_UNKNOWN_FIELD)
                        #del value[key]

        if len(errors.keys()):
            raise ValidationError(errors)

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
        errors = {}

        # default
        if value is None and default is not None:
            value = default

        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, Sequence):
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
                    errors[i] = e

        if len(errors.keys()):
            raise ValidationError(errors)

        return value


    async def validate_objectid(self, value, *, default: str = None, nullable: bool = False, data_relation: dict,
                                strict_mode: bool = True):
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

        """
        # default
        if value is None and default is not None:
            value = default

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


    def validate_string(self, value, *, default: str = None, nullable: bool = False, minlength: int = None,
                        maxlength: int = None, empty: bool = False, allowed: list = None, regex: str = None,
                        strict_mode: bool = True):
        """
        `validate_string` validates a string.

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
        # default
        if value is None and default is not None:
            value = default

        # nullable
        if value is None and nullable is False:
            raise ValidationError(self.ERROR_NOT_NULLABLE)

        if value is None:
            return value

        # type
        if not isinstance(value, str):
            if strict_mode is True:
                raise ValidationError(self.ERROR_BAD_TYPE.format('string'))

            value = str(value)
            # TODO: Add validate convertation?

        # minlength
        if minlength is not None:
            if len(value) < minlength:
                raise ValidationError(self.ERROR_MIN_LENGTH.format(minlength))

        # maxlength
        if maxlength is not None:
            if len(value) > maxlength:
                raise ValidationError(self.ERROR_MAX_LENGTH.format(maxlength))

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
                raise ValidationError(self.ERROR_REGEX.format(regex))

        return value


    def validate_integer(self, value, *, default: int = None, nullable: bool = False, min: int = None, max: int = None,
                         allowed: list = None, strict_mode: bool = True):
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
        # default
        if value is None and default is not None:
            value = default

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
                value = int(value)
            except ValueError as e:
                raise ValidationError(self.ERROR_BAD_TYPE.format("integer"))

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


    def validate_file(self, value, strict_mode: bool = True):
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
