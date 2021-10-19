# coding: utf-8

from django.forms.widgets import MultiWidget, Select, TextInput


class MultiQuantityWidget(MultiWidget):
    """
    Widget for Django forms that supports editing of multidimensional physical quantities.

    Args:
        dim (int): Positive integer, defines the number of dimensions.
        choices (list): A list containing (Pint unit representation, human readable unit name) tuples.

    Example:
        >>> weight = MultiQuantityWidget(dim=1, choices=[('gram', 'g'), ('kilogram', 'kg')])
    """

    template_name = 'layout/widgets/multi_widgets.html'

    def __init__(self, dim, choices, *args, **kwargs):
        widgets = [TextInput() for i in range(dim)] + [Select(choices=choices)]
        super(MultiQuantityWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return value.to_list()
        else:
            return []
