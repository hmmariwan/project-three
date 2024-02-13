from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee,Timesheet,CustomUser,ContactFile,Jobs

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    
    ordering = ('email',)

    list_display = ('first_name','last_name','email', 'is_staff', 'is_active', 'is_employee', 'is_employer',)
    
    search_fields = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_employee', 'is_employer')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_employee', 'is_employer'),
        }),
    )

class EmployeeAdmin(admin.ModelAdmin):
    list_display=('id','fname','lname','email','ni','tcode','pension','student_loan')

class TimesheetAdmin(admin.ModelAdmin):
    list_display=('eid','mon','tue','wed','thu','fri','sat','sun','npr','opr')

class ContactFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'contact_name', 'contact_email','contact_message']

    def contact_name(self, object):
        return object.contact.name
    
    def contact_email(self, object):
        return object.contact.email
    
    def contact_message(self, object):
        return object.contact.message
    
class JobsAdmin(admin.ModelAdmin):
    list_display=('reference','title','duration','type','rate','location','description')


admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Timesheet,TimesheetAdmin)
admin.site.register(ContactFile,ContactFileAdmin)
admin.site.register(Jobs,JobsAdmin)


