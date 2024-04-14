# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient


def patient_detail(request, patient_id):
    patient = Patient.objects.using('db1' if patient_id % 2 != 0 else 'db2').get(patient_id=patient_id)
    return render(request, 'insights/patient_detail.html', {'patient': patient})


def home(request):
    p1 = Patient.objects.using('db1').all()
    p2 = Patient.objects.using('db2').all()

    return render(request, 'insights/home.html', {'patients1': p1, 'patients2': p2})


def manager_view(request):
    p1 = Patient.objects.using('db1').all()
    p2 = Patient.objects.using('db2').all()
    return render(request, 'insights/manager_view.html', {'patients1': p1, 'patients2': p2})


def user_view(request):
    p1 = Patient.objects.using('db1').all()
    p2 = Patient.objects.using('db2').all()
    # if request.GET.get("user_id"):
    #     print(request.GET.get("user_id"))

    return render(request, 'insights/user_view.html', {'patients1': p1, 'patients2': p2})


def user_details(request, pk):
    user = Patient.objects.using('db2' if pk % 2 == 0 else 'db1').filter(patient_id=pk).get()
    # print('nananananananaanananananananaanananananana',user[0].name)

    params = {'user': user}

    return render(request, 'insights/user_details.html', params)

def analysis(request,pk):
    id = pk

    mypatient = Patient.objects.using('db2' if pk % 2 == 0 else 'db1').filter(patient_id=id).get()

    db1_data = Patient.objects.using('db1').filter(gender = mypatient.gender).all()

    db2_data = Patient.objects.using('db2').filter(gender=mypatient.gender).all()

    all_heights = list(db1_data.values_list('height', flat=True)) + list(db2_data.values_list('height', flat=True))
    all_weights = list(db1_data.values_list('weight', flat=True)) + list(db2_data.values_list('weight', flat=True))
    all_blood_pressures = list(db1_data.values_list('blood_pressure', flat=True)) + list(db2_data.values_list('blood_pressure', flat=True))
    all_oxygen_levels = list(db1_data.values_list('oxygen_level', flat=True)) + list(db2_data.values_list('oxygen_level', flat=True))
    all_heart_rates = list(db1_data.values_list('heart_rate', flat=True)) + list(db2_data.values_list('heart_rate', flat=True))

    def aggregate_data(attribute):
        return list(db1_data.values_list(attribute, flat=True)) + list(db2_data.values_list(attribute, flat=True))

    charts_data = [
        {'attribute': 'height', 'label': 'Height in inches', 'values': aggregate_data('height'), 'user_value': mypatient.height},
        {'attribute': 'weight', 'label': 'Weight in pounds', 'values': aggregate_data('weight'), 'user_value': mypatient.weight},
        {'attribute': 'blood_pressure', 'label': 'Blood Pressure in mmHg', 'values': aggregate_data('blood_pressure'), 'user_value': mypatient.blood_pressure},
        {'attribute': 'oxygen_level', 'label': 'Oxygen Level in %', 'values': aggregate_data('oxygen_level'), 'user_value': mypatient.oxygen_level},
        {'attribute': 'heart_rate', 'label': 'Heart Rate in bpm', 'values': aggregate_data('heart_rate'), 'user_value': mypatient.heart_rate},
        {'attribute': 'blood_sugar', 'label': 'Blood Sugar in mg/dL', 'values': aggregate_data('blood_sugar'), 'user_value': mypatient.blood_sugar},        {'attribute': 'sleep_hours', 'label': 'Sleep Hours per Night', 'values': aggregate_data('sleep_hours'), 'user_value': mypatient.sleep_hours},
        {'attribute': 'stress_level', 'label': 'Stress Level', 'values': aggregate_data('stress_level'), 'user_value': mypatient.stress_level}
    ]

    context = {
        'patient': mypatient,
        'charts_data': charts_data
    }

    return render(request,'insights/analysis.html', context)