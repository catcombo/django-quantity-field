# coding: utf-8

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.forms import modelform_factory

from quantity_field import ureg
from quantity_field.base import MultiQuantity
from quantity_field.forms import MultiQuantityFormField
from tests.models import Package


class MultiQuantityFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MultiQuantityFormTest, cls).setUpClass()
        cls.TestForm = modelform_factory(Package, fields=("size",))

        size = MultiQuantity.from_list(2, 5.5, 4, str(ureg.m))
        weight = MultiQuantity.from_string('42 kilogram')
        cls.entry = Package.objects.create(size=size, weight=weight)

    def test_form_field(self):
        self.assertRaises(ValidationError, MultiQuantityFormField)
        self.assertRaises(ValidationError, MultiQuantityFormField, dim=3.0)
        self.assertRaises(ValidationError, MultiQuantityFormField, dim=-4)
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=42)
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=[1, 1, 2, 3, 5])
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=[('kg', 'kilogram')])
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=[(ureg.g, 'gram'), (ureg.m, 'meter')])

    def test_form(self):
        form = self.TestForm(data={'size_0': '2', 'size_1': '3.5', 'size_2': '11', 'size_3': 'meter'})
        self.assertTrue(form.is_valid())

    def test_model_form(self):
        form = self.TestForm(data={'size_0': '2', 'size_1': '3.5', 'size_2': '11', 'size_3': 'meter'}, instance=self.entry)
        self.assertTrue(form.is_valid())
        form.save()
