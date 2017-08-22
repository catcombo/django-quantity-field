# coding: utf-8

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.forms import modelform_factory

from quantity_field import ureg
from quantity_field.forms import MultiQuantityFormField
from tests.models import Package


class MultiQuantityFormTest(TestCase):
    def test_form_field(self):
        self.assertRaises(ValidationError, MultiQuantityFormField)
        self.assertRaises(ValidationError, MultiQuantityFormField, dim=3.0)
        self.assertRaises(ValidationError, MultiQuantityFormField, dim=-4)
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=42)
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=[1, 1, 2, 3, 5])
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=[('kg', 'kilogram')])
        self.assertRaises(ValidationError, MultiQuantityFormField, choices=[(ureg.g, 'gram'), (ureg.m, 'meter')])

    def test_form(self):
        TestForm = modelform_factory(Package, fields=("size",))
        form = TestForm(data={'size_0': '2', 'size_1': '3.5', 'size_2': '11', 'size_3': 'meter'})
        self.assertTrue(form.is_valid())
