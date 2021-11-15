from django.contrib import admin
from djangoBackend.payment_module.models import Invoice,Commission,Payment,Employer


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id','employee','employer','payment','createdAt','updatedAt')

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('id','agency','payment','createdAt','updatedAt')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','amount','transactionId','createdAt','updatedAt')

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','createdAt','updatedAt')    

# Register your models here.
admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(Commission,CommissionAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Employer,EmployerAdmin)