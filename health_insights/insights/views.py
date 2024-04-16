# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import shutil
from pathlib import Path
import json
import os
from django.contrib import messages
from django.http import HttpResponse, request
from django.shortcuts import get_object_or_404
from .models import Patient
from .models import File
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.shortcuts import render
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


    # sleep speedometer
    sleep_hrs_list=[]
    sleep_db1 = Patient.objects.using('db1').all()
    sleep_db2 = Patient.objects.using('db2').all()

    for p in sleep_db1:
        sleep_hrs_list.append(p.sleep_hours)
    for p in sleep_db2:
        sleep_hrs_list.append(p.sleep_hours)

    sleep_hrs_list=sorted(sleep_hrs_list)
    average_sleep = sum(sleep_hrs_list) / len(sleep_hrs_list) if sleep_hrs_list else 0

    # stress speedometer
    stress_list=[]
    for p in sleep_db1:
        stress_list.append(p.stress_level)
    for p in sleep_db2:
        stress_list.append(p.stress_level)

    stress_list = sorted(stress_list)
    average_stress = sum(stress_list) / len(stress_list) if stress_list else 0

    # weight gauge
    weight_list=[]
    for p in sleep_db1:
        weight_list.append(p.cholesterol)
    for p in sleep_db2:
        weight_list.append(p.cholesterol)
    weight_list=sorted(weight_list)
    average_weight =sum(weight_list) / len(weight_list) if weight_list else 0

    # hight gauge
    height_list=[]
    for p in sleep_db1:
        height_list.append(p.oxygen_level)
    for p in sleep_db2:
        height_list.append(p.oxygen_level)
    height_list=sorted(height_list)
    average_height =sum(height_list) / len(height_list) if height_list else 0


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
            'db2_count': db2_count,
            'sleep_hours':sleep_hrs_list,
            'average_sleep': average_sleep,
            'stress_list':stress_list,
            'average_stress':average_stress,
            'weight_list':weight_list,
            'average_weight':average_weight,
            'height_list':height_list,
            'average_height':average_height

            }

    return render(request, 'insights/manager_view.html', params)


def manager_graphs(request):

    x_list = []
    y_list=[]
    x_axis ='null'
    y_axis='null'

    if request.method == 'POST':
        x_axis = request.POST.get('xaxis')
        y_axis = request.POST.get('yaxis')
        graph_type = request.POST.get('graph')



        print('Received x-axis value:', x_axis)
        print('Received y-axis value:', y_axis)

        # Querying the Patient objects using a specified database
        patients1 = Patient.objects.using('db1').all()

        # Assuming you want to print the value of attributes in patients that are named similarly to x_axis and y_axis dynamically
        for patient in patients1:
            # Safely getting attribute values based on string names with default fallback
            patient_x_value = getattr(patient, x_axis, "Attribute not found")
            x_list.append(patient_x_value)
            patient_y_value = getattr(patient, y_axis, "Attribute not found")
            y_list.append(patient_y_value)

        patients2 = Patient.objects.using('db2').all()

        for patient in patients2:
            # Safely getting attribute values based on string names with default fallback
            patient_x_value = getattr(patient, x_axis, "Attribute not found")
            x_list.append(patient_x_value)
            patient_y_value = getattr(patient, y_axis, "Attribute not found")
            y_list.append(patient_y_value)

    params={'xlabel':x_axis.upper(),
            'ylabel':y_axis.upper(),
            'x_list':x_list,
            'y_list':y_list,
            'graph': graph_type
            }
    return render(request,'insights/manager_graphs.html',params)

def user_view(request):
    p1 = Patient.objects.using('db1').all()
    p2 = Patient.objects.using('db2').all()

    return render(request, 'insights/user_view.html', {'patients1': p1, 'patients2': p2})


def user_details(request, pk):
    user = Patient.objects.using('db2' if pk % 2 == 0 else 'db1').filter(patient_id=pk).get()

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
    height_m = height * 0.0254
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

def delete_directory_contents(path):
    p = Path(path)
    if p.exists():  # Check if the directory exists
        for sub in p.iterdir():  # iterates over the items of the directory
            if sub.is_dir():
                shutil.rmtree(sub)  # removes directories recursively
            else:
                sub.unlink()  # removes files and links
        print(f"Contents of {path} have been deleted.")
    else:
        print(f"The directory {path} does not exist.")
