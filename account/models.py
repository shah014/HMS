from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


departments = [('Cardiologist', 'Cardiologist'),
               ('Dermatologists', 'Dermatologists'),
               ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
               ('Allergists/Immunologists', 'Allergists/Immunologists'),
               ('Anesthesiologists', 'Anesthesiologists'),
               ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
               ]


class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=40, null=True)
    contact = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=40, null=True)
    department = models.CharField(max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField(default=False)
    profile_pic = models.ImageField(null=True, default="original.jpg", blank=True)

    def __str__(self):
        return str(self.name)


class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=40)
    age = models.PositiveIntegerField(null=True)
    bloodGroup = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=30, null=True)
    contact = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctor = models.CharField(max_length=100, null=True)
    Created_at = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    profile_pic = models.ImageField(null=True, default="original.jpg", blank=True)

    def __str__(self):
        return str(self.name)


class Appointment(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Discharged', 'Discharged'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    appointDate = models.DateField(auto_now_add=False, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.patient) + " " + "has appointment with Dr."+" " + str(self.doctor)
