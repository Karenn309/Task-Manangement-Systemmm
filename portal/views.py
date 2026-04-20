from cgi import print_arguments
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.views import View
from .models import *
from form_designer.models import *
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.models import User,Group
from django.db.models.functions import Extract
from .forms import  NewUserForm
from datetime import *
from DateTime import DateTime
from zhiportal.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import jsons



# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login as loginUser , logout
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import messages
from django.contrib.admin.models import LogEntry
import random



from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from portal.models import Message
from portal.forms import SignUpForm
from portal.serializers import MessageSerializer, UserSerializer


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


def home(request):
    aa= datetime.now().date()
    cli=Job.objects.filter(closingdate__gte=aa).order_by('-pk')[:5:-1]
    tjobs = Job.objects.all().count
    tapplicants = Applicant.objects.all().count
    final = {'cli':cli,'tjobs':tjobs,'tapplicants':tapplicants}
    return render(request,'index-logged-out.html',final)

def login(request):
    if request.method == 'POST':
        _username = request.POST['_username']
        _password = request.POST['_password']
        user = authenticate(username = _username,password = _password)
        if user is not  None:
            loginUser(request , user)
            user2=request.user
            
            if request.user.is_staff:
                
                return redirect('dashboard')
            else:
                if Account.objects.filter(user=user2).exists():
                    return redirect('list-job')
                else:
                    return redirect('profile')
            # return render(request,'jobslist.html')
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect Details')
            return render(request,'sign-in.html')
            
            
    else:
        return render(request,'sign-in.html')
    return render(request,'sign-in.html')


@csrf_exempt
def new(request):
    if request.method == 'POST':
        sub = Subscriber.objects.create(email=request.POST['email'], conf_num=random_digits())
        sub.save()
        recepient = request.POST['email']
        print(request.POST['email'])
        subject='Newsletter Confirmation'
        message='Thank you for signing up to our newsletter!' + '\n'  + '\n' + 'Good day' +'\n' +'\n' +'ZHI IMIS'
                
        # message = Mail(
        #     from_email=settings.FROM_EMAIL,
        #     to_emails=request.POST['email'],
        #     subject='Newsletter Confirmation',
        #     html_content='Thank you for signing up to our newsletter! \
        #         Please complete the process by \
        #         <a href="{}/confirm/?email={}&conf_num={}"> clicking here to \
        #         confirm your registration</a>.'.format(request.build_absolute_uri('/confirm/'),
        #                                             sub.email,
        #                                             sub.conf_num))
        # sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        # response = sg.send(message)
        send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'index-logged-out.html', {'email': sub.email, 'action': 'added'})
    else:
        return render(request, 'index-logged-out.html')

def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'index-logged-out.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'index-logged-out.html', {'email': sub.email, 'action': 'denied'})


# def jobcandidates(request,id):
#     request.session['candidate'] = id
#     a=Job.objects.filter(pk = id)
#     hh = Applicant.objects.filter(job= id)
#     staff = User.objects.filter(is_staff=True)

#     for aa in staff:
#         print(aa.username)   

#     print(a)
#     for zx in a:
#         ax = zx.linktoform
    

#     xx = FormSubmission.objects.filter(form__title=ax).values_list('data',flat=True)
#     out = jsons.dump(xx)
#     out2 = jsons.load(out)

#     for item in out2:
#         print(item.items.key)
#     print(out2)
#     h=[]
#     for r in xx:
#         h.append(r.split())
    
   

#     print("yes")
#     return render(request,'short.html',{'a':a,'h':h,'staff':staff})

    

def jobcandidates(request,id):
    request.session['candidate'] = id
    a=Job.objects.filter(pk = id)
    h = Applicant.objects.filter(job= id)
    staff = User.objects.filter(is_staff=True)
     
    print("yes")
    return render(request,'shortlist.html',{'a':a,'h':h,'staff':staff})


@csrf_exempt
def shortcan(request):
    id=request.session.get('candidate')
    if request.method == 'POST':
       try:
           se_id= request.session.get('candidate')
           user= request.user
           officer= request.POST['gC']
           applicantlist = request.POST.getlist('select_all')
           checked_instances = Applicant.objects.filter(id__in=applicantlist)
           print('checked_instances')
           job=Job.objects.get(pk =se_id)
           out =User.objects.get(pk=officer)
           for a in checked_instances:
               allons = Shortlist.objects.create(
                   job=job,
                   applicant= Applicant.objects.get(pk =a.id),
                   shortlister=user,
                   officer=out)
               print('well done allonschecked_instances')
                        
           messages.add_message(request, messages.SUCCESS, 'ShortListed Succesfully')
           recepient = out.email
           subject='ShortListed Candidates'
           message='Dear Sir/Madam'+'\n'+'Kindly process the shortlisted candidates for ' +'  ' + job.title + 'vacany' +'\n'+ 'Regards' +'\n' +'\n' +'ZHI IMIS'
           send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
       except Exception as e:
           print('unknown error')
           pass

        
    staff = User.objects.filter(is_staff=True)
    for a in staff:
        print(a.username)   
    a=Job.objects.filter(pk = id)

    h = Applicant.objects.filter(job= id)
    for ac in a:
        ax = ac.linktoform
        print(ax)
    output = FormSubmission.objects.all()
    return render(request,'shortlist.html',{'a':a,'h':h,'staff':staff})


