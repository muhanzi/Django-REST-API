from djangoBackend.utils.sendSMS import SMS
from djangoBackend.payment_module.models import Commission, Employer, Invoice, Payment
from djangoBackend.user_module.models import Employee, RecrutingAgency, SuperSite
from djangoBackend.user_module.serializers import EmployeeDataSerializer, EmployeeSerializer, RecrutingAgencyDataSerializer, RecrutingAgencySerializer, SuperSiteDataSerializer, SuperSiteSerializer, UserDataSerializer, UserSerializer
from djangoBackend.payment_module.serializers import CommissionDataSerializer, CommissionSerializer, EmployerSerializer, InvoiceDataSerializer, InvoiceSerializer, PaymentDataSerializer, PaymentSerializer

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from djangoBackend.utils.exceptionHandlers import custom_exception_handler, CustomAPIException
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
import random


class CreateEmployeeView(GenericAPIView):

    res = openapi.Response("create Employee", EmployeeSerializer)

    @swagger_auto_schema(request_body=EmployeeSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):
        data = request.data
        serializerEmployee = EmployeeSerializer(data=data)

        if not serializerEmployee.is_valid():
            raise CustomAPIException(
                serializerEmployee.errors, status.HTTP_400_BAD_REQUEST)
        elif not "username" in data or not "password" in data or not "email" in data:
            return Response(send_response(False, "username or password or email is missing", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            if not User.objects.filter(username=data["username"]).exists():
                user = User.objects.create_user(
                    username=data["username"], password=data["password"], email=data["email"],first_name=data["first_name"],last_name=data["last_name"], is_staff=False, is_superuser=False)
                # add user to employee group
                groupInstance = Group.objects.get(name='employee')
                groupInstance.user_set.add(user)

                serializerEmployee.save(user=User.objects.get(id=user.id))
                
                # Employee.objects.create(
                #     first_name=data["first_name"], last_name=data["last_name"], user=User.objects.get(id=user.id),phoneNumber=data["phoneNumber"])
                
                # signIn the user
                signedInUser = authenticate(
                    username=data["username"], password=data["password"])
                login(request, signedInUser)  # starts a session on the server
                # generate token
                token = Token.objects.create(user=signedInUser)

                current_users = User.objects.filter(id=user.id)
                current_user_data = [UserDataSerializer(
                    userInstance).data for userInstance in current_users][0]
                #  current_user_data  --> has groups and permissions     
                # remove password field from data # should not return password to the frontend
                del current_user_data["password"]    
                groupId = groupInstance.pk
                userId = user.id
                current_user_data["user_group_data"] = getUserGroupData(groupId,userId)

                # OTP
                if "type" in current_user_data["user_group_data"]:
                    if (sendOTP(groupId,userId)):
                        return Response(send_response(True, "Employee Created successfully", {"token": token.key, "user_data": current_user_data}), status=status.HTTP_200_OK)
                    else:
                        # TODO: delete the user // in case it wasn't fully successful
                        return Response(send_response(False, "Failed to send OTP", {}), status=status.HTTP_400_BAD_REQUEST)    
                else:
                    return Response(send_response(False, "Failed to get user group data", {}), status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(send_response(False, "username already exist, choose a different one", {}), status=status.HTTP_400_BAD_REQUEST)


class CreateAgencyView(GenericAPIView):
    res = openapi.Response("create Agency", RecrutingAgencySerializer)

    @swagger_auto_schema(request_body=RecrutingAgencySerializer, responses={200: res})
    def post(self, request, *args, **kwargs):
        data = request.data
        serializerAgency = RecrutingAgencySerializer(data=data)

        if not serializerAgency.is_valid():
            raise CustomAPIException(
                serializerAgency.errors, status.HTTP_400_BAD_REQUEST)
        elif not "username" in data or not "password" in data or not "email" in data:
            return Response(send_response(False, "username or password or email is missing", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            if not User.objects.filter(username=data["username"]).exists():
                user = User.objects.create_user(
                    username=data["username"], password=data["password"], email=data["email"], is_staff=False, is_superuser=False)
                # add user to agency group
                groupInstance = Group.objects.get(name='agency')
                groupInstance.user_set.add(user)

                serializerAgency.save(user=User.objects.get(id=user.id))
                
                # RecrutingAgency.objects.create(
                #     name=data["name"], user=User.objects.get(id=user.id),phoneNumber=data["phoneNumber"])
                
                # signIn the user
                signedInUser = authenticate(
                    username=data["username"], password=data["password"])
                login(request, signedInUser)  # starts a session on the server
                # generate token
                token = Token.objects.create(user=signedInUser)

                current_users = User.objects.filter(id=user.id)
                current_user_data = [UserDataSerializer(
                    userInstance).data for userInstance in current_users][0]
                #  current_user_data  --> has groups and permissions  
                # remove password field from data # should not return password to the frontend
                del current_user_data["password"]    
                groupId = groupInstance.pk
                userId = user.id
                current_user_data["user_group_data"] = getUserGroupData(groupId,userId)

                # OTP
                if "type" in current_user_data["user_group_data"]:
                    if (sendOTP(groupId,userId)):
                        return Response(send_response(True, "Recruiting Agency Created successfully", {"token": token.key, "user_data": current_user_data}), status=status.HTTP_200_OK)
                    else:
                        return Response(send_response(False, "Failed to send OTP", {}), status=status.HTTP_400_BAD_REQUEST)    
                else:
                    return Response(send_response(False, "Failed to get user group data", {}), status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(send_response(False, "username already exist, choose a different one", {}), status=status.HTTP_400_BAD_REQUEST)


class CreateSuperSiteView(GenericAPIView):
    res = openapi.Response("create SuperSite", SuperSiteSerializer)

    @swagger_auto_schema(request_body=SuperSiteSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):

        # request.user.userId # user id of the current logged in user
        logged_in_user = User.objects.get(id=request.user.userId)
        if not User.has_perm(logged_in_user,perm="Can add super site") :
            return Response(send_response(False, "you do not have permission to perform this action", {}), status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializerSupersite = SuperSiteSerializer(data=data)

        if not serializerSupersite.is_valid():
            raise CustomAPIException(
                serializerSupersite.errors, status.HTTP_400_BAD_REQUEST)
        elif not "username" in data or not "password" in data or not "email" in data:
            return Response(send_response(False, "username or password or email is missing", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            if not User.objects.filter(username=data["username"]).exists():
                user = User.objects.create_user(
                    username=data["username"], password=data["password"], email=data["email"], is_staff=True, is_superuser=True)
                # add user to supersite group
                groupInstance = Group.objects.get(name='supersite')
                groupInstance.user_set.add(user)

                serializerSupersite.save(user=User.objects.get(id=user.id))
                
                # SuperSite.objects.create(
                #     name=data["name"], user=User.objects.get(id=user.id),phoneNumber=data["phoneNumber"])
                # token for this created supersite will be generated when they login 

                return Response(send_response(True, "SuperSite Created successfully", {"name": data["name"], "is_staff": True,"is_superuser":True}), status=status.HTTP_200_OK)
            else:
                return Response(send_response(False, "username already exist, choose a different one", {}), status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):

    res = openapi.Response("user login", UserSerializer)

    @swagger_auto_schema(request_body=UserSerializer, responses={200: res})
    def post(self, request, *args, **kwargs):

        data = request.data
        user = authenticate(
            username=data["username"], password=data["password"])
        if user is not None and user.check_password(data["password"]):
            # A backend authenticated the credentials # user was found
            # creates a session on the server with current userId and backend used to authenticate the user
            login(request, user)
            # generate JWT token # if user logged out, the previous token was deleted # a new token for the user is created
            token = Token.objects.get_or_create(user=user)
            print("token: "+str(token))
            current_users = User.objects.filter(username=user.get_username())
            current_user_data = [UserDataSerializer(
                userInstance).data for userInstance in current_users][0]
            # remove password field from data # should not return password to the frontend
            del current_user_data["password"]    
            # user groups and permissions are part of the data
            groupId = current_user_data["groups"][0]
            userId = current_user_data["id"]
            current_user_data["user_group_data"] = getUserGroupData(groupId,userId)

            # OTP
            if "type" in current_user_data["user_group_data"]:
                if (sendOTP(groupId,userId)):
                    return Response(send_response(True, "user signed in successfully", {"token": str(token[0]), "user_data": current_user_data}), status=status.HTTP_200_OK)
                else:
                    return Response(send_response(False, "Failed to send OTP", {}), status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response(send_response(False, "Failed to get user group data", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            # No backend authenticated the credentials # user does not exist
            return Response(send_response(False, "invalid user credentials", {}), status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@swagger_auto_schema(RequestField="groupId")
def getUser(request, *args, **kwargs):
    if "groupId" in kwargs and kwargs["groupId"] != None:
        # request.user.is_authenticated  # is user logged in ?
        # request.user.userId # user id of the current logged in user
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "groupId is required", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@swagger_auto_schema(RequestField="groupId")
def updateUser(request, *args, **kwargs):
    if "groupId" in kwargs and kwargs["groupId"] != None:
        return Response(send_response(True, "message here", {}), status=status.HTTP_200_OK)
    else:
        return Response(send_response(False, "groupId is required", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@swagger_auto_schema(RequestField="otp")
def verifyOTP(request, *args, **kwargs):
    if not "otp" in kwargs or kwargs["otp"] == None:
        return Response(send_response(False, "otp is required", {}), status=status.HTTP_400_BAD_REQUEST)

    if not "groupId" in kwargs or kwargs["groupId"] == None:
        return Response(send_response(False, "groupId is required", {}), status=status.HTTP_400_BAD_REQUEST)

    groupId = int(kwargs["groupId"])
    otp = kwargs["otp"]
    userId = request.user.userId

    if groupId == 1:
        # agency
        agencies = RecrutingAgency.objects.filter(user=userId)
        if agencies.count() > 0:
            agency = [RecrutingAgencyDataSerializer(
                agencyInstance).data for agencyInstance in agencies][0]
            if otp == agency["otp"]:
                return Response(send_response(True, "Phone number verified successfuly", {}), status=status.HTTP_200_OK)
            else:
                return Response(send_response(False, "The code you entered is incorrect", {}), status=status.HTTP_400_BAD_REQUEST)      
        else:
            return Response(send_response(False, "Failed to verify your phone number", {}), status=status.HTTP_400_BAD_REQUEST)     
    elif groupId == 2:
        # employee
        employees = Employee.objects.filter(user=userId)
        if employees.count() > 0:
            employee = [EmployeeDataSerializer(
                employeeInstance).data for employeeInstance in employees][0]
            if otp == employee["otp"]:
                return Response(send_response(True, "Phone number verified successfuly", {}), status=status.HTTP_200_OK)
            else:
                return Response(send_response(False, "The code you entered is incorrect", {}), status=status.HTTP_400_BAD_REQUEST)      
        else:
            return Response(send_response(False, "Failed to verify your phone number", {}), status=status.HTTP_400_BAD_REQUEST)     
    elif groupId == 3:
        # supersite
        supersites = SuperSite.objects.filter(user=userId)
        if supersites.count() > 0:
            supersite = [SuperSiteDataSerializer(
                supersiteInstance).data for supersiteInstance in supersites][0]
            if otp == supersite["otp"]:
                return Response(send_response(True, "Phone number verified successfuly", {}), status=status.HTTP_200_OK)
            else:
                return Response(send_response(False, "The code you entered is incorrect", {}), status=status.HTTP_400_BAD_REQUEST)      
        else:
            return Response(send_response(False, "Failed to verify your phone number", {}), status=status.HTTP_400_BAD_REQUEST)         
    else:
        return Response(send_response(False, "Failed to verify your phone number", {}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@swagger_auto_schema()
def signOut(request, *args, **kwargs):
    # request.user.is_authenticated  # is user logged in ?
    # request.user.userId # user id of the current logged in user
    Token.objects.filter(user_id=request.user.userId).delete()
    # Remove the authenticated user's ID from the request and flush their session data.
    logout(request)
    return Response(send_response(True, "successfuly signed out", {}), status=status.HTTP_200_OK)


def getUserGroupData(groupId, userId) :
    user_group_data = {}
    if groupId == 1:
        # agency
        agencies = RecrutingAgency.objects.filter(user=userId)
        if agencies.count() > 0:
            agency = [RecrutingAgencyDataSerializer(
                agencyInstance).data for agencyInstance in agencies][0]
            agency["type"] = "agency"
            user_group_data = agency
    elif groupId == 2:
        # employee
        employees = Employee.objects.filter(user=userId)
        if employees.count() > 0:
            employee = [EmployeeDataSerializer(
                employeeInstance).data for employeeInstance in employees][0]
            employee["type"] = "employee"
            user_group_data = employee
    elif groupId == 3:
        # supersite
        supersites = SuperSite.objects.filter(user=userId)
        if supersites.count() > 0:
            supersite = [SuperSiteDataSerializer(
                supersiteInstance).data for supersiteInstance in supersites][0]
            supersite["type"] = "supersite"
            user_group_data = supersite

    if "otp" in user_group_data:
        # remove otp field from data
        del user_group_data["otp"]

    return user_group_data    

def sendOTP(groupId,userId) :
    success = False
    # generate OTP for the user 
    otp = generateOTP()
    phoneNumber = ""
    message = f"{otp} is your verification code to access the server."
    # print("============ OTP: "+otp+" ===================")
    # save OTP
    if groupId == 1:
        # agency
        agency = RecrutingAgency.objects.filter(user=userId)
        agency.update(otp=otp)
        phoneNumber = [RecrutingAgencySerializer(
                    agencyInstance).data for agencyInstance in agency][0]["phoneNumber"]
    elif groupId == 2:
        # employee
        employee = Employee.objects.filter(user=userId)
        employee.update(otp=otp)
        phoneNumber = [EmployeeSerializer(
                    employeeInstance).data for employeeInstance in employee][0]["phoneNumber"]
    elif groupId == 3:
        # supersite
        supersite = SuperSite.objects.filter(user=userId)
        supersite.update(otp=otp)  
        phoneNumber = [SuperSiteSerializer(
                    supersiteInstance).data for supersiteInstance in supersite][0]["phoneNumber"]

    # use Africastalking to send OTP via SMS 
    # sms = SMS()
    # sentSMSResults = sms.send(recipients=[phoneNumber],message=message)
    # if(sentSMSResults):
    #     success = True 

    success =True  # for development // to save sms costs

    return success      

def generateOTP() :
    otp = ""
    for i in range(4) : 
        otp += str(random.randint(0,9))    
    return otp    

def send_response(success, message, data):
    return {"success": success, "message": message, "data": data}

@api_view(['GET'])
@swagger_auto_schema()
def getAllData(request, *args, **kwargs):

    logged_in_user = User.objects.get(id=request.user.userId)
    if not logged_in_user.is_superuser :
        return Response(send_response(False, "you do not have permission to perform this action", {}), status=status.HTTP_403_FORBIDDEN)

    employees = [EmployeeDataSerializer(emloyeeInstance).data for emloyeeInstance in Employee.objects.all()] 
    agencies = [RecrutingAgencyDataSerializer(agencyInstance).data for agencyInstance in RecrutingAgency.objects.all()] 
    commissions = [CommissionDataSerializer(commissionInstance).data for commissionInstance in Commission.objects.all()]  
    invoices = [InvoiceDataSerializer(invoiceInstance).data for invoiceInstance in Invoice.objects.all()]  
    employers = [EmployerSerializer(employerInstance).data for employerInstance in Employer.objects.all()] 
    payments = [PaymentDataSerializer(paymentInstance).data for paymentInstance in Payment.objects.all()] 

    responseData = {
        "employees":employees,
        "agencies":agencies,
        "commissions":commissions,
        "invoices":invoices,
        "employers":employers,
        "payments":payments
    }

    return Response(send_response(True, "successful", responseData), status=status.HTTP_200_OK)    
