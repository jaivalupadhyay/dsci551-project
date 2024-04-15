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

def bmi_analysis(Patient):
    # underweight
    underweight_count_db1 = Patient.objects.using('db1').filter(bmi__lt=18.5).count()
    underweight_count_db2 = Patient.objects.using('db2').filter(bmi__lt=18.5).count()
    underweight_count = underweight_count_db1 + underweight_count_db2

    # ideal weight (Normal range)
    idealweight_count_db1 = Patient.objects.using('db1').filter(bmi__gte=18.5, bmi__lt=25).count()
    idealweight_count_db2 = Patient.objects.using('db2').filter(bmi__gte=18.5, bmi__lt=25).count()
    idealweight_count = idealweight_count_db1 + idealweight_count_db2

    # overweight
    overweight_count_db1 = Patient.objects.using('db1').filter(bmi__gte=25, bmi__lt=30).count()
    overweight_count_db2 = Patient.objects.using('db2').filter(bmi__gte=25, bmi__lt=30).count()
    overweight_count = overweight_count_db1 + overweight_count_db2

    # Obese class I
    obese_class1_count_db1 = Patient.objects.using('db1').filter(bmi__gte=30, bmi__lt=35).count()
    obese_class1_count_db2 = Patient.objects.using('db2').filter(bmi__gte=30, bmi__lt=35).count()
    obese_class1_count = obese_class1_count_db1 + obese_class1_count_db2

    # Obese class II
    obese_class2_count_db1 = Patient.objects.using('db1').filter(bmi__gte=35, bmi__lt=40).count()
    obese_class2_count_db2 = Patient.objects.using('db2').filter(bmi__gte=35, bmi__lt=40).count()
    obese_class2_count = obese_class2_count_db1 + obese_class2_count_db2

    # Obese class III
    obese_class3_count_db1 = Patient.objects.using('db1').filter(bmi__gte=40).count()
    obese_class3_count_db2 = Patient.objects.using('db2').filter(bmi__gte=40).count()
    obese_class3_count = obese_class3_count_db1 + obese_class3_count_db2



    return underweight_count,idealweight_count,overweight_count,obese_class1_count,obese_class2_count,obese_class3_count


def manager_view(request):
    p1 = Patient.objects.using('db1').all()
    p2 = Patient.objects.using('db2').all()


    # Getting the count of all Patient objects in the queryset
    p1_count = p1.count()
    p2_count = p2.count()
    count = p1_count + p2_count


    # getting count of males
    male_count_db1 = Patient.objects.using('db1').filter(gender='Male').count()
    male_count_db2 = Patient.objects.using('db2').filter(gender='Male').count()
    male_count = male_count_db1 + male_count_db2

    #getting count of females
    Female_count_db1 = Patient.objects.using('db1').filter(gender='Female').count()
    Female_count_db2 = Patient.objects.using('db2').filter(gender='Female').count()
    Female_count = Female_count_db1 + Female_count_db2

    #bmi based analysis
    underweight_count,idealweight_count,overweight_count,obese_class1_count,obese_class2_count,obese_class3_count = bmi_analysis(Patient)

    db1_count = Patient.objects.using('db1').count()
    db2_count = Patient.objects.using('db2').count()


    # graph filters
    if request.method == "POST":
        xaxis = request.POST.get('xaxis')
        print('toiewofiobeoivbosdibcsidbsubd;sbc;obce;fsuob;ccb; dof dfi',xaxis)



    params={'patients1': p1,
            'patients2': p2,
            'count':count,
            'male_count':male_count,
            'female_count': Female_count,
            'underweight_count':underweight_count,
            'idealweight_count':idealweight_count,
            'overweight_count':overweight_count,
            'obese_class1_count':obese_class1_count,
            'obese_class2_count':obese_class2_count,
            'obese_class3_count':obese_class3_count,
            'db1_count': db1_count,
            'db2_count': db2_count

            }

    return render(request, 'insights/manager_view.html', params)


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


