# coding: utf-8

import sys

from django.core import serializers
from django.core.exceptions import ValidationError
from django.test import TestCase

from quantity_field import ureg
from quantity_field.base import MultiQuantity
from quantity_field.fields import MultiQuantityField
from tests.models import Package


class MultiQuantityFieldTest(TestCase):
    def setUp(self):
        size = MultiQuantity.from_list(2, 5.5, 4, str(ureg.m))
        weight = MultiQuantity.from_string('42 kilogram')
        self.entry = Package.objects.create(size=size, weight=weight)

    def test_field(self):
        self.assertRaises(ValidationError, MultiQuantityField)
        self.assertRaises(ValidationError, MultiQuantityField, dim=3.0)
        self.assertRaises(ValidationError, MultiQuantityField, dim=-4)
        self.assertRaises(ValidationError, MultiQuantityField, units=42)
        self.assertRaises(ValidationError, MultiQuantityField, units=[1, 1, 2, 3, 5])
        self.assertRaises(ValidationError, MultiQuantityField, units=(ureg.g, ureg.m,))

    def test_deconstruct(self):
        field = MultiQuantityField(units=(ureg.g, ureg.kg))

        name, path, args, kwargs = field.deconstruct()
        module, cls = path.rsplit('.', 1)
        field_class = getattr(sys.modules[module], cls)
        field_instance = field_class(*args, **kwargs)

        self.assertIsInstance(field_instance, field.__class__)

    def test_serialize(self):
        data = serializers.serialize('xml', Package.objects.all())
        first = serializers.deserialize('xml', data).next().object
        self.assertEqual(first, Package.objects.first())

    def test_read(self):
        self.entry.refresh_from_db()

        size = MultiQuantity.from_list(2, 5.5, 4, str(ureg.m))
        self.assertEqual(self.entry.size, size)

        weight = MultiQuantity.from_string('42 kilogram')
        self.assertEqual(self.entry.weight, weight)

    def test_write(self):
        weight = MultiQuantity.from_string('2 kg')

        self.entry.weight = weight
        self.entry.save()

        self.entry.refresh_from_db()
        self.assertEqual(self.entry.weight, weight)