def add_multiple(request):
    if request.method == "POST":
        file = request.FILES.get('file')

        if file is not None:
            if not file.name.lower().endswith('.json'):
                return HttpResponse("File is not a JSON type", status=400)

            # Create a new File instance and save the uploaded file
            File.objects.create(file=file)

            # print(f'Uploaded file name: {file.name}')
            file_name =  file.name
            json_file = os.getcwd() + f'/media/{file.name}'

            print("Current working directory:", os.getcwd())

            with open(json_file,'r') as dataset:
                data = json.load(dataset)['Sheet1']

                for item in data:
                    patient_id = item['Patient ID']
                    database = 'db2' if int(patient_id) % 2 == 0 else 'db1'

                    patient_record = {
                        'patient_id': patient_id,
                        'name': item['Name'],
                        'age': item.get('Age', None),
                        'gender': item.get('Gender', None),
                        'height': item.get('Height(Inches)', None),
                        'weight': item.get('Weight(Pounds)', None),
                        'blood_type': item.get('Blood Type', None),
                        'blood_pressure': item.get('Blood Pressure', None),
                        'oxygen_level': item.get('Oxygen level', None),
                        'heart_rate': item.get('Heart Rate', 0),
                        'blood_sugar': item.get('Blood Sugar', None),
                        'cholesterol': item.get('Cholestrol', 0),  # Corrected field name spelling
                        'body_temperature': item.get('Body Temeperature', None),  # Corrected field name spelling
                        'sleep_hours': item.get('Sleep Hours', None),
                        'bmi': item.get('BMI', None),
                        'stress_level': item.get('Stress Level', None)
                    }

                    patient = Patient.objects.using(database).create(**patient_record)
                    print(f'Added {patient.name} to database {database}')

                    # delete contents of media folder
                    delete_path = Path(os.getcwd()) / 'media'

                    # Delete the contents of this path
                    delete_directory_contents(delete_path)


            # Redirect to a new URL if file is valid and saved:
            return redirect('manager_view')  # Replace 'some-view-name' with your actual view or URL name
        else:
            return HttpResponse("No file uploaded", status=400)

    return render(request, 'insights/add_multiple.html')

@require_http_methods(["GET", "POST"])
def delete(request):
    if request.method == "POST":
        # Basic fields
        patient_id = request.POST.get('patient_id')
        name = request.POST.get('name')
        gender = request.POST.get('gender')

        # Fields with comparisons
        age_comparison = request.POST.get('age_comparison', '')
        age = request.POST.get('age')
        height_comparison = request.POST.get('height_comparison', '')
        height = request.POST.get('height')
        weight_comparison = request.POST.get('weight_comparison', '')
        weight = request.POST.get('weight')

        # Building the query based on the input provided
        query = {}
        if patient_id:
            query['patient_id'] = patient_id
        if name:
            query['name__iexact'] = name
        if gender:
            query['gender__iexact'] = gender

        # Adding queries with possible comparisons
        if age:
            query[f'age__{age_comparison}' if age_comparison else 'age'] = age
        if height:
            query[f'height__{height_comparison}' if height_comparison else 'height'] = height
        if weight:
            query[f'weight__{weight_comparison}' if weight_comparison else 'weight'] = weight


        if patient_id:
        # Determining the database to use
            database = 'db2' if int(patient_id) % 2 == 0 else 'db1'
            
            # Deleting the records
            Patient.objects.using(database).filter(**query).delete()

        else:
            Patient.objects.using('db1').filter(**query).delete()
            Patient.objects.using('db2').filter(**query).delete()

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


@require_http_methods(["GET", "POST"])
def update_multiple(request):
    if request.method == "POST":
        # Constructing Q objects for filter conditions
        query = Q()

        # Gender filter
        if filter_gender := request.POST.get('filter_gender'):
            query &= Q(gender__iexact=filter_gender)

        # Age filter
        age_comparison = request.POST.get('filter_age_comparison', '')
        if age := request.POST.get('filter_age'):
            query &= Q(age__gt=age) if age_comparison == 'gt' else Q(age__lt=age) if age_comparison == 'lt' else Q(age=age)

        # Height filter
        height_comparison = request.POST.get('filter_height_comparison', '')
        if height := request.POST.get('filter_height'):
            query &= Q(height__gt=height) if height_comparison == 'gt' else Q(height__lt=height) if height_comparison == 'lt' else Q(height=height)

        # Weight filter
        weight_comparison = request.POST.get('filter_weight_comparison', '')
        if weight := request.POST.get('filter_weight'):
            query &= Q(weight__gt=weight) if weight_comparison == 'gt' else Q(weight__lt=weight) if weight_comparison == 'lt' else Q(weight=weight)

        # Update fields construction
        update_fields = {}
        if new_gender := request.POST.get('new_gender'):
            update_fields['gender'] = new_gender
        if new_blood_type := request.POST.get('new_blood_type'):
            update_fields['blood_type'] = new_blood_type
        if new_blood_pressure := request.POST.get('new_blood_pressure'):
            update_fields['blood_pressure'] = new_blood_pressure
        # Additional fields updates can be added here in the same pattern

        if not query or not update_fields:
            messages.error(request, "No valid filters or update fields provided.")
            return redirect('update_patient')

        # Applying the update
        updated_count1 = Patient.objects.using('db1').filter(query).update(**update_fields)
        updated_count2 = Patient.objects.using('db2').filter(query).update(**update_fields)
        messages.success(request, f'Updated {updated_count1 + updated_count2} patient(s).')

        return redirect('manager_view')

    return render(request, 'insights/update_multiple.html')
