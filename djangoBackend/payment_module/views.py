from djangoBackend.user_module.serializers import EmployeeDataSerializer
from django.contrib.auth.models import User
from djangoBackend.user_module.models import Employee, RecrutingAgency
from djangoBackend.settings import FLUTTERWAVE
from datetime import datetime

import requests
from djangoBackend.payment_module.models import Commission, Employer, Invoice, Payment
from djangoBackend.payment_module.serializers import CommissionDataSerializer, CommissionSerializer, EmployerSerializer, InvoiceDataSerializer, InvoiceSerializer, PaymentDataSerializer, PaymentSerializer

# Create your views here.

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from django.conf import settings
from djangoBackend.utils.exceptionHandlers import custom_exception_handler, CustomAPIException
from rest_framework.decorators import api_view
from rest_framework import viewsets
import pytz


EATZ = pytz.timezone('Africa/Kampala')
FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE["SECRET_KEY"]
FLUTTERWAVE_CREATE_PAYMENT = settings.FLUTTERWAVE["CREATE_PAYMENT"]
FLUTTERWAVE_MAKE_TRANSFER = settings.FLUTTERWAVE["MAKE_TRANSFER"]
FLUTTERWAVE_PAYMENT_LOGO = settings.FLUTTERWAVE["PAYMENT_LOGO"]
FLUTTERWAVE_REDIRECT_URL = settings.FLUTTERWAVE["REDIRECT_URL"]
FLUTTERWAVE_CALLBACK_URL = settings.FLUTTERWAVE["CALLBACK_URL"]


class PayView(GenericAPIView):

    res = openapi.Response("create Payment", PaymentSerializer)

    @swagger_auto_schema(request_body=PaymentSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):

        data = request.data
        serializerPayment = PaymentSerializer(data=data)

        if not serializerPayment.is_valid():
            raise CustomAPIException(
                serializerPayment.errors, status.HTTP_400_BAD_REQUEST)

        serializerPayment.save()

        return Response(send_response(True, "Payment created successfuly", {}), status=status.HTTP_200_OK)

# fields amount,employer,employee


