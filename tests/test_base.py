# coding: utf-8

import unittest

from quantity_field import ureg
from quantity_field.base import MultiQuantity


class MultiQuantityTest(unittest.TestCase):
    def test_single_value(self):
        self.assertIsInstance(MultiQuantity(0), ureg.Quantity)

        self.assertEqual(MultiQuantity(3.5, ureg.kg), 3.5 * ureg.kg)
        self.assertEqual(MultiQuantity.from_string('42 kilogram'), 42 * ureg.kg)

        mq = MultiQuantity.from_list(100, ureg.m)
        self.assertEqual(mq, 100 * ureg.m)
        self.assertEqual(mq.units, ureg.m)
        self.assertEqual(mq[0], 100 * ureg.m)
        self.assertEqual(mq.dim, 1)

        self.assertEqual(mq * 2 * ureg.m, 200 * ureg.m * ureg.m)
        self.assertGreater(mq, 50 * ureg.m)

        self.assertEqual(unicode(mq), '100.0 meter')
        self.assertEqual(mq.to_string(), '100.0 meter')
        self.assertEqual(mq.to_list(), [100, 'meter'])

    def test_multi_value(self):
        self.assertEqual(MultiQuantity.from_string('2.5*4*3 meter'), 30 * ureg.m ** 3)

        mq = MultiQuantity.from_list(2.5, 4, ureg.m)
        self.assertEqual(mq, 10 * ureg.m ** 2)
        self.assertEqual(mq.units, ureg.m ** 2)
        self.assertEqual([q for q in mq], [2.5 * ureg.m, 4 * ureg.m])
        self.assertEqual(mq.dim, 2)

        self.assertEqual(mq * 2 * ureg.m, 20 * ureg.m ** 3)
        self.assertGreater(mq, 5 * ureg.m ** 2)

        self.assertEqual(unicode(mq), '2.5*4.0 meter')
        self.assertEqual(mq.to_string(), '2.5*4.0 meter')
        self.assertEqual(mq.to_list(), [2.5, 4, 'meter'])
