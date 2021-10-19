# coding: utf-8

from six import python_2_unicode_compatible
from quantity_field import ureg
from functools import reduce


@python_2_unicode_compatible
class MultiQuantity(ureg.Quantity):
    """
    A class for working with multi quantity values. Can be instantiated from
    string in corresponded format or from list of values and Pint units.

    Example:
        >>> empty = MultiQuantity(0)
        >>> tv = MultiQuantity(3.5, ureg.kg)
        >>> package = MultiQuantity.from_string('42 kilogram')
        >>> box = MultiQuantity.from_string('2*5.5*4 meter')
        >>> chest = MultiQuantity.from_list(2, 5.5, 4, 'm')
        >>> square = MultiQuantity.from_list(4, 8, ureg.m)
    """

    SEPARATOR = '*'  # Used for serialization and deserialization

    def __init__(self, *args, **kwargs):
        self._values = [self]

    def __str__(self):
        return self.to_string()

    def __getitem__(self, i):
        return self._values[i]

    def __iter__(self):
        return iter(self._values)

    def compare(self, other, op):
        q = ureg.Quantity(self.magnitude, self.units)
        return q.compare(other, op)

    @property
    def dim(self):
        """int: Returns the number of dimensions."""
        return len(self._values)

    @classmethod
    def from_list(cls, *args):
        """:obj:`MultiQuantity`: Instantiate object from a list.

        Args:
            args: List of numeric values and Pint units.

        Example:
            >>> volume = MultiQuantity.from_list(2, 5.5, 4, 'meter')
            >>> square = MultiQuantity.from_list(4, 8, ureg.m)
        """

        value = reduce((lambda x, y: x * y), args[:-1])
        base_units = isinstance(args[-1], ureg.Unit) and args[-1] or ureg(args[-1])
        units = pow(base_units, len(args[:-1]))

        mq = cls(value, units)
        mq._values = [float(v) * base_units for v in args[:-1]]

        return mq

    @classmethod
    def from_string(cls, data):
        """:obj:`MultiQuantity`: Instantiate object from string.

        Args:
            data (str): String in corresponded format.

        Example:
            >>> mq = MultiQuantity.from_string('2.0*5.5*4.0 meter')
        """

        packed_values = data.split(cls.SEPARATOR)
        packed_values = packed_values[:-1] + packed_values[-1].split()
        packed_values = [float(v) for v in packed_values[:-1]] + [packed_values[-1]]

        return cls.from_list(*packed_values)

    def to_list(self):
        """list: Returns serialized object as a list.

        Example:
            >>> mq = MultiQuantity.from_list(2, 5.5, 4, 'meter')
            >>> mq.to_list()
            [2.0, 5.5, 4.0, 'meter']
        """
        return [v.magnitude for v in self._values] + [str(self[0].units)]

    def to_string(self):
        """str: Returns serialized object as a string.

        Example:
            >>> mq = MultiQuantity.from_list(2, 5.5, 4, 'meter')
            >>> mq.to_string()
            '2.0*5.5*4.0 meter'
        """
        return self.SEPARATOR.join([str(v.magnitude) for v in self._values]) + ' ' + str(self[0].units)