def interv(request):
    print('ey')
    if request.method == 'POST':
        se_id= request.session.get('approve')
        user= request.user
        output = FormSubmission.objects.all()
        applicantlist = request.POST.getlist('select_all')
        checked_instances = Shortlist.objects.filter(id__in=applicantlist)
        job=Job.objects.get(pk =se_id)
       
        for a in checked_instances:
            allons = Interview.objects.create(
                job=job,
                applicant= Applicant.objects.get(pk =a.applicant.id),
                officerin=user
            )
            recepient = a.applicant.account.email
            subject='Interview Invitation'
            message= 'Dear Sir/Madam'+'\n' + 'You application for' +' ' + job.title + 'vacany has been successfull and you have been shortlisted for interviews ' + '\n'  + 'Regards' +'\n' +'\n' +'ZHI IMIS'
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            print('well done interview instances')
        messages.add_message(request, messages.SUCCESS, 'Applicants selected  Succesfully')
        
    id=request.session.get('approve')
    job=Job.objects.get(pk =id)
    staff = User.objects.filter(is_staff=True)
    for a in staff:
        print(a.username)   
    h=Shortlist.objects.filter(job = job)
    print('eeey')
    return render(request,'interview.html',{'h':h,'staff':staff})


def approve(request,id):
    request.session['approve'] = id
    job=Job.objects.get(pk =id)
    staff = User.objects.filter(is_staff=True)
    for a in staff:
        print(a.username)   
    h=Shortlist.objects.filter(job = job)
    return render(request,'interview.html',{'h':h,'staff':staff})


def cmsform(request):
    return render(request,'interview.html')

@csrf_exempt
@login_required(login_url='login')
def profileview(request):
    account = Account.objects.filter(user=request.user)
    return render(request,'profile.html',{'account':account})
    
@csrf_exempt
@login_required(login_url='login')
def dashboard(request):
    use = request.user
    tjobs = Job.objects.all().count
    ab= datetime.now().date()
    aa = Job.objects.filter(closingdate__gte = ab).order_by('-pk')[:5:-1]
    tapplicants =Applicant.objects.all().count
    action= LogEntry.objects.filter(user=request.user).order_by('-pk')[:5:-1]
    print(tapplicants)
    content={'use':use,'tjobs':tjobs,'aa':aa,'tapplicants':tapplicants,'action':action}
    return render(request,'admin.html',content)
    
        
@csrf_exempt
@login_required(login_url='login')
def managejobs(request):
    # if request.user.is_authenticated:
    #     print('yes')
    
    cli=Job.objects.all()
    final = {'cli':cli}
    print(final)
    return render(request,'dashboard-manage-jobs.html',final)

@csrf_exempt
@login_required(login_url='login')
def createjobs(request):
    fom = Form.objects.all()
    
    if request.user.is_authenticated:
        message= messages.success(request, "Add a job")
        if request.method =='POST':
            user = request.user
            title = request.POST['title']
            category = request.POST['category']
            location = request.POST['location']
            currency = request.POST['currency']
            description = request.POST['description']
            company = "ZHI"
            companydescription = "ZHI"
            website= "website"
            expiry= request.POST['date']
            link= request.POST['link']
            cat= request.POST['cat']
            
            if Job.objects.filter(title=title).exists():
                a= request.session.get('selected_id')
                update = Job.objects.get(pk =a)
                update.user = user
                update.title =title
                update.description = description
                update.salary = currency
                update.location = location
                update.closingdate= expiry
                update.linktoform = link
                update.job_category = cat
                update.type = category
                update.save()
                print('done update')
                messages.add_message(request, messages.SUCCESS, 'Vacancy updated Succesfully')
            else:
                createdjob =Job.objects.create(user=user,title=title,description=description,salary=currency,company_name=company,company_description=companydescription,type=category,location=location,website=website,closingdate=expiry,linktoform=link,job_category=cat)
                subscribers = Subscriber.objects.all()
                for sub in subscribers:
                    recepient = sub.email
                    subject='Vacancy Notification'
                    message='There is an open vacancy for' + title + 'Vacancy Expires on ' + expiry + '\n'  + '\n' + 'Good day' +'\n' +'\n' +'ZHI IMIS'
                    send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    
                messages.add_message(request, messages.SUCCESS, 'Vacancy created Succesfully')
            return render(request,'dashboard-post-a-job.html')
        print('aa')
    
    return render(request,'dashboard-post-a-job.html',{'fom':fom})


