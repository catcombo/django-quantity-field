# coding: utf-8

from django.test import TestCase

from quantity_field.base import MultiQuantity
from quantity_field.widgets import MultiQuantityWidget


class MultiQuantityWidgetTest(TestCase):
    def test_widget(self):
        mq = MultiQuantity.from_list(2, 'kg')
        widget = MultiQuantityWidget(dim=1, choices=[('gram', 'g'), ('kilogram', 'kg')])

        self.assertIn('<input name="weight_0" type="text" />', widget.render('weight', None))
        self.assertIn('<option value="kilogram">kg</option>', widget.render('weight', None))

        self.assertIn('<input name="weight_0" type="text" value="2.0" />', widget.render('weight', mq))
        self.assertIn('<option value="kilogram" selected="selected">kg</option>', widget.render('weight', mq))
