# coding: utf-8

from django.forms import MultiValueField, FloatField, ChoiceField
from django.core.exceptions import ValidationError
from django.utils.itercompat import is_iterable
from django.utils.translation import ugettext_lazy as _

from quantity_field import ureg
from quantity_field.base import MultiQuantity
from quantity_field.widgets import MultiQuantityWidget


class MultiQuantityFormField(MultiValueField):
    """
    Field for Django forms that supports editing of multidimensional physical quantities.

    Args:
        dim (int): Positive integer, defines the number of dimensions. Default is 1.
        choices (list): A list containing (Pint unit, human readable unit name) tuples.

    Example:
        >>> weight = MultiQuantityFormField(choices=[(ureg.g, 'gram'), (ureg.kg, 'kilogram')])
        >>> size = MultiQuantityFormField(dim=3, choices=[(ureg.cm, 'centimeter'), (ureg.m, 'meter')])
    """

    error_messages = {
        'invalid_dim': _('`dim` must be a positive integer.'),
        'invalid_choices': _('`choices` must be an iterable containing (`Pint` unit, human readable unit name) tuples.'),
        'different_units': _('All `Pint` units must be the same dimensionality.'),
    }

    def __init__(self, *args, **kwargs):
        dim = kwargs.pop('dim', 1)
        choices = kwargs.pop('choices', None)

        if not isinstance(dim, int) or (dim < 1):
            raise ValidationError(self.error_messages['invalid_dim'])

        if not is_iterable(choices) or \
                any(not is_iterable(c) for c in choices) or \
                any(not isinstance(c[0], ureg.Unit) for c in choices):
            raise ValidationError(self.error_messages['invalid_choices'])

        if any(c[0].dimensionality != choices[0][0].dimensionality for c in choices):
            raise ValidationError(self.error_messages['different_units'])

        fields = [FloatField() for i in range(dim)] + [ChoiceField(choices=[(str(u), c) for u, c in choices])]

        kwargs.update({
            'widget': MultiQuantityWidget(dim=dim, choices=choices)
        })

        super(MultiQuantityFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return MultiQuantity.from_list(*data_list)
