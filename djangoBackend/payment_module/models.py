# from djangoBackend.user_module.models import Employee,RecrutingAgency,SuperSite
from datetime import datetime
from django.db import models

# Create your models here.

class Employer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    amount = models.IntegerField()
    transactionId = models.CharField(max_length=255,unique=True)  # generate it with current timestamp # eg.  server-16838437838
    paymentLink = models.CharField(max_length=255,null=True,blank=True) # Flutterwave payment link
    status = models.CharField(max_length=255,default="pending")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):  # salary of employee
    employee = models.ForeignKey("user_module.Employee",on_delete=models.CASCADE) # many to one realationship
    employer = models.ForeignKey(to=Employer,on_delete=models.CASCADE) # many to one realationship
    payment = models.OneToOneField(Payment,blank=True,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=255,default="sent")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

class Commission(models.Model):
    agency =  models.ForeignKey("user_module.RecrutingAgency",on_delete=models.CASCADE) # many to one realationship
    payment = models.OneToOneField(Payment,blank=True,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=255,default="initiated")  
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
  

