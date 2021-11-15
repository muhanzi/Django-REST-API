from datetime import datetime
from django.contrib.auth.models import User
# from djangoBackend.payment_module.models import Employer
from django.db import models
from django.db.models.fields import DateField

# Create your models here.

class RecrutingAgency(models.Model):
    name = models.CharField(max_length=255)
    otp = models.CharField(blank=True,null=True,max_length=4)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    village = models.CharField(max_length=255,null=True,blank=True)
    nin = models.CharField(max_length=255,null=True,blank=True) 
    bankName = models.CharField(max_length=255,null=True,blank=True)
    bankAccountNumber = models.CharField(max_length=255,null=True,blank=True)
    dateOfBirth = DateField(null=True)
    profilePicture = models.CharField(max_length=255,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    employer = models.ForeignKey("payment_module.Employer",on_delete=models.SET_NULL,blank=True,null=True)
    agency = models.ForeignKey(to=RecrutingAgency,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    otp = models.CharField(blank=True,null=True,max_length=4)
    phoneNumber = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    district = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    village = models.CharField(max_length=255,null=True,blank=True)
    dateOfBirth = DateField(null=True)
    parentGuardian = models.CharField(max_length=255,null=True,blank=True)
    lc1Name = models.CharField(max_length=255,null=True,blank=True)
    bioData = models.CharField(max_length=255,null=True,blank=True)
    profilePicture = models.CharField(max_length=255,null=True,blank=True)
    bankName = models.CharField(max_length=255,null=True,blank=True)
    bankAccountNumber = models.CharField(max_length=255,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

class SuperSite(models.Model):
    name = models.CharField(max_length=255)  
    otp = models.CharField(blank=True,null=True,max_length=4)
    phoneNumber = models.CharField(max_length=255,blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profilePicture = models.CharField(max_length=255,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)      
