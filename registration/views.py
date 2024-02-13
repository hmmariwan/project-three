from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
import string
from django.core.paginator import Paginator
from django.core.mail import EmailMessage,send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.views import PasswordResetCompleteView,PasswordResetDoneView,LoginView
from .forms import (EmployeeForm,ContactForm,TimesheetForm,EmployeeSignUpForm,EmployerSignUpForm,PaySlipAccessForm,
                    CustomAuthenticationForm,PasswordResetRequestForm,SetNewPasswordForm,
                    JobsForm,CandidateForm,ApplyJobForm)
from .models import Employee,Timesheet,ContactFile,CustomUser,PasswordReset,Jobs
from django.http import Http404
import os
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import CreateView
from django.utils.timezone import now, timedelta
from django.contrib.auth import logout
from reportlab.pdfgen import canvas

def home(request):
    return render (request,'registration/home.html')

class EmployeeSignUpView(CreateView):
    form_class = EmployeeSignUpForm
    template_name = 'registration/employee_signup.html'
    success_url = reverse_lazy('employee_login')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully signed up as an employee!')
        return super().form_valid(form)

class EmployerSignUpView(CreateView):
    form_class = EmployerSignUpForm
    template_name = 'registration/employer_signup.html'
    success_url = reverse_lazy('employer_login')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully signed up as an employer!')
        return super().form_valid(form)

class EmployeeLoginView(LoginView):
    template_name = 'registration/employee_login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = False

    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser or not user.is_employee:
            return super().form_invalid(form)
        messages.success(self.request, 'You have successfully logged in!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('employee_dashboard')
    
class EmployerLoginView(LoginView):
    template_name = 'registration/employer_login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = False

    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser or not user.is_employer:
            return super().form_invalid(form)
        messages.success(self.request, 'You have successfully logged in!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('employer_dashboard')

def employee_logout(request):
    logout(request)
    messages.success(request,('You have successfully logged out'))
    return redirect('/employee_login')

def employer_logout(request):
    logout(request)
    messages.success(request,('You have successfully logged out'))
    return redirect('/employer_login')

class EmployeePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_data'] = "Some custom data"
        print('password done')
        return context
    
class EmployeePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_data'] = "Some custom data"
        print('password complete')
        return context

class EmployerPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/employer_password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_data'] = "Some custom data"
        print('password done')
        return context
    
class EmployerPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/employer_password_reset_complete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_data'] = "Some custom data"
        print('password complete')
        return context

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
            token = PasswordReset.create_token(user)
            
            reset_url = request.build_absolute_uri(reverse('set_new_password', args=[token.token]))
            send_mail('Password Reset', f'Click here to reset your password: {reset_url}', 'hmareiwan@outlook.com', [user.email])
            return redirect('password_reset_done')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'registration/password_reset.html', {'form': form})

def set_new_password(request, token):
    try:
        reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        
        return render(request, 'registration/invalid_token.html')
    
    if now() - reset.timestamp > timedelta(hours=24):
        
        return render(request, 'registration/token_expired.html')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = reset.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('password_reset_complete')
    else:
        form = SetNewPasswordForm()
    return render(request, 'registration/set_new_password.html', {'form': form})

def employer_password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
            token = PasswordReset.create_token(user)
            
            reset_url = request.build_absolute_uri(reverse('employer_set_new_password', args=[token.token]))
            send_mail('Password Reset', f'Click here to reset your password: {reset_url}', 'hmareiwan@outlook.com', [user.email])
            return redirect('employer_password_reset_done')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'registration/employer_password_reset.html', {'form': form})

def employer_set_new_password(request, token):
    try:
        reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        
        return render(request, 'registration/invalid_token.html')
    
    if now() - reset.timestamp > timedelta(hours=24):
        
        return render(request, 'registration/token_expired.html')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = reset.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('employer_password_reset_complete')
    else:
        form = SetNewPasswordForm()
    return render(request, 'registration/employer_set_new_password.html', {'form': form})

