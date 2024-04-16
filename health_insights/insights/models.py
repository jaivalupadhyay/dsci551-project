# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Patient(models.Model):
    patient_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=20, null=True)
    height = models.FloatField(help_text='Height in Inches', null=True)
    weight = models.FloatField(help_text='Weight in pounds', null=True)
    blood_type =  models.CharField(max_length=10, null=True)
    blood_pressure = models.FloatField(null=True)
    oxygen_level = models.FloatField(null=True)
    heart_rate = models.FloatField(default=0)  # Assuming 0 as default for heart rate
    blood_sugar = models.FloatField(null=True)
    cholesterol = models.FloatField(default=0)  # Assuming 0 as default for cholesterol
    body_temperature = models.FloatField(null=True)
    bmi = models.FloatField(null=True)
    sleep_hours = models.FloatField(null=True)
    stress_level = models.FloatField(null=True)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.patient_id


class File(models.Model):
    file = models.FileField()