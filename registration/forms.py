from django import forms
from .models import Employee,Timesheet,Contact,CustomUser,Jobs
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_employee', 'is_employer')

class EmployeeSignUpForm(CustomUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','mobile','email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            # Using string formatting to include the email in the error message
            message = _("The email '{email}' has already been registered. Please change the email and try again.").format(email=email)
            raise ValidationError(message, code='email_exists')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
        return user

class EmployerSignUpForm(CustomUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','mobile','email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            # Using string formatting to include the email in the error message
            message = _("The email '{email}' has already been registered. Please use a different email.").format(email=email)
            raise ValidationError(message, code='email_exists')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class SetNewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Please enter correct email and password."
        ),
        'inactive': ("This account is inactive."),
    }


class EmployeeForm(forms.ModelForm):

    id=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'only numbers'}),label='ID')
    dbirth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')

    class Meta:
        model=Employee
        fields= '__all__'

    #removing the mandatory of tcode
    def __init__(self,*args,**kwargs):
        super(EmployeeForm,self).__init__(*args,**kwargs)
        self.fields['tcode'].required=False

class TimesheetForm(forms.ModelForm):
    class Meta:
        model=Timesheet
        fields=('eid','mon','tue','wed','thu','fri','sat','sun','npr','opr','date')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class CandidateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','mobile','email','photo','cv')

    photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['photo'].widget = forms.ClearableFileInput(attrs={'multiple': False, 'class': 'custom-file-input'})
        self.fields['cv'].widget = forms.ClearableFileInput(attrs={'multiple': False, 'class': 'custom-file-input'})

class PaySlipAccessForm(forms.Form):
    email = forms.EmailField()
    dbirth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label='Date of Birth')


class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = '__all__'

class ApplyJobForm(forms.Form):
    firstName = forms.CharField(label='First Name')
    lastName = forms.CharField(label='Last Name')
    mobile = forms.IntegerField()  # Assuming mobile is a numeric input
    email = forms.EmailField()
    cv = forms.FileField(label='CV')

    # hidding fields for job_title and job_reference 
    job_title = forms.CharField(widget=forms.HiddenInput())
    job_reference = forms.CharField(widget=forms.HiddenInput())


        

    