from django.db import models
from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import pre_save
from .models import *
from zhiportal.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

JOB_TYPE = (("1", "Full time"), ("2", "Part time"), ("3", "Internship"))
JOB_STATUS = (("1", "Approved"), ("2", "Declined"), ("3", "Pending"))
JOB_CAT = (("1", "Internal"), ("2", "External"))

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300,blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300,blank=True, null=True)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.CharField(max_length=300,blank=True, null=True)
    closingdate = models.DateField()
    linktoform= models.CharField(max_length = 300,blank=True, null=True)
    job_category=models.CharField(choices=JOB_CAT, max_length=200)

    


    class Meta: 
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", args=[self.id])

    def __str__(self):


        return self.title
    
    def send(self, request):
        subscribers = Subscriber.objects.all()
        for sub in subscribers:
            recepient = sub.email
            subject='Vacancy Notification'
            message='There is an open vacancy for' + self.title + 'Vacancy Expires on ' + self.closingdate + '\n'  + '\n' + 'Good day' +'\n' +'\n' +'ZHI IMIS'
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    




class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="account")
    firstname = models.CharField(max_length=300,blank=True, null=True)
    surname = models.CharField(max_length=300,blank=True, null=True)
    email= models.EmailField(max_length=300,blank=True, null=True)
    contact = models.CharField(max_length=300,blank=True, null=True)
    cv=models.FileField(upload_to='cv/')
    cover_letter=models.FileField(upload_to='coverletter/')
    description=models.TextField(max_length=300,blank=True, null=True)
    address = models.CharField(max_length=300,blank=True, null=True)
    recent_position = models.CharField(max_length=300,blank=True, null=True)
    profilepic = models.ImageField(upload_to='pic/',default='default.png')
    created_at = models.DateTimeField(default=timezone.now)
    locate = models.CharField(max_length=300,blank=True, null=True)
    NOG = models.CharField(max_length=300,blank=True, null=True)
    experince = models.CharField(max_length=300,blank=True, null=True)
    degree = models.CharField(max_length=300,blank=True, null=True)
    masters = models.CharField(max_length=300,blank=True, null=True)
    current_salary = models.CharField(max_length=300,blank=True, null=True)
    


    def __str__(self):
        return self.firstname + self.surname
     
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="applicant" )
    account=models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    status = models.BooleanField(null=True)
    shortlisted = models.BooleanField(null=True)
    # language = models.CharField(max_length=300,blank=True, null=True)
    # QA = models.CharField(max_length=300,blank=True, null=True)
    # InstiA=models.CharField(max_length=300,blank=True, null=True)
    # StartA=models.DateField(null=True)
    # EndA=models.DateField(null=True)
    # GradA=models.CharField(max_length=300,blank=True, null=True)
    # QB = models.CharField(max_length=300,blank=True, null=True)
    # InstiB=models.CharField(max_length=300,blank=True, null=True)
    # StartB=models.DateField(null=True)
    # EndB=models.DateField(null=True)
    # GradB=models.CharField(max_length=300,blank=True, null=True)
    # QC = models.CharField(max_length=300,blank=True, null=True)
    # InstiC=models.CharField(max_length=300,blank=True, null=True)
    # StartC=models.DateField(null=True)
    # EndC=models.DateField(null=True)
    # GradC=models.CharField(max_length=300,blank=True, null=True)
    # NRA=models.CharField(max_length=300,blank=True, null=True)
    # NOGA= models.CharField(max_length=300,blank=True, null=True)
    # TitleA = models.CharField(max_length=300,blank=True, null=True)
    # ContactA= models.CharField(max_length=300,blank=True, null=True)
    # EmailA=models.CharField(max_length=300,blank=True, null=True)
    # NRB=models.CharField(max_length=300,blank=True, null=True)
    # NOGB= models.CharField(max_length=300,blank=True, null=True)
    # TitleB = models.CharField(max_length=300,blank=True, null=True)
    # ContactB= models.CharField(max_length=300,blank=True, null=True)
    # EmailB=models.CharField(max_length=300,blank=True, null=True)
    # NRC=models.CharField(max_length=300,blank=True, null=True)
    # NOGC= models.CharField(max_length=300,blank=True, null=True)
    # TitleC = models.CharField(max_length=300,blank=True, null=True)
    # ContactC= models.CharField(max_length=300,blank=True, null=True)
    # EmailC=models.CharField(max_length=300,blank=True, null=True)
    # CSalary=models.CharField(max_length=300,blank=True, null=True)
    # ESalary= models.CharField(max_length=300,blank=True, null=True)
    # Benefits= models.CharField(max_length=300,blank=True, null=True)
    # Others  = models.TextField(blank=True, null=True)
    # dob=models.DateField()
    # biodata=models.FileField(upload_to='cv/',default='default.png') 
    
    

    class Meta:
        ordering = ["id"]
        unique_together = ["user", "job"]

    def __str__(self):
        return str(self.user) +'-' +  str(self.job)

class Sex(models.Model):
    description = models.CharField(max_length=300,blank=True, null=True)
    initial = models.CharField(max_length=300,blank=True, null=True)
    
    def __str__(self):
        return self.description

class Country(models.Model):
    name = models.CharField(max_length=300,blank=True, null=True)
    shortcode = models.CharField(max_length=300,blank=True, null=True)
    
    def __str__(self):
        return self.name
class AccountExtra(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    sex=models.ForeignKey(Sex, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    dob = models.CharField(max_length=300,blank=True, null=True)
    skill_a = models.CharField(max_length=300,blank=True, null=True)
    skill_b = models.CharField(max_length=300,blank=True, null=True) 
    skill_c =models.CharField(max_length=300,blank=True, null=True)
    reference_a = models.CharField(max_length=300,blank=True, null=True)
    reference_b = models.CharField(max_length=300,blank=True, null=True)
    reference_c = models.CharField(max_length=300,blank=True, null=True)
    highest_education = models.CharField(max_length=300,blank=True, null=True)
    notification = models.BooleanField(default=False)

    def __str__(self):
        return self.account

class FAQ(models.Model):
    question = models.CharField(max_length=300,blank=True, null=True)
    answer = models.TextField(max_length=300,blank=True, null=True)
    
    def __str__(self):
        return self.question  

class Shortlist(models.Model):
    job= models.name = models.ForeignKey(Job, related_name='job', on_delete=models.CASCADE)
    applicant= models.ForeignKey(Applicant, related_name='applicant',on_delete=models.CASCADE)
    shortlister=models.ForeignKey(User, related_name='applicantofficer', on_delete=models.CASCADE)
    officer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    
    def __str__(self):
        return self.applicant
    
class Interview(models.Model):
    job= models.name = models.ForeignKey(Job, related_name='jobin', on_delete=models.CASCADE)
    applicant= models.ForeignKey(Applicant, related_name='applicantin',on_delete=models.CASCADE)
    officerin = models.ForeignKey(User, related_name='int',on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.applicant
    
class Subscriber(models.Model):
    email = models.EmailField(unique=False)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    
class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")
        



class Biodata(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cv=models.FileField(upload_to='biodata/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="accountz")

class BiodataForm(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cv=models.FileField(upload_to='biodata/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="accounts")


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
