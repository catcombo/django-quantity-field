# coding: utf-8

from pint import UnitRegistry
from django.conf import settings

__version__ = VERSION = (1, 0, 1)
ureg = UnitRegistry()

try:
    DIMENSIONALITY = settings.DIMENSIONALITY
except:
    DIMENSIONALITY = True