def updatejob(request ,id):
    request.session['selected_id'] = id
    updates = Job.objects.filter(pk =id)
    for a in updates:
        
        print(a.id)     
    messages.add_message(request, messages.SUCCESS, 'Create Vacancy')
    return render(request,'dashboarduser.html',{'updates':updates})


@csrf_exempt
@login_required(login_url='login')
def managecandidates(request):
    aa= datetime.now().date()
    cli=Job.objects.filter(closingdate__gte=aa)
    final = {'cli':cli}
    print(cli.query)
    return render(request,'dashboard-manage-candidates.html',final)



@csrf_exempt
@login_required(login_url='login')
def manageapplication(request):
    use=request.user
    account= Account.objects.filter(user=use)
    cli = Applicant.objects.filter(user=request.user)
    final = {'cli':cli,'account':account}
    print(cli.query)
    return render(request,'myapplicants.html',final)

@csrf_exempt
@login_required(login_url='login')
def applyjob(request):
    if request.user.is_authenticated:
        user = request.user
        if Account.objects.filter(user=user).exists():
            account = Account.objects.get(user=user)
            if request.method == 'POST':
                ac= request.POST['job']
                aa= Job.objects.get(pk=ac)
                bc=Account.objects.get(user=request.user.id)
                print("ýes ")
                if Applicant.objects.filter(job = aa, user =user).exists():
                    messages.add_message(request, messages.ERROR, 'You have already applied')
                    return HttpResponseRedirect('list-job')
                else:
                    create = Applicant.objects.create(user=user,job=aa,account=account)
                    subject = 'Welcome to ZHI Portal'
                    message = 'Dear Sir /Madam' +'\n' +'Your Application has been suceesful.'+'\n' + 'We will get in touch with you soon' + '\n' +'Regards' +'\n' +'ZHI IMIS'
                    mil=Account.objects.get(user=request.user)
                    aa=mil.email 
                    recepient = aa
                    send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                    messages.add_message(request, messages.SUCCESS, 'Application Succesfull')
                    return HttpResponseRedirect('list-job')
                    
        else:
            messages.add_message(request, messages.ERROR, 'Create your profile first before application')
            return redirect('create-profile')

        
        
    logout(request)
    
    return redirect('home')



def biodata(request):
    if request.method == 'POST':
        aa=request.user
        abc = request.FILES['cv']
        created = Biodata.objects.create(user=aa,cv=abc)
        return render(request,'biodata-upload.html')
    else:
        h = BiodataForm.objects.all()
        return render(request,'biodata-upload.html',{'h':h})


def apply(request, id):
    request.session['jobid'] = id
    return render(request, 'apply.html')



def signout(request):
    logout(request)
    return redirect('login')


@csrf_exempt
@login_required(login_url='login')
def shortlisted(request):
    if request.method == 'POST':
        try:
            comment = request.POST['text']
            app=request.POST['job']
            tru = Applicant.objects.get(pk=app)
            tru.comment=comment
            tru.job.filled = True
            mil = tru.account.email
            print(mil)
            print('no')
            tru.save()
            print('yes')
            subject = 'ZHI Vacancy'
            message = 'Your Application has been succesfull.'+'\n' + 'We will get in touch with you soon' + '\n' + '\n' +'Good day'
            recepient = mil
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            messages.add_message(request, messages.SUCCESS, 'Shortlist Succesfull')
            return HttpResponseRedirect('candidates')
        except:
            messages.add_message(request, messages.SUCCESS, 'Shortlist Succesfull but network is down')
            return HttpResponseRedirect('candidates')
            
  
def extraprofile(request):
    use = request.user
    a= Account.objects.filter(user=use)
    
    return render(request,'blog.html')
  
def faq(request):
    b = FAQ.objects.all()
    return render(request,'blog.html',{'b':b})
    

def tables(request):
    a=Job.objects.all()
    h= Applicant.objects.all()
    return render(request,'job-table.html',{'a':a,'h':h})
    



@csrf_exempt
@login_required(login_url='login')
def comment(request):
    if request.method == 'POST':
        comment1 = request.POST['comment']
        applicant = request.POST['comment']
        account = Applicant.objects.get(pk=applicant)
        account.comment = comment1
        account.save()
        if account.save():
            messages.add_message(request, messages.SUCCESS, 'Application Updated')
            return redirect('candidates')
        else:
            messages.add_message(request, messages.ERROR, 'Application Update Failed')
            return redirect('candidates')
            
    return render(request,'time.html')



