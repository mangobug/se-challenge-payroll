# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Payroll(models.Model):
    employee_id = models.IntegerField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    job_group = models.CharField(max_length=1)
    date = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
