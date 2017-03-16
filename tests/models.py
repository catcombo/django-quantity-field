# coding: utf-8

from django.db import models

from quantity_field import ureg
from quantity_field.fields import MultiQuantityField


class Package(models.Model):
    size = MultiQuantityField(dim=3, units=(ureg.mm, ureg.cm, ureg.m))
    weight = MultiQuantityField(units=(ureg.g, ureg.kg))
