from django.contrib import admin
from djangoBackend.user_module.models import Employee,RecrutingAgency,SuperSite


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','user','phoneNumber','agency','employer','otp','createdAt','updatedAt')

class RecrutingAgencyAdmin(admin.ModelAdmin):
    list_display = ('id','name','user','otp','phoneNumber','createdAt','updatedAt')

class SuperSiteAdmin(admin.ModelAdmin):
    list_display = ('id','name','user','otp','phoneNumber','createdAt','updatedAt')

# Register your models here.
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(RecrutingAgency,RecrutingAgencyAdmin)
admin.site.register(SuperSite,SuperSiteAdmin)