def employee_dashboard(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('employee_dashboard')  
    else:
        form = CandidateForm(instance=request.user)
    
    return render(request, 'registration/employee_dashboard.html', {'form': form})


def employer_dashboard(request):
    
    return render(request, 'registration/employer_dashboard.html')


def employee_form(request):
    if request.method=='POST':
        form=EmployeeForm(request.POST)
        employee_id=request.POST['id']
        letters=string.ascii_letters
        if form.is_valid():
            form.save()
            first_name=request.POST['fname']
            second_name=request.POST['lname']
            messages.success(request,'You have added '+first_name + ' '+second_name+' to your database.')
            return redirect ('/employee/list')
        elif [i for i in letters if i in employee_id]:
            messages.error(request,('You entered '+employee_id+' but the value of an ID must be a number, so please change it.'))
            return render (request,'registration/employee_form.html',{'form':form})
        else:
            messages.error(request,('Another employee has been given '+employee_id+' as an ID, so please change it.'))
            return render (request,'registration/employee_form.html',{'form':form})
    else:
        form=EmployeeForm()
        return render (request,'registration/employee_form.html',{'form':form})

def employee_list(request):
    
    p=Paginator(Employee.objects.all().order_by('id'),25)
    page=request.GET.get('page')
    context=p.get_page(page)
    return render(request,'registration/employee_list.html',{'context':context})

def employee_update(request,id=0):
    if request.method=='GET':
        if id==0:
            form = EmployeeForm()
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(instance=employee)
        return render (request,'registration/employee_form.html',{'form':form})       
    else:
        employee_id=request.POST['id']
        if id==0:
            form = EmployeeForm(request.POST)
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(request.POST,instance =employee)
        if form.is_valid():
            form.save()
            messages.success(request,'You have saved the changes of the employee whose ID is '+employee_id+'.')
            return redirect ('/employee/list')
        else:
            messages.error(request,('You entered '+employee_id+' but the value of an ID must be a number, so please change it.'))
            return render (request,'registration/employee_form.html',{'form':form})

def employee_delete(request,id):
    r=get_object_or_404(Employee,id=id)
    r.delete()
    messages.success(request,'You have successfully removed the employee from your database.')
    return redirect('/employee/list')

def employee_timesheet(request,eid=0):
    if request.method=='POST':
        tform=TimesheetForm(request.POST)
        employee_id=request.POST['eid']
        if tform.is_valid():
            tform.save()
            messages.success(request,'You have saved the timesheet of the ID '+employee_id)
            return redirect ('/completed_timesheet')
        else:
            messages.error(request,('The given ID already has the timesheet so you can update it.'))
            return render (request,'registration/employee_timesheet.html',{'tform':tform})
    else:
        tform=TimesheetForm()
        return render (request,'registration/employee_timesheet.html',{'tform':tform})

def completed_timesheet(request):
    
    p=Paginator(Timesheet.objects.all().order_by('eid'),10)
    page=request.GET.get('page')
    context=p.get_page(page)
    return render(request,'registration/completed_timesheet.html',{'context':context})

def timesheet_update(request,eid=0):
    if request.method=='GET':
        if eid==0:
            tform = TimesheetForm()
        else:
            temployee=Timesheet.objects.get(pk=eid)
            tform=TimesheetForm(instance=temployee)
        return render (request,'registration/employee_timesheet.html',{'tform':tform})       
    else:
        employee_id=request.POST['eid']
        if eid==0:
            tform =TimesheetForm(request.POST)
        else:
            temployee=Timesheet.objects.get(pk=eid)
            tform=TimesheetForm(request.POST,instance =temployee)
        if tform.is_valid():
            tform.save()
            messages.success(request,'You have saved the changes of the timesheet for the employee whose ID is '+employee_id+'.')
            return redirect ('/completed_timesheet')
         
        else:
            messages.error(request,('The given ID already has the timesheet so you can update it.'))
            return redirect ('/timesheet')

def timesheet_delete(request,id):
    r=get_object_or_404(Timesheet,pk=id)
    r.delete()
    messages.success(request,'You have successfully removed the timesheet from your database.')
    return redirect ('/completed_timesheet')

def employee_payment(request):
    p=Paginator(Timesheet.objects.all().order_by('eid'),10)
    page=request.GET.get('page')
    context=p.get_page(page)
    return render(request,'registration/employee_payment.html',{'context':context})

def employee_pdf (request,pk):
    employee=Timesheet.objects.get(id=pk)
    tp='registration/employee_pdf.html'
    context={'employee':employee,

    }
    response=HttpResponse(content_type='application/pdf')
    response['content-Disposition'] = 'filename="report.pdf"' #I can add attachment; before filename to view the payslip before download it
    tem=get_template(tp)
    html=tem.render(context) 

    #create a pdf
    pisa_status=pisa.CreatePDF(html,dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' +html + '</pre>')
    return response

def generate_pdf(request, employee_id):
    
    employee = get_object_or_404(Employee, id=employee_id)
    timesheet = get_object_or_404(Timesheet, eid=employee)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{employee.fname}_{employee.lname}_pay_slip.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 830, f"Pay Slip for {employee.id} {employee.fname} {employee.lname} {employee.email}")
    p.drawString(100, 800, f"Pay Slip for {employee.ni} {employee.tcode} {timesheet.date}")
    p.drawString(100, 780, f"Employee ID: {employee.id}")
    p.drawString(100, 760, f"Email: {employee.email}")
    p.drawString(100, 740, f"Total Hours: {timesheet.total_hours()}")
    p.drawString(100, 720, f"Normal Pay Rate: {timesheet.npr}")
    p.drawString(100, 700, f"Overtime Pay Rate: {timesheet.opr}")
    p.drawString(100, 680, f"Gross salary: {timesheet.wages()}")
    p.drawString(100, 660, f"Tax: {timesheet.tax}")
    p.drawString(100, 640, f"NI: {timesheet.ni_contri}")
    p.drawString(100, 620, f"Pension: {timesheet.pen_contri}")
    p.drawString(100, 600, f"Plan 2: {timesheet.stu_loan}")
    p.drawString(100, 580, f"PL: {timesheet.post_stu_loan}")
    p.drawString(100, 560, f"Total deductions: {timesheet.all_deductions}")
    p.drawString(100, 540, f"Net salary: {timesheet.net_salary}")

    p.save()

    return response

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            contact = form.save()
            messages.success(request,'Thanks for your message. We will get bact to you shortly.')
    
            for uploaded_file in request.FILES.getlist('files'):
                ContactFile.objects.create(contact=contact, file=uploaded_file)

            email_to_owner = EmailMessage(
                subject=f'New contact form submission from {contact.name}',
                body=f"Name: {contact.name} \n\nEmail: {contact.email}: \n\nMessage: {contact.message}",
                from_email='hmareiwan@outlook.com',
                to=['hmareiwan@outlook.com'],
            )
            email_to_owner.send()

            send_mail(
                'Thanks for Contacting Us',
                'Dear {},\n\nWe have received your message and files. We will get back to you shortly.\n\nRegards,\n\nIT Solutions'.format(contact.name),
                'hmareiwan@outlook.com',
                [contact.email]
            )

            return redirect('contact')

    else:
        form = ContactForm()
    
    return render(request, 'registration/contact_form.html', {'form': form})

def create_job(request):
    if request.method == 'POST':
        form = JobsForm(request.POST)
        title=request.POST['title']
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully created '+title+' job.')
            return redirect('employer_view_jobs') 
    else:
        form = JobsForm()

    return render (request,'registration/create_job.html',{'form':form})
        

def delete_jobs(request, reference):
    job = get_object_or_404(Jobs, reference=reference)
    job.delete()
    messages.success(request,'You have successfully deleted the job in your database!')
    return redirect('employer_view_jobs')

def employer_view_jobs(request):
    pagin=Paginator(Jobs.objects.all().order_by('reference'),10)
    page=request.GET.get('page')
    context=pagin.get_page(page)
    return render (request,'registration/employer_view_jobs.html',{'context':context})

def candidate_view_jobs(request):
    jobs =Paginator (Jobs.objects.all(),10)
    page=request.GET.get('page')
    context=jobs.get_page(page)
    return render(request, 'registration/candidate_view_jobs.html', {'context':context})

def job_detail(request, reference):
    job = get_object_or_404(Jobs, pk=reference)
    return render(request, 'registration/job_detail.html', {'job': job})


def job_apply(request, reference):
    job = get_object_or_404(Jobs, reference=reference)

    if request.method == 'POST':
        form = ApplyJobForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.cleaned_data['cv']
            file_path = os.path.join('media', 'job_files', cv.name)

            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'wb') as destination:
                for chunk in cv.chunks():
                    destination.write(chunk)

            fname = form.cleaned_data['firstName']
            lname = form.cleaned_data['lastName']
            mobile=form.cleaned_data['mobile']
            recipient_email = form.cleaned_data['email']

            
            job_title = job.title
            job_reference = job.reference

            send_mail(
                'Application Confirmation',
                f'Dear {fname} {lname},\n\nThank you for applying for the position: {job_title} (Reference: {job_reference}). \n\nWe will get back to you very soon.\n\nRegards\n\nIT Solutions',
                'hmareiwan@outlook.com', 
                [recipient_email],  
                fail_silently=False,
            )

            email_to_owner = EmailMessage(
                subject=f'New job application for {job_title}',
                body=f'A new job application has been received for the position: {job_title} (Reference: {job_reference}). Their details are as follows:\n\nName: {fname} {lname}\n\nMobile: {mobile}\n\nEmail: {recipient_email}',
                from_email='hmareiwan@outlook.com',
                to=['hmareiwan@outlook.com'],
            )
            email_to_owner.send()

            messages.success(request, f'Thanks {fname}. You have successfully sent your application form!')
            return redirect('job_apply',reference=job.reference) 

    else:
        form = ApplyJobForm(initial={'job_title': job.title, 'job_reference': job.reference})

    return render(request, 'registration/job_apply.html', {'form': form, 'job': job})

def access_pay_slip(request):
    if request.method == 'POST':
        form = PaySlipAccessForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            dbirth = form.cleaned_data['dbirth']
            
            try:
                employee = get_object_or_404(Employee, email=email, dbirth=dbirth)
                timesheet = get_object_or_404(Timesheet, eid=employee)

                context = {
                    'employee': employee,
                    'timesheet': timesheet,
                }

                messages.success(request, 'Successfully logged in to view your pay slip!')
                return render(request, 'registration/pay_slip_detail.html', context)
            except Http404:
                
                if not Employee.objects.filter(email=email).exists():
                    messages.error(request, 'Incorrect email. Please try again.')
                else:
                    messages.error(request, 'Incorrect date of birth. Please try again.')
                return redirect('access_pay_slip')
    else:
        form = PaySlipAccessForm()

    return render(request, 'registration/access_pay_slip.html', {'form': form})