class CreateInvoiceView(GenericAPIView):
    res = openapi.Response("create Invoice", InvoiceSerializer)

    @swagger_auto_schema(request_body=InvoiceSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):

        data = request.data
        serializerPayment = PaymentSerializer(data=data)

        if not serializerPayment.is_valid():
            raise CustomAPIException(
                serializerPayment.errors, status.HTTP_400_BAD_REQUEST)
        elif not "employer" in data or not "employee" in data:
            return Response(send_response(False, "employer or employee is missing", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            transactionId = f"server-{int(datetime.now(EATZ).timestamp())}"
            paymentInstance = serializerPayment.save(
                transactionId=transactionId)
            # get employer data
            employers = Employer.objects.filter(id=data['employer'])
            employerData = [EmployerSerializer(
                employerInstance).data for employerInstance in employers][0]
            # create payment in Flutterwave
            payload = {
                "tx_ref": transactionId,
                "amount": str(data['amount']),
                "currency": "UGX",
                "redirect_url": FLUTTERWAVE_REDIRECT_URL,
                "payment_options": ["card", "banktransfer", "mobilemoneyuganda", "mobilemoneyrwanda", "mobilemoneytanzania", "mpesa", "account"],
                "customer": {
                    "email": employerData['email'],
                    "phonenumber": employerData['phoneNumber'],
                    "name": employerData['name']
                },
                "customizations": {
                    "title": "Backend Server",
                    "description": "Complete invoice payment",
                    "logo": FLUTTERWAVE_PAYMENT_LOGO
                }
            }
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
            }
            results = flutterwavePostRequest(
                url=FLUTTERWAVE_CREATE_PAYMENT, headers=headers, data=payload)
            payment = Payment.objects.filter(id=paymentInstance.id)
            if not results['success']:
                payment.delete()
                return Response(send_response(False, results['message'], {}), status=status.HTTP_400_BAD_REQUEST)
            link = results['data']['data']['link']
            payment.update(paymentLink=link, status="pending")
            employee = Employee.objects.get(id=data['employee'])
            employer = Employer.objects.get(id=data['employer'])

            Invoice.objects.create(employer=employer, employee=employee,
                                   payment=paymentInstance, amount=data['amount'], status='sent')

            # TODO: send invoice (html template with flutterwave link) to employer via email

            return Response(send_response(True, "Invoice was successfuly created", {"flutterwave": results['data']}), status=status.HTTP_200_OK)


class CreateCommissionView(GenericAPIView):
    res = openapi.Response("create Commission", CommissionSerializer)

    @swagger_auto_schema(request_body=CommissionSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):

        data = request.data
        serializerPayment = PaymentSerializer(data=data)

        if not serializerPayment.is_valid():
            raise CustomAPIException(
                serializerPayment.errors, status.HTTP_400_BAD_REQUEST)
        elif not "agency" in data:
            return Response(send_response(False, "agency is missing", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            transactionId = f"server-{int(datetime.now(EATZ).timestamp())}"
            paymentInstance = serializerPayment.save(
                transactionId=transactionId, status="pending")
            agency = RecrutingAgency.objects.get(id=data['agency'])

            commissionInstance = Commission.objects.create(
                agency=agency, payment=paymentInstance, status="initiated")

            commissions = Commission.objects.filter(id=commissionInstance.id)
            commissionData = [CommissionDataSerializer(
                commissionInstance).data for commissionInstance in commissions][0]

            return Response(send_response(True, "Commission initiated successfuly", commissionData), status=status.HTTP_200_OK)


class CreateEmployerView(GenericAPIView):
    res = openapi.Response("create Employer", EmployerSerializer)

    @swagger_auto_schema(request_body=EmployerSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):

        data = request.data
        serializerEmployer = EmployerSerializer(data=data)

        if not serializerEmployer.is_valid():
            raise CustomAPIException(
                serializerEmployer.errors, status.HTTP_400_BAD_REQUEST)

        employerInstance = serializerEmployer.save()

        employers = Employer.objects.filter(id=employerInstance.id)
        employerData = [EmployerSerializer(
            instance).data for instance in employers][0]

        return Response(send_response(True, "Employer created successfuly", employerData), status=status.HTTP_200_OK)


@api_view(['GET'])
@swagger_auto_schema(RequestField="id")
def withdrawInvoice(request, *args, **kwargs):
    # TODO: employee withdraws salary # Flutterwave transfer
    if not "id" in kwargs or kwargs["id"] == None:
        return Response(send_response(False, "id is required", {}), status=status.HTTP_400_BAD_REQUEST)
    if not "mode" in kwargs or kwargs["mode"] == None:
        return Response(send_response(False, "withdraw mode is required", {}), status=status.HTTP_400_BAD_REQUEST)

    logged_in_user = User.objects.get(id=request.user.userId)

    try:
        employee = Employee.objects.get(user=logged_in_user)
    except Employee.DoesNotExist as ex:
        print(str(ex))
        return Response(send_response(False, "You are not authorized to withdraw any invoice", {}), status=status.HTTP_400_BAD_REQUEST)

    invoices = Invoice.objects.filter(id=kwargs["id"], employee=employee)

    if invoices.count() < 1:
        return Response(send_response(False, "This invoice does not match this Employee", {}), status=status.HTTP_400_BAD_REQUEST)

    invoiceData = [InvoiceDataSerializer(
        instance).data for instance in invoices][0]

    employees = Employee.objects.filter(user=logged_in_user)
    employeeData = [EmployeeDataSerializer(
        instance).data for instance in employees][0]

    payments = Payment.objects.filter(transactionId=invoiceData['payment'])
    paymentData = [PaymentDataSerializer(
        instance).data for instance in payments][0]

    bankName = ''
    bankAccountNumber = ''

    if kwargs["mode"] == "mobile":
        bankName = 'MPS'
        bankAccountNumber = employeeData['phoneNumber']
    elif kwargs["mode"] == "bank":
        bankName = employeeData['bankName']
        bankAccountNumber = employeeData['bankAccountNumber']

    # make Flutterwave transfer
    payload = {
        "account_bank": bankName,
        "account_number": bankAccountNumber,
        "amount": paymentData['amount'],
        "beneficiary_name": f"{employeeData['first_name']} {employeeData['last_name']}",
        "narration": "Initiate withdraw",
        "currency": "UGX",
        "reference": paymentData['transactionId'],
        "callback_url": f"{FLUTTERWAVE_CALLBACK_URL}{paymentData['transactionId']}",
        "debit_currency": "UGX"
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
    }
    results = flutterwavePostRequest(
        url=FLUTTERWAVE_MAKE_TRANSFER, headers=headers, data=payload)
    if not results['success']:
        return Response(send_response(False, results['message'], {}), status=status.HTTP_400_BAD_REQUEST)

    fullName = results['data']['data']['full_name']
    flutterwaveStatus = results['data']['data']['status']  # --> 'NEW'

    payment = Payment.objects.filter(id=paymentData['id'])
    payment.update(status="Withdraw Queued")

    return Response(send_response(True, "withdraw Invoice was successfuly initiated", {"flutterwave": results['data']}), status=status.HTTP_200_OK)


@api_view(['GET'])
@swagger_auto_schema(RequestField="id")
def withdrawCommission(request, *args, **kwargs):
    # TODO: agency withdraws commission # Flutterwave transfer
    if "id" in kwargs and kwargs["id"] != None:
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "id is required", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@swagger_auto_schema(RequestField="id")
def getPayment(request, *args, **kwargs):
    if "id" in kwargs and kwargs["id"] != None:
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "id is required", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@swagger_auto_schema(RequestField="id")
def getInvoice(request, *args, **kwargs):
    if "id" in kwargs and kwargs["id"] != None:
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "id is required", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@swagger_auto_schema(RequestField="id")
def getCommission(request, *args, **kwargs):
    if "id" in kwargs and kwargs["id"] != None:
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "id is required", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@swagger_auto_schema(RequestField="id")
def updatePayment(request, *args, **kwargs):
    if "id" in kwargs and kwargs["id"] != None:
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "id is required", {}), status=status.HTTP_400_BAD_REQUEST)


def send_response(success, message, data):
    return {"success": success, "message": message, "data": data}


class InvoicesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed.
    """
    queryset = Invoice.objects.all().order_by('createdAt')
    serializer_class = InvoiceSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CommissionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commissions to be viewed.
    """
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    # permission_classes = [permissions.IsAuthenticated]


def flutterwavePostRequest(url, headers, data):
    try:
        r = requests.post(url, headers=headers, data=json.dumps(data))
        status_code = r.status_code
        response_body = r.json()
        if status_code == 200:
            return {"success": True, "status": status_code, "message": response_body['message'], "data": response_body}
        else:
            return {"success": False, "status": status_code, "message": response_body['message'], "data": response_body}
    except Exception as e:
        print(str(e))
        return {"success": False, "message": str(e)}
