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
    height_list1 = [i.height for i in db1_data]
    height_list2 = [i.height for i in db2_data]
    height_list1.extend(height_list2)

    params ={'id':id, 'mypatient':mypatient, 'all_data': height_list1}
    return render(request,'insights/analysis.html', params)