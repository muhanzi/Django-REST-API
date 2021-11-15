from django.urls import path,include
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from djangoBackend.payment_module.views import CreateCommissionView,CreateInvoiceView,CreateEmployerView,PayView,getCommission,getInvoice,getPayment,updatePayment,withdrawInvoice,withdrawCommission
from rest_framework import routers
from djangoBackend.payment_module.views import InvoicesViewSet,CommissionsViewSet

router = routers.DefaultRouter()
router.register(r'invoices', InvoicesViewSet)
router.register(r'commissions', CommissionsViewSet)

urlpatterns = [
    path('payment/pay', PayView.as_view()),
    path('payment/create_invoice', CreateInvoiceView.as_view()),
    path('payment/create_commission', CreateCommissionView.as_view()),
    path('payment/create_employer', CreateEmployerView.as_view()),
    path('payment/withdraw_invoice/<str:id>/<str:mode>', withdrawInvoice),
    path('payment/withdraw_commission/<str:id>/<str:mode>', withdrawCommission),
    path('payment/get_payment/<str:id>', getPayment),
    path('payment/get_invoice/<str:id>', getInvoice),
    path('payment/get_commission/<str:id>', getCommission),
    path('payment/update_payment/<str:id>', updatePayment),
    path('', include(router.urls)),
] 