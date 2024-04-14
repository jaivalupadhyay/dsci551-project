# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Patient

def patient_detail(request, patient_id):
    patient = Patient.objects.using('db1' if patient_id % 2 != 0 else 'db2').get(patient_id=patient_id)
    return render(request, 'insights/patient_detail.html', {'patient': patient})
