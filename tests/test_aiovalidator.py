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
import pytest

from aiovalidator import Validator, ValidationError


class TestValidator():

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


    def test_validate_string_type_list(self, validator):
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


    def test_validate_string_type_dict(self, validator):
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

        assert 123 == validator.validate_integer(123.123, default=None, nullable=False, min=None, max=None,
                                                 allowed=None, strict_mode=False)

    def test_validate_integer_type_str(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer('123', default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        assert 123 == validator.validate_integer('123', default=None, nullable=False, min=None, max=None, allowed=None,
                                                 strict_mode=False)

    def test_validate_integer_type_bool(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        assert 1 == validator.validate_integer(True, default=None, nullable=False, min=None, max=None, allowed=None,
                                               strict_mode=False)

    def test_validate_integer_type_dict(self, validator):
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer({'test': 'test'}, default=None, nullable=False, min=None, max=None, allowed=None,
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')

        with pytest.raises(ValidationError) as exc_info:
            assert 1 == validator.validate_integer({'test': 'test'}, default=None, nullable=False, min=None, max=None,
                                                   allowed=None, strict_mode=False)
        assert str(exc_info.value) == validator.ERROR_BAD_TYPE.format('integer')


    def test_validate_integer_type_list(self, validator):
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

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_integer(9, default=None, nullable=False, min=None, max=None, allowed=[1, 2, 3],
                                       strict_mode=True)
        assert str(exc_info.value) == validator.ERROR_UNALLOWED_VALUE.format(9)
