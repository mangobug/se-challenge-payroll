# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv, os

from calendar import monthrange
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from payroll.models import Payroll

def get_employee_info(eid):
    payroll_years = Payroll.objects.filter(employee_id = eid).order_by('year').values('year').distinct()
    data = []
    for p in payroll_years:
        payroll_months = Payroll.objects.filter(employee_id = eid, year = p['year']).order_by('month').values('month').distinct()
        for m in payroll_months:
             total_hrs_worked = Payroll.objects.filter(employee_id = eid, year = p['year'], month = m['month'], day__in = range(1,15)).aggregate(Sum('hours_worked'))
             if total_hrs_worked:
                pay_period = '1/' + str(m['month']) + '/' + str(p['year']) + ' - ' + '15/' + str(m['month']) + '/' + str(p['year'])
                try:
                    job_group = Payroll.objects.filter(employee_id = eid)[0]['job_group']
                except:
                    job_group = None

                if total_hrs_worked['hours_worked__sum']:
                    if job_group == 'A':
                        amount_paid = total_hrs_worked['hours_worked__sum'] * 20
                    else:
                        amount_paid = total_hrs_worked['hours_worked__sum'] * 30

                    data.append( {'employee_id': eid, 'pay_period': pay_period, 'amount_paid': amount_paid} )

             total_hrs_worked = Payroll.objects.filter(employee_id = eid, year = p['year'], month = m['month'], day__in = range(16,31)).aggregate(Sum('hours_worked'))
             if total_hrs_worked:
                pay_period = '16/' + str(m['month']) + '/' + str(p['year']) + ' - ' + str(monthrange(p['year'], m['month'])[1]) + '/' + str(m['month']) + '/' + str(p['year'])
                try:
                    job_group = Payroll.objects.filter(employee_id = eid)[0]['job_group']
                except:
                    job_group = None

                if total_hrs_worked['hours_worked__sum']:
                    if job_group == 'A':
                        amount_paid = total_hrs_worked['hours_worked__sum'] * 20
                    else:
                        amount_paid = total_hrs_worked['hours_worked__sum'] * 30

                    data.append(  {'employee_id': eid, 'pay_period': pay_period, 'amount_paid': amount_paid} )
    return data

def index(request):
    employee_ids = Payroll.objects.order_by().values('employee_id').distinct()
    employee_list = []
    for eid in employee_ids:
        employee_info = get_employee_info(eid['employee_id'])
        employee_list.extend(employee_info)
    data = {
        'employee_list': employee_list
    }
    return render(request, 'index.html', context = data)

def traverse(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        Payroll.objects.all().delete()
        with open('upload/' + str(request.FILES['file'])) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['date'] == 'report id':
                    break
                Payroll.objects.create(date = datetime.strptime(row['date'], "%d/%m/%Y"), employee_id = int(row['employee id']),
                job_group = row['job group'], hours_worked = float(row['hours worked']), year = row['date'].split('/')[-1],
                month = row['date'].split('/')[1], day = row['date'].split('/')[0])
    return HttpResponseRedirect('/')

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return True
