# coding: utf-8

from django.test import TestCase

from quantity_field.base import MultiQuantity
from quantity_field.widgets import MultiQuantityWidget
from .utils import contains_partial


class MultiQuantityWidgetTest(TestCase):
    def test_widget(self):
        mq = MultiQuantity.from_list(2, 'kg')
        widget = MultiQuantityWidget(dim=1, choices=[('gram', 'g'), ('kilogram', 'kg')])

        self.assertTrue(contains_partial(widget.render('weight', None), '<input name="weight_0" type="text" />'))
        self.assertTrue(contains_partial(widget.render('weight', None), '<option value="kilogram">kg</option>'))

        self.assertTrue(contains_partial(widget.render('weight', mq),
                                         '<input name="weight_0" type="text" value="2.0" />'))
        self.assertTrue(contains_partial(widget.render('weight', mq),
                                         '<option value="kilogram" selected="selected">kg</option>'))
