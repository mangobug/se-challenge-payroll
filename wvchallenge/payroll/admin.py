# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from payroll.models import Payroll

class PayrollAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payroll, PayrollAdmin)