@csrf_exempt
@login_required(login_url='login')
def jobslist(request):
    use = request.user
    account= Account.objects.filter(user=use)
    aa= datetime.now().date()
    cli=Job.objects.filter(closingdate__gte=aa)
    final = {'cli':cli,'account':account}
    
    
    return render(request,'jobslist.html',final)




@csrf_exempt
@login_required(login_url='login')
def singlejob(request, id):
    user = request.user
    account = Account.objects.filter(user=user)
    print(id)
    cli=Job.objects.filter(pk = id)
    
    final = {'cli':cli,'account':account}
    return render(request,'single-job-page.html',final)



 
def signup(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.SUCCESS, 'Account created Successfully.Login to create your Profile')
            return render(request,'signup.html',{'f':f})
            
    else:
        f = UserCreationForm()
        
        
    return render(request,'signup.html',{'f':f})





@csrf_exempt
@login_required(login_url='login')
def profile(request):
    user = request.user
    uu=User.objects.filter(username = user)
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            name = request.POST['fname']
            surname = request.POST['sname']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            post = request.POST['posts']
            locate = request.POST['loc']
            ngo = request.POST['ngo']
            degree = request.POST['deg']
            masters = request.POST['mast']
            yep = request.POST['yep']
            csal = request.POST['csal']
            cv=request.FILES['cv']
            cover=request.FILES['cv']
            prof=request.FILES['prof']
            description = request.POST['scripts']
            print('its been a long day')
            if Account.objects.filter(user=user).exists():
                account = Account.objects.get(user=request.user)
                account.user = user
                account.firstname = name
                account.surname=surname
                account.email=email
                account.contact=contact
                account.address=address
                account.cover_letter=cover
                account.profilepic =prof
                account.description=description
                account.recent_position=post
                account.cv=cv
                account.locate=locate
                account.NOG=ngo
                account.experince=yep
                account.masters=masters
                account.current_salary=csal
                
                account.degree=degree
                account.save() 
                messages.add_message(request, messages.SUCCESS, 'Profile updated succesfully , you can now apply for vacancies')
                return render(request,'dashboard-settingsuser.html',{'uu':uu})
            else:
                created=Account.objects.create(user=user,firstname=name,surname=surname,email=email,contact=contact,address=address,cover_letter=cover,profilepic =prof,
                                               description=description,recent_position=post,cv=cv,locate=locate,NOG=ngo,experince=yep,masters=masters,degree=degree,current_salary=csal)
                messages.add_message(request, messages.SUCCESS, 'Profile created succesfully , you can now apply for vacancies')
                return render(request,'dashboard-settingsuser.html',{'uu':uu})
                
    return render(request,'dashboard-settingsuser.html',{'uu':uu})
    
  
@csrf_exempt
@login_required(login_url='login')
def delete(request , id ):
    print(id)
    Job.objects.get(pk = id).delete()
    if Job.objects.get(pk = id).delete():
        messages.add_message(request, messages.SUCCESS, 'Job Deleted Succesfully')
        return HttpResponseRedirect('create-job')
    else:
        messages.add_message(request, messages.SUCCESS, 'Job Deletion Failed')
        return HttpResponseRedirect('create-job')
        
    return redirect('manage-job')

@csrf_exempt
@login_required(login_url='login')
def update(request , id ):
    print(id)
    Applicant.objects.get(pk = id).delete()
    if Applicant.objects.get(pk = id).delete():
        messages.add_message(request, messages.SUCCESS, 'Application Deleted Succesfully')
        return HttpResponseRedirect('applications')
    else:
        messages.add_message(request, messages.SUCCESS, 'Application Deleted Succesfully')
        return redirect('application')   



@csrf_exempt
@login_required(login_url='login')
def single(request , id ,id2 ):
    print(id)
    pc=Account.objects.get(pk =id)
    app=Applicant.objects.filter(pk = id2,account=pc)
    account=Account.objects.filter(pk = id)
    return render(request, 'single-applicant-page.html',{'account':account,'app':app})
   
# Create your views here.


def chat(request):
    
    return render(request,'dashboard-messages.html')



def interview(request):
    return render(request, 'interview.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    """
    Render registration template
    """
    if request.method == 'POST':
        print("working1")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')
    else:
        print("working2")
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form':form}
    return render(request, template, context)

@csrf_exempt
def csform(request ,id):
    filt = id
    fom = Form.objects.get(title=filt)
    print(fom)
    form_class = fom.form()
    form = form_class()
    print(form)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            result = fom.process(form, request)
            print(result)
            fields = FormSubmission._meta.get_fields()
            result = FormSubmission.objects.filter(id='1').values_list('data',flat=True)
            print(fields)
            

    return render(request,'test.html',{"form":form})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'dashboard-messages.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "dashboard-messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})
