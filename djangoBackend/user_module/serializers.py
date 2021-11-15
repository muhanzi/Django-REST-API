from rest_framework import serializers
from rest_framework.authtoken.models import Token
from djangoBackend.user_module.models import Employee,RecrutingAgency,SuperSite
from django.contrib.auth.models import User

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['employer','user','otp','profilePicture']

class EmployeeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  

class RecrutingAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecrutingAgency
        exclude = ['otp','user','profilePicture']

class RecrutingAgencyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecrutingAgency
        fields = '__all__'         

class SuperSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperSite
        exclude = ['otp','user','profilePicture']

class SuperSiteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperSite
        fields = '__all__'           

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["username","password"]   

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'  

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'                      