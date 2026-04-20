from django.urls import path
from .  import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout',views.signout , name='logout' ),
    path('create-job',views.createjobs, name='create-job' ),
    path('apply-job',views.applyjob, name='apply-job' ),
    path('manage-job',views.managejobs, name='manage-job' ),
    path('candidates',views.managecandidates, name='candidates' ),
    path('tables',views.tables, name='tables' ),
    path('applications',views.manageapplication, name='applications'),
    path('list-job',views.jobslist, name='list-job' ),
    path('apply/<int:id>',views.apply, name='apply'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('create-profile',views.profile, name='create-profile' ),
    path('profile',views.profile, name='profile' ),
    path('comment',views.comment, name='comment' ),
    path('chat1',views.chat, name='chat1' ),
    path('new',views.new, name='new' ),
    path('biodata',views.biodata, name='biodata' ),
    path('confirm/', views.confirm, name='confirm'),
    path('interv',views.interv, name='interv'),
    path('shortcan',views.shortcan, name='shortcan'),
    path('profile-view',views.profileview, name='profile-view'),
    path('profile-extra',views.profile, name='profile-extra' ),
    path('approve/<int:id>',views.approve, name='approve' ),
    path('delete/<int:id>',views.delete, name='delete' ),
    path('single-job/<int:id>',views.singlejob, name='single-job' ),
    path('single-application/<int:id>/<int:id2>',views.single, name='single-applicant' ),
    path('update/<int:id>',views.update, name='update' ),
    path('job-candidates/<int:id>',views.jobcandidates, name='job-candidates' ),
    path('updatejob/<int:id>',views.updatejob, name='updatejob' ),
    path('chat', views.chat_view, name='chat'),
    path('csform/<str:id>', views.csform, name='csform'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)