def bmi_calculation(height, weight):
    height_m = height / 100.0
    weight_kg = weight * 0.453592

    bmi = weight_kg / (height_m ** 2)

    return float(bmi)


def add(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        blood_type = request.POST.get('blood_type')
        blood_pressure = float(request.POST.get('blood_pressure'))
        oxygen_level = float(request.POST.get('oxygen_level'))
        blood_sugar = float(request.POST.get('blood_sugar'))
        heart_rate = float(request.POST.get('heart_rate'))
        cholesterol = float(request.POST.get('cholestrol'))
        body_temperature = float(request.POST.get('body_temperature'))
        sleep_hours = float(request.POST.get('sleep_hours'))
        stress_level = float(request.POST.get('stress_level'))

        bmi = bmi_calculation(height, weight)

        if gender == "male":
            gender = 'Male'

        if gender == 'female':
            gender = 'Female'

        print(f"""
        Patient ID: {patient_id}
        Name: {name}
        Age: {age}
        Gender: {gender}
        Height: {height} cm
        Weight: {weight} kg
        Blood Type: {blood_type}
        Blood Pressure: {blood_pressure}
        Oxygen Level: {oxygen_level}%
        blood_sugar: {blood_sugar}
        Heart Rate: {heart_rate} bpm
        Cholesterol: {cholesterol} mg/dL
        Body Temperature: {body_temperature} °C
        Sleep Hours: {sleep_hours} hours/night
        Stress Level: {stress_level}
        """)
        database = 'db1' if int(patient_id) % 2 != 0 else 'db2'

        new_patient = Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            blood_type=blood_type,
            blood_pressure=blood_pressure,
            oxygen_level=oxygen_level,
            blood_sugar=blood_sugar,
            heart_rate=heart_rate,
            cholesterol=cholesterol,
            body_temperature=body_temperature,
            bmi=bmi,
            sleep_hours=sleep_hours,
            stress_level=stress_level
        )
        new_patient.save(using=database)

        return redirect('manager_view')

    params = {}

    return render(request, 'insights/add.html', params)


def delete(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')

        if int(patient_id) % 2 == 0:
            patient = Patient.objects.using('db2').filter(patient_id=patient_id).delete()
        else:
            patient = Patient.objects.using('db1').filter(patient_id=patient_id).delete()

        # for patient in patients:
        #     patient.delete()

        return redirect('manager_view')
    return render(request, 'insights/delete.html')


def update(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        patient = Patient.objects.using('db2' if int(patient_id) % 2 == 0 else "db1").filter(patient_id=patient_id).get()
        Patient.objects.using('db2' if int(patient_id) % 2 == 0 else "db1").filter(patient_id=patient_id).delete()

        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        blood_type = request.POST.get('blood_type')
        blood_pressure = request.POST.get('blood_pressure')
        oxygen_level = request.POST.get('oxygen_level')
        blood_sugar = request.POST.get('blood_sugar')
        heart_rate = request.POST.get('heart_rate')
        cholesterol = request.POST.get('cholesterol')
        body_temperature = request.POST.get('body_temperature')
        sleep_hours = request.POST.get('sleep_hours')
        stress_level = request.POST.get('stress_level')

        # Updating fields if provided
        if name:
            patient.name = name
        if age:
            patient.age = age
        if gender:
            patient.gender = gender
        if height:
            patient.height = height
        if weight:
            patient.weight = weight
        if blood_type:
            patient.blood_type = blood_type
        if blood_pressure:
            patient.blood_pressure = blood_pressure
        if oxygen_level:
            patient.oxygen_level = oxygen_level
        if blood_sugar:
            patient.blood_sugar = blood_sugar
        if heart_rate:
            patient.heart_rate = heart_rate
        if cholesterol:
            patient.cholesterol = cholesterol
        if body_temperature:
            patient.body_temperature = body_temperature
        if sleep_hours:
            patient.sleep_hours = sleep_hours
        if stress_level:
            patient.stress_level = stress_level


        patient.save()

        return redirect('manager_view')

    params = {}
    return render(request, 'insights/update.html', params)

    params = {}
    return render(request, 'insights/delete.html', params)
