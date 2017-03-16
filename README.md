# django-quantity-field

A Django application providing model and form field
to accept and store multidimensional physical quantities.


## Requirements

This application depends on `Pint` library, used for operate
and manipulate physical quantities. Full documentation is
available at http://pint.readthedocs.org/


## Installation

1. Install django-quantity-field using pip: `pip install -e git://github.com/tapeit/django-quantity-field`.
2. Add `'quantity_field'` to your `INSTALLED_APPS` setting.


## Usage

In order to use a quantity field add it to your model definition:

    from quantity_field import ureg
    from quantity_field.fields import MultiQuantityField

    class Package(models.Model):
        size = MultiQuantityField(dim=3, units=(ureg.mm, ureg.cm, ureg.m))
        weight = MultiQuantityField(units=(ureg.g, ureg.kg))

`django-quantity-field` comes with the custom form field that is
used by default for editing in admin or in your forms.

Accessing `MultiQuantityField` field will returns `MultiQuantity` object
that can be used as ordinary Pint quantities.

    >>> from quantity_field.base import MultiQuantity
    >>> size = MultiQuantity.from_list(2, 5.5, 4, str(ureg.m))
    >>> size
    <Quantity(44.0, 'meter ** 3')>
    >>> size.dim
    3
    >>> [v for v in size]
    [<Quantity(2.0, 'meter')>, <Quantity(5.5, 'meter')>, <Quantity(4.0, 'meter')>]


## Warning

Don't forget there are no global units in Pint. To use Pint quantities
in your project side by side with `django-quantity-field` use
Pint registry from our application.

    >>> from quantity_field import ureg
    >>> from quantity_field.base import MultiQuantity
    >>> box = MultiQuantity.from_string('42 kg')
    >>> box + 2.2 * ureg.kg
    <Quantity(44.2, 'kilogram')>
