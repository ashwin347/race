"""race URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('',views.renderWelcome),
    path('welcome',views.renderWelcome),
    path('admin/', admin.site.urls),
    path('adminlogin',views.renderAdminLogin,name='admin'),
    path('studentlogin',views.renderStudentLogin),
    path('adminloginvalidation',views.adminLoginValidation,name='admin'),
    path('viewstudentdetails',views.viewStudentDetails),
    path('studenthome',views.renderStudentHomePage),
    path('studentprofile',views.renderStudentProfile),
    path('studentblog',views.studentBlog),
    path('studentfeedback',views.studentFeedback),
    path('studentevents',views.renderStudentEvents),
    path('studentjobs',views.renderStudentJobs),
    path('applystudentevents',views.applyStudentEvent),
    path('cancelstudentevents',views.cancelStudentEvent),
    path('applystudentjob',views.applyStudentJob),
    path('cancelstudentjob',views.cancelStudentJob),
    path('insertstudentfeedback',views.insertStudentFeedback),
    path('studentblood',views.renderStudentBlood),
    path('showallstudents',views.renderAdminShowStudents),
    path('insertnewstudent',views.insertNewStudent),
    path('deletestudentdata',views.deleteStudentData),
    path('showallevents',views.renderAdminShowEvents),
    path('insertnewevent',views.insertNewEvent),
    path('deleteeventdata',views.deleteEventData),
    path('showalljobs',views.renderAdminShowJobs),
    path('insertnewjob',views.insertNewJob),
    path('deletejobdata',views.deleteJobData),
    path('showallbloods',views.renderAdminShowBloods),
    path('insertnewblood',views.insertNewBlood),
    path('deleteblooddata',views.deleteBloodData),
    path('liststudents',views.renderStudentsList),
    path('showallfeedbacks',views.showAllFeedbacks),
    path('deletefeedback',views.deleteFeedback),
    path('updatestudentprofile',views.updateStudentProfile),
    path('showallblogs',views.renderStudentBlogs),
    path('viewsingleblog',views.renderSingleBlog),
    path('updatestudentblog',views.updateStudentBlog),
    path('deletestudentblog',views.deleteStudentBlog),
    path('studentnewblogform',views.renderStudentBlogForm), 
    path('addnewblog',views.insertNewBlog),
    path('logout',views.logout)
]
