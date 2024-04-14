# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, request
from django.shortcuts import render
from .models import Patient


def patient_detail(request, patient_id):
    patient = Patient.objects.using('db1' if patient_id % 2 != 0 else 'db2').get(patient_id=patient_id)
    return render(request, 'insights/patient_detail.html', {'patient': patient})


def home(request):
    p1 = Patient.objects.using('db1').all()
    p2 = Patient.objects.using('db2').all()

    return render(request, 'insights/patient_detail.html', {'patients1': p1, 'patients2': p2})
