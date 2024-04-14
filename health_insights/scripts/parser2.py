import json
from django.conf import settings
from insights.models import Patient
from pymongo import MongoClient
from datetime import datetime

# Function to convert Excel serial date to Python datetime
def excel_to_datetime(excel_date_num):
    return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date_num) - 2)

def run():
    """
    Imports data from a JSON file into the Patient model, routing to db1 or db2 based on patient_id.
    """
    Patient.objects.using('db1').delete()
    Patient.objects.using('db2').delete()
    with open("dataset.json", 'r') as file:
        data = json.load(file)['Sheet1'] 

        for item in data[:11]:
            patient_id = item['Patient ID']
            
            database = 'db2' if int(patient_id) % 2 == 0 else 'db1'

            Patient.objects.using(database).filter(patient_id=patient_id).delete()
            
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
                'cholesterol': item.get('Cholesterol', 0),  # Corrected field name spelling
                'body_temperature': item.get('Body Temperature', None),  # Corrected field name spelling
                'sleep_hours': item.get('Sleep Hours', None),
                'bmi': item.get('BMI', None),
                'stress_level': item.get('Stress Level', None)
            }

            # Create a new patient record in the designated database

          
            patient = Patient.objects.using(database).create(**patient_record)
            print(f'Added {patient.name} to database {database}')

# Note: Ensure the 'Patient' model and the JSON file's keys match exactly with the model fields.
