# coding: utf-8

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext as _

from quantity_field import ureg
from quantity_field.base import MultiQuantity
from quantity_field.forms import MultiQuantityFormField


class MultiQuantityField(models.Field):
    """
    Field for Django models that stores multidimensional physical quantities.

    Args:
        dim (int): Positive integer, defines the number of dimensions. Default is 1.
        units (list): A list of the Pint units of the same dimensionality.
    """

    error_messages = {
        'invalid_dim': _('`dim` must be a positive integer.'),
        'require_units': _('`units` must be an iterable (e.g., a list or tuple).'),
        'invalid_units': _('`units` must contain `Pint` units.'),
        'different_units': _('`units` must contain `Pint` units of the same dimensionality.'),
    }

    def __init__(self, *args, **kwargs):
        self.dim = kwargs.pop('dim', 1)
        self.units = kwargs.pop('units', None)

        if not isinstance(self.dim, int) or (self.dim < 1):
            raise ValidationError(self.error_messages['invalid_dim'])

        if not is_iterable(self.units):
            raise ValidationError(self.error_messages['require_units'])

        if any(not isinstance(u, (ureg.Unit, str)) for u in self.units):
            raise ValidationError(self.error_messages['invalid_units'])

        self.units = list(map(lambda u: isinstance(u, str) and ureg(u) or u, self.units))

        if any(u.dimensionality != self.units[0].dimensionality for u in self.units):
            raise ValidationError(self.error_messages['different_units'])

        kwargs['max_length'] = 255
        super(MultiQuantityField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def deconstruct(self):
        name, path, args, kwargs = super(MultiQuantityField, self).deconstruct()

        kwargs['dim'] = self.dim
        kwargs['units'] = map(str, self.units)
        del kwargs['max_length']

        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context=None):
        """
        Converts a value as returned by the database to a Python object.
        It is the reverse of get_prep_value().
        """

        if value is None:
            return value

        return MultiQuantity.from_string(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        if isinstance(value, MultiQuantity):
            return value.to_string()

        return value

    def to_python(self, value):
        """
        Method is called by deserialization and during the clean() method used from forms.
        """

        if value is None:
            return value

        if isinstance(value, MultiQuantity):
            return value

        return MultiQuantity.from_string(value)

    def value_to_string(self, obj):
        """
        Converting field data for serialization
        """

        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        """
        Returns a django.forms.Field instance for this database Field.
        """

        choices = [
            (unit, _(str(unit)))
            for unit in self.units
        ]

        defaults = {
            'form_class': MultiQuantityFormField,
            'dim': self.dim,
            'choices': choices,
        }
        defaults.update(kwargs)

        return super(MultiQuantityField, self).formfield(**defaults)
