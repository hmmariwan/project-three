from django.urls import path
from . import views
from . views import (EmployerSignUpView,EmployerLoginView,EmployeeSignUpView,EmployeeLoginView,
                     EmployeePasswordResetDoneView,EmployeePasswordResetCompleteView,
                     EmployerPasswordResetDoneView,EmployerPasswordResetCompleteView)

urlpatterns = [

    path('',views.home,name='home'),

    path('signup/employee/', EmployeeSignUpView.as_view(), name='employee_signup'),
    path('signup/employer/', EmployerSignUpView.as_view(), name='employer_signup'),
    path('login/employee/', EmployeeLoginView.as_view(), name='employee_login'),
    path('login/employer/', EmployerLoginView.as_view(), name='employer_login'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('set_new_password/<str:token>/', views.set_new_password, name='set_new_password'),
    path('password_reset/done/', EmployeePasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/complete/', EmployeePasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('employer_password_reset/', views.employer_password_reset_request, name='employer_password_reset_request'),
    path('employer_set_new_password/<str:token>/', views.employer_set_new_password, name='employer_set_new_password'),
    path('employer_password_reset/done/', EmployerPasswordResetDoneView.as_view(), name='employer_password_reset_done'),
    path('employer_password_reset/complete/', EmployerPasswordResetCompleteView.as_view(), name='employer_password_reset_complete'),

    path('employee/', views.employee_form,name='employee_insert'),
    path('employee/list/',views.employee_list,name='employee_list'),
    path('employee/<int:id>/',views.employee_update,name='employee_update'),
    path('employee/delete/<int:id>/',views.employee_delete,name='employee_delete'),
    path('timesheet/',views.employee_timesheet,name='employee_timesheet'),
    path('completed_timesheet/',views.completed_timesheet,name='completed_timesheet'),
    path('timesheet/<int:eid>/',views.timesheet_update,name='timesheet_update'),
    path('timesheet/delete/<int:id>/',views.timesheet_delete,name='timesheet_delete'),
    path('employee_payment/',views.employee_payment,name='employee_payment'),
    path('employee_pdf/<int:pk>/',views.employee_pdf,name='employee_pdf'),
    path('contact/',views.contact_view,name='contact'),
     
    path('create_job/', views.create_job, name='create_job'),
    path('delete_jobs/<str:reference>/',views.delete_jobs,name='delete_jobs'),
    path('employer_view_jobs/', views.employer_view_jobs, name='employer_view_jobs'),
    path('candidate_view_jobs/', views.candidate_view_jobs, name='candidate_view_jobs'),
    path('job/<str:reference>/', views.job_detail, name='job_detail'),
    path('job_apply/<str:reference>/', views.job_apply, name='job_apply'),

    path('access_pay_slip/', views.access_pay_slip, name='access_pay_slip'),
    path('generate_pdf/<int:employee_id>/', views.generate_pdf, name='generate_pdf'),
]
