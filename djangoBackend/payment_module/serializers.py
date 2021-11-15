from rest_framework import serializers
from djangoBackend.payment_module.models import Employer,Invoice,Commission,Payment

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        exclude =["employee","employer","payment","status"]  

class InvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'         

class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        exclude =["agency","payment","status"]

class CommissionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'        

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ["transactionId","paymentLink","status"]   

class PaymentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment 
        fields = '__all__'               