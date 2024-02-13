from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Permission,Group
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    mobile=models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='employee_photos/', default='default.jpg', null=True, blank=True)
    cv = models.FileField(upload_to='candidate_files/', null=True, blank=True)  

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions',  # Change this line
        help_text=_('Specific permissions for this user.'),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups',  # Change this line
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
    )

class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def create_token(cls, user):
        return cls.objects.create(user=user, token=get_random_string(50))

class Employee(models.Model):
    id=models.IntegerField(primary_key=True,verbose_name='Employee ID')
    fname=models.CharField(max_length=20,verbose_name='First Name')
    lname=models.CharField(max_length=20,verbose_name='Last Name')
    mobile=models.CharField(max_length=15,verbose_name='Mobile')
    dbirth=models.DateField()
    email=models.EmailField(max_length=200)
    ni=models.CharField(max_length=20,verbose_name='National Insurance Number')
    tcode=models.CharField(max_length=20,verbose_name='Tax Code')
    join_pension=(('No','No'),('Yes','Yes'))
    pension=models.CharField(max_length=3,null=True,choices=join_pension) #returns Yes or No
    sloan=(('P1','Plan 1'),('P2','Plan 2'),('P4','Plan 4'),('P5','Plan 5'),('PL','Postgraduate Loan'),('P2&PL','Plan 2 and Postgraduate Loan'),('No','No'))
    student_loan=models.CharField(max_length=20,null=True,choices=sloan,verbose_name='Student Loan')

    def __str__(self):
        return str(self.id)

class Timesheet(models.Model):
    gross_salary=0;net_salary=0;tax=0;ni_contri=0;pen_contri=0;stu_loan=0;post_stu_loan=0;all_deductions=0
    eid=models.OneToOneField(Employee,on_delete=models.CASCADE,verbose_name='ID')
    mon=models.FloatField(default=0)
    tue=models.FloatField(default=0)
    wed=models.FloatField(default=0)
    thu=models.FloatField(default=0)
    fri=models.FloatField(default=0)
    sat=models.FloatField(default=0)
    sun=models.FloatField(default=0)
    npr=models.FloatField(verbose_name='Normal Pay Rate')
    opr=models.FloatField(verbose_name='Overtime Pay Rate')
    date=models.CharField(max_length=255,default='')

    def total_hours(self):
        return self.mon + self.tue + self.wed + self.thu + self.fri + self.sat + self.sun
    
    def wages(self):
        hours = self.total_hours()
        if hours <= 37.5:
            self.normal_hours=hours
            self.overtime_hours=0
            self.gross_salary=round (self.normal_hours*self.npr,2)
        else:
            self.normal_hours=37.5
            self.overtime_hours=round(hours-37.5,2)
            self.gross_salary=round(self.overtime_hours*self.opr+(self.normal_hours*self.npr),2)

        if 'L' in self.eid.tcode.upper():
            if self.gross_salary <=245:
                self.tax=0
            elif self.gross_salary >245 and self.gross_salary <967:
                self.tax=round(((self.gross_salary-245)*20)/100,2)
            else:
                self.tax=round(((self.gross_salary-967)*40)/100+((self.gross_salary-245)-(self.gross_salary-967))*20/100,2)
        elif self.eid.tcode.upper()=='BR':
            self.tax=round((int(self.gross_salary)*20)/100,2)
        else:
            self.tax=round((self.gross_salary*40)/100,2)
       
        if self.gross_salary < 242:
            self.ni_contri=0
        elif self.gross_salary >= 242 and self.gross_salary <= 967:
            self.ni_contri=round((self.gross_salary*12)/100,2)
        else:
            self.ni_contri=round((self.gross_salary*2)/100,2)

        if self.eid.pension=='Yes':
            if self.gross_salary<200:
                self.pen_contri=0
            else:
                self.pen_contri=round(self.gross_salary*4/100,2)
        
        if self.eid.student_loan=='No':
            self.stu_loan=0
            self.post_stu_loan=0
        elif self.eid.student_loan=='P1':
            if self.gross_salary>423:
                self.stu_loan=round((self.gross_salary-423)*9/100,2)
        elif self.eid.student_loan=='P2':
            if self.gross_salary >524:
                self.stu_loan=round((self.gross_salary-524)*9/100,2)
        elif self.eid.student_loan=='P4': 
            if self.gross_salary >532: 
                self.stu_loan=round(((self.gross_salary-532)*9)/100,2)
        elif self.eid.student_loan=='P5':
            if self.gross_salary>480:
                self.stu_loan=round((self.gross_salary-480)*9/100,2)
        elif self.eid.student_loan=='P2&PL':
            if self.gross_salary >524:
                self.stu_loan=round((self.gross_salary-524)*9/100,2)
                self.post_stu_loan=round((self.gross_salary-403)*6/100,2)
            elif self.gross_salary >403 and self.gross_salary<=524:
                self.post_stu_loan=round((self.gross_salary-403)*6/100,2)  
        else:
            if self.gross_salary>403:
                self.post_stu_loan=round((self.gross_salary-403)*6/100,2)
        
        self.all_deductions=round(self.tax + self.ni_contri + self.pen_contri+self.stu_loan+self.post_stu_loan,2)
        self.net_salary=round(self.gross_salary-self.all_deductions,2)

        return self.gross_salary


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

class ContactFile(models.Model):
    contact = models.ForeignKey(Contact, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="contact_files/")

    
class Jobs(models.Model):
    reference=models.CharField(primary_key=True,max_length=15)
    title = models.CharField(max_length=255)
    duration=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    rate=models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.reference

    


