from django.urls import path
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from djangoBackend.user_module.views import CreateAgencyView,CreateEmployeeView,CreateSuperSiteView, getAllData,getUser,updateUser,LoginView,signOut, verifyOTP

urlpatterns = [
    path('user/create_employee', authentication_classes([])(permission_classes([AllowAny])(CreateEmployeeView)).as_view()),
    path('user/create_agency', authentication_classes([])(permission_classes([AllowAny])(CreateAgencyView)).as_view()),
    path('user/create_supersite', CreateSuperSiteView.as_view()),
    path('user/login', authentication_classes([])(permission_classes([AllowAny])(LoginView)).as_view()),
    path('user/get_user/<str:groupId>', getUser),
    path('user/update_user/<str:groupId>', updateUser),
    path('user/logout', signOut),
    path('user/verify_otp/<str:groupId>/<str:otp>', verifyOTP),
    path('user/get_all_data', getAllData),
] 