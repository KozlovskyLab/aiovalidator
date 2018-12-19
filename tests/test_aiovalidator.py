#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the `aiovalidator` package.
# (c) 2016-2018 alldbx <welcome@alldbx.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
"""
:Authors:
    - `Vladimir Kozlovsky <vladimir@alldbx.com>`_
"""
import pytest

from aiovalidator import Validator, ValidationError


class TestValidator:

    @pytest.fixture
    def validator(self):
        return Validator()

    def test_validate_string_type_str(self, validator):
        # ok / strict_mode=True
        assert 'string' == validator.validate_string('string', default=None, nullable=False, minlength=None,
                                                     maxlength=None, empty=False, allowed=None, regex=None,
                                                     strict_mode=True)

        # ok / strict_mode=False
        assert 'string' == validator.validate_string('string', default=None, nullable=False, minlength=None,
                                                     maxlength=None, empty=False, allowed=None, regex=None,
                                                     strict_mode=False)

    def test_validate_string_type_bool(self, validator):
        # error / strict_mode=True
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(True, default=None, nullable=False, minlength=None, maxlength=None, empty=False,
                                      allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

        # error / strict_mode=False
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(True, default=None, nullable=False, minlength=None, maxlength=None, empty=False,
                                      allowed=None, regex=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

    def test_validate_string_type_int(self, validator):
        # error / strict_mode=True
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(123, default=None, nullable=False, minlength=None, maxlength=None, empty=False,
                                      allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

        # ok / strict_mode=False
        assert '123' == validator.validate_string(123, default=None, nullable=False, minlength=None, maxlength=None,
                                                  empty=False, allowed=None, regex=None, strict_mode=False)

    def test_validate_string_type_float(self, validator):
        # error / strict_mode=True
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(123.123, default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

        # ok / strict_mode=False
        assert '123.123' == validator.validate_string(123.123, default=None, nullable=False, minlength=None,
                                                      maxlength=None, empty=False, allowed=None, regex=None,
                                                      strict_mode=False)

    def test_validate_string_type_array(self, validator):
        # error / strict_mode=True
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(['test'], default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

        # error / strict_mode=False
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(['test'], default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

    def test_validate_string_type_object(self, validator):
        # error / strict_mode=True
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string({'test': 'test'}, default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

        # error /strict_mode=False
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string({'test': 'test'}, default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('string')

    def test_validate_string_nullable(self, validator):
        # null / ok
        assert None is validator.validate_string(None, default=None, nullable=True, minlength=None, maxlength=None,
                                                 empty=False, allowed=None, regex=None, strict_mode=True)

        # null / error
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string(None, default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

    def test_validate_string_minlength(self, validator):
        assert 'string' == validator.validate_string('string', default=None, nullable=False, minlength=6,
                                                     maxlength=None, empty=False, allowed=None, regex=None,
                                                     strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string('string', default=None, nullable=False, minlength=7, maxlength=None,
                                      empty=False, allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_STR_MIN_LENGTH.format(7)

    def test_validate_string_maxlength(self, validator):
        assert 'string' == validator.validate_string('string', default=None, nullable=False, minlength=None,
                                                     maxlength=6, empty=False, allowed=None, regex=None,
                                                     strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string('string', default=None, nullable=False, minlength=None, maxlength=5,
                                      empty=False, allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_STR_MAX_LENGTH.format(5)

    def test_validate_string_empty(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string('', default=None, nullable=False, minlength=None, maxlength=None, empty=False,
                                      allowed=None, regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_EMPTY_NOT_ALLOWED

        assert '' == validator.validate_string('', default=None, nullable=False, minlength=None, maxlength=None,
                                               empty=True, allowed=None, regex=None, strict_mode=True)

    def test_validate_string_allowed(self, validator):
        assert 'string' == validator.validate_string('string', default=None, nullable=False, minlength=None,
                                                     maxlength=None, empty=False, allowed=['string', 'string1'],
                                                     regex=None, strict_mode=True)

        assert None is validator.validate_string(None, default=None, nullable=True, minlength=None, maxlength=None,
                                                 empty=False, allowed=['string', 'string1'], regex=None,
                                                 strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string('string', default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=['empty'], regex=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUE.format('string')

    def test_validate_string_regex(self, validator):
        assert 'string' == validator.validate_string('string', default=None, nullable=False, minlength=None,
                                                     maxlength=None, empty=False, allowed=None,
                                                     regex='^str([ing]+)$', strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_string('string', default=None, nullable=False, minlength=None, maxlength=None,
                                      empty=False, allowed=None, regex='^str([i]+)$', strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_STR_REGEX.format('^str([i]+)$')

    def test_validate_integer_type_int(self, validator):
        assert 123 == validator.validate_integer(123, default=None, nullable=False, min=None, max=None, allowed=None,
                                                 strict_mode=True)

        assert 123 == validator.validate_integer(123, default=None, nullable=False, min=None, max=None, allowed=None,
                                                 strict_mode=False)

    def test_validate_integer_type_float(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(123.123, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(123.123, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        assert 123 == validator.validate_integer(123.0, default=None, nullable=False, min=None, max=None,
                                                 allowed=None, strict_mode=False)

    def test_validate_integer_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer('123', default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        assert 123 == validator.validate_integer('123', default=None, nullable=False, min=None, max=None, allowed=None,
                                                 strict_mode=False)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer('abs123', default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

    def test_validate_integer_type_bool(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        assert 1 == validator.validate_integer(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                               strict_mode=False)

    def test_validate_integer_type_object(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer({'test': 'test'}, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer({'test': 'test'}, default=None, nullable=False, min=None, max=None,
                                       allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

    def test_validate_integer_type_array(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(['test'], default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(['test'], default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

    def test_validate_integer_nullable(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(None, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

        assert None is validator.validate_integer(None, default=None, nullable=True, min=None, max=None, allowed=None,
                                                  strict_mode=True)

    def test_validate_integer_min(self, validator):
        assert 9 == validator.validate_integer(9, default=None, nullable=False, min=9, max=None, allowed=None,
                                               strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(10, default=None, nullable=False, min=11, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MIN_VALUE.format(11)

    def test_validate_integer_max(self, validator):
        assert 9 == validator.validate_integer(9, default=None, nullable=False, min=None, max=9, allowed=None,
                                               strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(9, default=None, nullable=False, min=None, max=8, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MAX_VALUE.format(8)

    def test_validate_integer_allowed(self, validator):
        assert 9 == validator.validate_integer(9, default=None, nullable=False, min=None, max=None, allowed=[1, 9, 20],
                                               strict_mode=True)

        assert None is validator.validate_integer(None, default=None, nullable=True, min=None, max=None,
                                                  allowed=[1, 9, 20], strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(9, default=None, nullable=False, min=None, max=None, allowed=[1, 2, 3],
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUE.format(9)

    def test_validate_float_type_float(self, validator):
        assert 123.123 == validator.validate_float(123.123, default=None, nullable=False, min=None, max=None,
                                                   allowed=None, strict_mode=True)

        assert 123.123 == validator.validate_float(123.123, default=None, nullable=False, min=None, max=None,
                                                   allowed=None, strict_mode=False)

    def test_validate_float_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float('123.123', default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

        assert 123.123 == validator.validate_float('123.123', default=None, nullable=False, min=None, max=None,
                                                   allowed=None, strict_mode=False)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float('abs.123', default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

    def test_validate_float_type_bool(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

        assert 1.0 == validator.validate_float(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                               strict_mode=False)

        assert 0.0 == validator.validate_float(False, default=None, nullable=False, min=None, max=None, allowed=None,
                                               strict_mode=False)

    def test_validate_float_type_int(self, validator):
        assert 123.0 == validator.validate_float(123, default=None, nullable=False, min=None, max=None, allowed=None,
                                                 strict_mode=True)

        assert 123.0 == validator.validate_float(123, default=None, nullable=False, min=None, max=None, allowed=None,
                                                 strict_mode=False)

    def test_validate_float_type_array(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(['test'], default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(['test'], default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

    def test_validate_float_type_object(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float({'test': 'test'}, default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float({'test': 'test'}, default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('float')

    def test_validate_float_nullable(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(None, default=None, nullable=False, min=None, max=None, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

        assert None is validator.validate_float(None, default=None, nullable=True, min=None, max=None, allowed=None,
                                                strict_mode=True)

    def test_validate_float_min(self, validator):
        assert 1.23 == validator.validate_float(1.23, default=None, nullable=False, min=1.0, max=None, allowed=None,
                                                strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(1.23, default=None, nullable=False, min=1.5, max=None, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MIN_VALUE.format(1.5)

    def test_validate_float_max(self, validator):
        assert 1.23 == validator.validate_float(1.23, default=None, nullable=False, min=None, max=2.0, allowed=None,
                                                strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(1.23, default=None, nullable=False, min=None, max=1.0, allowed=None,
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MAX_VALUE.format(1.0)

    def test_validate_float_allowed(self, validator):
        assert 1.23 == validator.validate_float(1.23, default=None, nullable=False, min=None, max=None,
                                                allowed=[1.24, 1.23], strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_float(1.23, default=None, nullable=False, min=None, max=None, allowed=[1.0, 2.3],
                                     strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUE.format(1.23)

    def test_validate_number_type_float(self, validator):
        assert 123.123 == validator.validate_number(123.123, default=None, nullable=False, min=None, max=None,
                                                    allowed=None, strict_mode=True)

        assert 123.123 == validator.validate_number(123.123, default=None, nullable=False, min=None, max=None,
                                                    allowed=None, strict_mode=False)

    def test_validate_number_type_int(self, validator):
        assert 123 == validator.validate_number(123, default=None, nullable=False, min=None, max=None, allowed=None,
                                                strict_mode=True)

        assert 123 == validator.validate_number(123, default=None, nullable=False, min=None, max=None, allowed=None,
                                                strict_mode=False)

    def test_validate_number_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number('123.123', default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

        assert 123.123 == validator.validate_number('123.123', default=None, nullable=False, min=None, max=None,
                                                    allowed=None, strict_mode=False)

        assert 123 == validator.validate_number('123', default=None, nullable=False, min=None, max=None, allowed=None,
                                                strict_mode=False)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number('abs.123', default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

    def test_validate_number_type_bool(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(False, default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

        assert 1.0 == validator.validate_number(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                                strict_mode=False)

        assert 0.0 == validator.validate_number(False, default=None, nullable=False, min=None, max=None, allowed=None,
                                                strict_mode=False)

    def test_validate_number_type_array(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(['test'], default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(['test'], default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

    def test_validate_number_type_object(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number({'test': 'test'}, default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number({'test': 'test'}, default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('int or float')

    def test_validate_number_nullable(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(None, default=None, nullable=False, min=None, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

        assert None is validator.validate_number(None, default=None, nullable=True, min=None, max=None, allowed=None,
                                                 strict_mode=True)

    def test_validate_number_min(self, validator):
        assert 1.23 == validator.validate_number(1.23, default=None, nullable=False, min=1.0, max=None, allowed=None,
                                                 strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(1.23, default=None, nullable=False, min=1.5, max=None, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MIN_VALUE.format(1.5)

    def test_validate_number_max(self, validator):
        assert 1.23 == validator.validate_number(1.23, default=None, nullable=False, min=None, max=2.0, allowed=None,
                                                 strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(1.23, default=None, nullable=False, min=None, max=1.0, allowed=None,
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MAX_VALUE.format(1.0)

    def test_validate_number_allowed(self, validator):
        assert 1.23 == validator.validate_number(1.23, default=None, nullable=False, min=None, max=None,
                                                 allowed=[1.24, 1.23], strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number(1.23, default=None, nullable=False, min=None, max=None, allowed=[1.0, 2.3],
                                      strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUE.format(1.23)

    def test_validate_boolean_type_bool(self, validator):
        assert True is validator.validate_boolean(True, default=None, nullable=False, allowed=None, strict_mode=True)

        assert False is validator.validate_boolean('false', default=None, nullable=False, allowed=None,
                                                   strict_mode=False)

        assert True is validator.validate_boolean('true', default=None, nullable=False, allowed=None, strict_mode=False)

    def test_validate_boolean_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean('string', default=None, nullable=False, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean('string', default=None, nullable=False, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

    def test_validate_boolean_type_int(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(123, default=None, nullable=False, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(123, default=None, nullable=False, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

    def test_validate_boolean_type_float(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(123.123, default=None, nullable=False, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(123.123, default=None, nullable=False, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

    def test_validate_boolean_type_array(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(['test'], default=None, nullable=False, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(['test'], default=None, nullable=False, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

    def test_validate_boolean_type_object(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean({'test': 'test'}, default=None, nullable=False, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean({'test': 'test'}, default=None, nullable=False, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('boolean')

    def test_validate_boolean_nullable(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(None, default=None, nullable=False, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

        assert None is validator.validate_boolean(None, default=None, nullable=True, allowed=None, strict_mode=True)

    def test_validate_boolean_allowed(self, validator):
        assert None is validator.validate_boolean(None, default=None, nullable=True, allowed=[True], strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_boolean(True, default=None, nullable=False, allowed=[False], strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUE.format(True)

    async def test_validate_object_type_object(self, validator):
        assert {'test': 'test'} == await validator.validate_object({'test': 'test'}, properties=None, default=None,
                                                                   nullable=False, allow_unknown=False,
                                                                   strict_mode=True)

        assert {'test': 'test'} == await validator.validate_object({'test': 'test'}, properties=None, default=None,
                                                                   nullable=False, allow_unknown=False,
                                                                   strict_mode=False)

    async def test_validate_object_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object('test', properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object('test', properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

    async def test_validate_object_type_int(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(123, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(123, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

    async def test_validate_object_type_float(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(123.123, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(123.123, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

    async def test_validate_object_type_bool(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(True, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(True, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

    async def test_validate_object_type_array(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(['test'], properties=None, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(['test'], properties=None, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('object')

    async def test_validate_object_properties(self, validator):
        properties = {
            'test1': {
                'type': 'object',
                'properties': {
                    'test11': {'type': 'string'},
                    'test12': {'type': 'number'},
                    'test13': {'type': 'boolean'},
                    '^(en|ru)$': {'type': 'object', 'properties': {'title': {'type': 'string'}}},
                    '^key4(\d)$': {'type': 'string'}
                }
            },
            'test2': {'type': 'string'},
            'test3': {'type': 'integer'},
            'test4': {'type': 'boolean'}
        }
        dct = {
            'test1': {
                'test11': 'hello',
                'test12': 123.123,
                'test13': True,
                'en': {'title': 'hello3'},
                'ru': {'title': 'hello4'},
                'key40': 'hello1',
                'key41': 'hello2'
            },
            'test2': 'hello1',
            'test3': 123,
            'test4': False
        }

        assert dct == await validator.validate_object(dct, properties=properties, default=None, nullable=False,
                                                      allow_unknown=False, strict_mode=True)
        dct = {
            'test': {'test0': {'test01': 'hello'}},
            'test1': {
                'test111': {'test1111': False},
                'test12': False,
                'test13': 'hello',
                'en': 123,
                'ru': 'hello',
                'key3': True,
                'key40': 345,
                'key50': None
            },
            'test2': 123,
            'test3': 'hello'
        }
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(dct, properties=properties, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=True)
        error = {
            'test1': {
                'test11': 'required field',
                'test12': "must be of 'int or float' type",
                'test13': "must be of 'boolean' type",
                'en': "must be of 'object' type",
                'ru': "must be of 'object' type",
                'key3': "unknown field",
                'key40': "must be of 'string' type",
                'key50': "unknown field",
                'test111': "unknown field",
            },
            'test2': "must be of 'string' type",
            'test3': "must be of 'integer' type",
            'test4': 'required field',
            'test': 'unknown field'
        }
        assert exc_info.value.issues == error

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(dct, properties=properties, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=False)
        error = {
            'test': 'unknown field',
            'test1': {
                'test11': 'required field',
                'test111': "unknown field",
                'test13': "must be of 'boolean' type",
                'en': "must be of 'object' type",
                'ru': "must be of 'object' type",
                'key3': "unknown field",
                'key50': "unknown field",
            },
            'test3': "must be of 'integer' type",
            'test4': 'required field'
        }
        assert exc_info.value.issues == error

    async def test_validate_object_nullable(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object(None, properties=None, default=None, nullable=False, allow_unknown=False,
                                            strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

        None is await validator.validate_object(None, properties=None, default=None, nullable=True, allow_unknown=False,
                                                strict_mode=True)

    async def test_validate_object_required_field(self, validator):
        properties = {'test': {'type': 'string'}}
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=True)
        assert exc_info.value.issues == {'test': validator.ERROR_REQUIRED_FIELD}

        properties = {'test': {'type': 'array'}}
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=True)
        assert exc_info.value.issues == {'test': validator.ERROR_REQUIRED_FIELD}

    async def test_validate_object_allow_unknown(self, validator):
        properties = {'test': {'type': 'string'}}
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_object({'test1': 'test2'}, properties=properties, default=None, nullable=False,
                                            allow_unknown=False, strict_mode=True)
        assert exc_info.value.issues == {'test1': validator.ERROR_UNKNOWN_FIELD, 'test': validator.ERROR_REQUIRED_FIELD}

        properties = {'test': {'type': 'string', 'required': False}}
        assert {'test1': 'test2'} == await validator.validate_object({'test1': 'test2'}, properties=properties,
                                                                     default=None, nullable=False, allow_unknown=True,
                                                                     strict_mode=True)

    async def test_validate_object_default_string(self, validator):
        properties = {'test': {'type': 'string', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'string', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'string', 'required': False, 'default': 'test'}}
        assert {'test': 'test'} == await validator.validate_object({}, properties=properties, default=None,
                                                                   nullable=False, allow_unknown=False,
                                                                   strict_mode=True)

    async def test_validate_object_default_integer(self, validator):
        properties = {'test': {'type': 'integer', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'integer', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'integer', 'required': False, 'default': 123}}
        assert {'test': 123} == await validator.validate_object({}, properties=properties, default=None,
                                                                nullable=False, allow_unknown=False, strict_mode=True)

    async def test_validate_object_default_float(self, validator):
        properties = {'test': {'type': 'float', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'float', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'float', 'required': False, 'default': 123.123}}
        assert {'test': 123.123} == await validator.validate_object({}, properties=properties, default=None,
                                                                    nullable=False, allow_unknown=False,
                                                                    strict_mode=True)

    async def test_validate_object_default_number(self, validator):
        properties = {'test': {'type': 'number', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'number', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'number', 'required': False, 'default': 123}}
        assert {'test': 123} == await validator.validate_object({}, properties=properties, default=None,
                                                                nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'number', 'required': False, 'default': 123.123}}
        assert {'test': 123.123} == await validator.validate_object({}, properties=properties, default=None,
                                                                    nullable=False, allow_unknown=False,
                                                                    strict_mode=True)

    async def test_validate_object_default_boolean(self, validator):
        properties = {'test': {'type': 'number', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'number', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'number', 'required': False, 'default': True}}
        assert {'test': True} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'number', 'required': False, 'default': False}}
        assert {'test': False} == await validator.validate_object({}, properties=properties, default=None,
                                                                  nullable=False, allow_unknown=False, strict_mode=True)

    async def test_validate_object_default_object(self, validator):
        properties = {'test': {'type': 'object', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'object', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'object', 'required': False, 'default': {'test': 'test'}}}
        assert {'test': {'test': 'test'}} == await validator.validate_object({}, properties=properties, default=None,
                                                                             nullable=False, allow_unknown=False,
                                                                             strict_mode=True)

        properties = {'test': {'type': 'object', 'required': False, 'default': 'test'}}
        assert {'test': 'test'} == await validator.validate_object({}, properties=properties, default=None,
                                                                   nullable=False, allow_unknown=False,
                                                                   strict_mode=True)

    async def test_validate_object_default_array(self, validator):
        properties = {'test': {'type': 'array', 'required': False}}
        assert {} == await validator.validate_object({}, properties=properties, default=None, nullable=False,
                                                     allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'array', 'required': False, 'default': None}}
        assert {'test': None} == await validator.validate_object({}, properties=properties, default=None,
                                                                 nullable=False, allow_unknown=False, strict_mode=True)

        properties = {'test': {'type': 'array', 'required': False, 'default': ['array']}}
        assert {'test': ['array']} == await validator.validate_object({}, properties=properties, default=None,
                                                                      nullable=False, allow_unknown=False,
                                                                      strict_mode=True)

        properties = {'test': {'type': 'array', 'required': False, 'default': 'test'}}
        assert {'test': 'test'} == await validator.validate_object({}, properties=properties, default=None,
                                                                   nullable=False, allow_unknown=False,
                                                                   strict_mode=True)

    async def test_validate_array_type_array(self, validator):
        assert ['test'] == await validator.validate_array(['test'], items=None, default=None, nullable=False,
                                                          minlength=None, maxlength=None, allowed=None,
                                                          strict_mode=True)

        assert ['test'] == await validator.validate_array(['test'], items=None, default=None, nullable=False,
                                                          minlength=None, maxlength=None, allowed=None,
                                                          strict_mode=False)

    async def test_validate_array_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array('test', items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array('test', items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

    async def test_validate_array_type_int(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(123, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(123, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

    async def test_validate_array_type_float(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(123.123, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(123.123, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

    async def test_validate_array_type_bool(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(True, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(True, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

    async def test_validate_array_type_object(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array({'test': 'test'}, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array({'test': 'test'}, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('array')

    async def test_validate_array_items_integer(self, validator):
        items = {'type': 'integer'}
        assert [1, 2] == await validator.validate_array([1, 2], items=items, default=None, nullable=False,
                                                        minlength=None, maxlength=None, allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array([1, '2'], items=items, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert exc_info.value.issues == {1: validator.ERROR_BAD_TYPE.format('integer')}

    async def test_validate_array_items_float(self, validator):
        items = {'type': 'float'}
        assert [123.123, 2.31] == await validator.validate_array([123.123, 2.31], items=items, default=None,
                                                                 nullable=False, minlength=None, maxlength=None,
                                                                 allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(['123.123', 2.31], items=items, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert exc_info.value.issues == {0: validator.ERROR_BAD_TYPE.format('float')}

    async def test_validate_array_items_number(self, validator):
        items = {'type': 'number'}
        assert [123.123, 2] == await validator.validate_array([123.123, 2], items=items, default=None,
                                                              nullable=False, minlength=None, maxlength=None,
                                                              allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array([123.123, 2.31, 'test'], items=items, default=None, nullable=False,
                                           minlength=None, maxlength=None, allowed=None, strict_mode=True)
        assert exc_info.value.issues == {2: validator.ERROR_BAD_TYPE.format('int or float')}

    async def test_validate_array_items_string(self, validator):
        items = {'type': 'string'}
        assert ['123.123', 'test'] == await validator.validate_array(['123.123', 'test'], items=items, default=None,
                                                                     nullable=False, minlength=None, maxlength=None,
                                                                     allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(['123.123', 2.31, 'test'], items=items, default=None, nullable=False,
                                           minlength=None, maxlength=None, allowed=None, strict_mode=True)
        assert exc_info.value.issues == {1: validator.ERROR_BAD_TYPE.format('string')}

    async def test_validate_array_items_boolean(self, validator):
        items = {'type': 'boolean'}
        assert [True, False] == await validator.validate_array([True, False], items=items, default=None,
                                                               nullable=False, minlength=None, maxlength=None,
                                                               allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array([True, False, 'test'], items=items, default=None, nullable=False,
                                           minlength=None, maxlength=None, allowed=None, strict_mode=True)
        assert exc_info.value.issues == {2: validator.ERROR_BAD_TYPE.format('boolean')}

    async def test_validate_array_items_array(self, validator):
        items = {'type': 'array', 'items': {'type': 'string'}}
        assert [['test1', 'test2']] == await validator.validate_array([['test1', 'test2']], items=items, default=None,
                                                                      nullable=False, minlength=None, maxlength=None,
                                                                      allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array([['test1', False, 'test2']], items=items, default=None, nullable=False,
                                           minlength=None, maxlength=None, allowed=None, strict_mode=True)
        assert exc_info.value.issues == {0: {1: validator.ERROR_BAD_TYPE.format('string')}}

    async def test_validate_array_items_object(self, validator):
        items = {'type': 'object', 'properties': {'test': {'type': 'string'}}}
        assert [{'test': 'test2'}] == await validator.validate_array([{'test': 'test2'}], items=items, default=None,
                                                                     nullable=False, minlength=None, maxlength=None,
                                                                     allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array([{'test': False}, {'test': 'test1'}], items=items, default=None,
                                           nullable=False, minlength=None, maxlength=None, allowed=None,
                                           strict_mode=True)
        assert exc_info.value.issues == {0: {'test': validator.ERROR_BAD_TYPE.format('string')}}

    async def test_validate_array_nullable(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(None, items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_NOT_NULLABLE

        None is await validator.validate_array(None, items=None, default=None, nullable=True, minlength=None,
                                               maxlength=None, allowed=None, strict_mode=True)

    async def test_validate_array_minlength(self, validator):
        assert ['test1', 'test2'] == await validator.validate_array(['test1', 'test2'], items=None, default=None,
                                                                    nullable=False, minlength=2, maxlength=None,
                                                                    allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(['test1', 'test2'], items=None, default=None, nullable=False, minlength=3,
                                           maxlength=None, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MIN_LENGTH.format(3)

    async def test_validate_array_maxlength(self, validator):
        assert ['test1', 'test2'] == await validator.validate_array(['test1', 'test2'], items=None, default=None,
                                                                    nullable=False, minlength=None, maxlength=2,
                                                                    allowed=None, strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(['test1', 'test2'], items=None, default=None, nullable=False, minlength=None,
                                           maxlength=1, allowed=None, strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_MAX_LENGTH.format(1)

    async def test_validate_array_allowed(self, validator):
        assert ['test1', 'test2'] == await validator.validate_array(['test1', 'test2'], items=None,
                                                                    default=None, nullable=False, minlength=None,
                                                                    maxlength=None, allowed=['test', 'test1', 'test2'],
                                                                    strict_mode=True)

        with pytest.raises(ValidationError) as exc_info:
            await validator.validate_array(['test1', 'test2'], items=None, default=None, nullable=False, minlength=None,
                                           maxlength=None, allowed=['test', 'test1'], strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUES.format(['test2'])
