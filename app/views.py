from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from .models import studentDetails
from django.http import HttpResponse
import sys
sys.path.append(r'C:\Users\best\Anaconda3\Lib\site-packages')
import mysql.connector
from datetime import datetime
today=datetime.today().strftime('%Y-%m-%d')# Create your views here.
def renderWelcome(request):
    try:
        email=request.session['email']
        return renderStudentHomePage(request)
    except:
        return render(request,'welcome.html')
def renderAdminLogin(request): #URL- adminlogin : returns admin login page template  
    return render(request,template_name='adminLogin.html') 
def renderStudentLogin(request):
    return render(request,'studentLogin.html')
@csrf_exempt
def adminLoginValidation(request):          # validates user login
    email=request.POST['email']
    password=request.POST['password']
    type=request.POST['type']
    if type=='admin':
        if email=='admin' and password=='admin':  # returns admin home template  if username and password is admin
            return render(request,'adminLeftPane.html')
        else:
            return render(request,'adminLogin.html',{'error':'True'})
    else:
        connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM `students` where email="'+email+'" and password= "'+password+'"')
        users=cursor.fetchall()
        if len(users)==0:
            return render(request,'adminLogin.html',{'error':'True'})
        else:
            request.session['email']=users[0][2]
            return renderStudentHomePage(request,users[0])
def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return render(request,'welcome.html')
def renderAdminShowBloods(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT b.*, COUNT(r.bloodid) AS "counts" FROM requirement b LEFT JOIN bloodregistrations r on b.id = r.bloodid GROUP BY b.id')
    bloods=cursor.fetchall()
    return render(request,'adminShowAllBloods.html',{'bloods':bloods})

def renderAdminShowEvents(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT e.*, COUNT(r.eventId) AS "counts" FROM events e LEFT JOIN eventregistrations r on e.id = r.eventId GROUP BY e.id')
    events=cursor.fetchall()

    return render(request,'adminShowAllEvents.html',{'events':events})

def renderAdminShowJobs(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT j.*, COUNT(r.jobid) AS "counts" FROM jobs j LEFT JOIN jobregistrations r on j.id = r.jobid GROUP BY j.id')
    jobs=cursor.fetchall()
    return render(request,'adminShowAllJobs.html',{'jobs':jobs})

def renderAdminShowStudents(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM `students`')
    users=cursor.fetchall()
    return render(request,'adminShowAllStudents.html',{'students':users})
@csrf_exempt
def insertNewStudent(request):
    name=request.POST['name']
    phone=request.POST['number']
    email=request.POST['email']
    password=request.POST['password']
    blood=request.POST['blood']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO `students`(`name`, `email`, `phone`, `password`, `blood`) VALUES ("'+name+'", "'+email+'", "'+phone+'", "'+password+'", "'+blood+'")')
    connection.commit()
    return HttpResponse('Success')
@csrf_exempt
def deleteStudentData(request):
    id=request.POST['id']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    email=request.session['email']
    cursor.execute('select id from students where email="'+email+'"')
    sid=cursor.fetchall()[0][0]
    cursor.execute('Delete FROM `students` where id= "'+id+'"')
    cursor.execute('Delete FROM `eventregistrations` where studentId= "'+sid+'"')
    cursor.execute('Delete FROM `jobregistrations` where studentid= "'+sid+'"')
    cursor.execute('Delete FROM `bloodregistrations` where studentid= "'+sid+'"')
    connection.commit()
    return renderAdminShowStudents(request)
@csrf_exempt
def insertNewEvent(request):
    title=request.POST['title']
    description=request.POST['description']
    date=request.POST['date']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO `events`( `eventTitle`, `eventDescription`, `eventDate`) VALUES ("'+title+'", "'+description+'", "'+date+'")')
    connection.commit()
    return renderAdminShowEvents(request)
@csrf_exempt
def deleteEventData(request):
    id=request.POST['id']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('Delete FROM `events` where id= "'+id+'"')
    connection.commit()
    return renderAdminShowEvents(request)
@csrf_exempt
def insertNewJob(request):
    position=request.POST['title']
    description=request.POST['description']
    lastdate=request.POST['date']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO `jobs`( `position`, `description`, `lastdate`) VALUES ("'+position+'", "'+description+'", "'+lastdate+'")')
    connection.commit()
    return HttpResponse('Success')
@csrf_exempt
def deleteJobData(request):
    id=request.POST['id']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('Delete FROM `jobs` where id= "'+id+'"')
    connection.commit()
    return renderAdminShowJobs(request)
@csrf_exempt
def insertNewBlood(request):
    blood=request.POST['blood']
    number=request.POST['contact']
    name=request.POST['name']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO `requirement`(`requirement`, `contactnumber`,recipient) VALUES  ("'+blood+'", "'+number+'", "'+name+'")')
    connection.commit()
    return HttpResponse('Success')
def showAllFeedbacks(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT f.id,s.name,f.feedback FROM `feedbacks` f JOIN students s on s.id=f.studentid')
    feedbacks=cursor.fetchall()
    return render(request,'adminShowAllFeedbacks.html',{'feedbacks':feedbacks})
@csrf_exempt
def deleteFeedback(request):
    id=request.POST['id']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('delete from `feedbacks` where id="'+id+'"')
    connection.commit()
    return HttpResponse('Success')
@csrf_exempt
def renderStudentsList(request):
    id=request.GET['id']
    table=request.GET['type']
    back=request.GET['back']
    if table=='jobregistrations':
        val='jobid'
    else:
        val='eventId'
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT name from students s INNER JOIN '+table+' r on s.id = r.studentId where r.'+val+'="'+id+'"')
    students=cursor.fetchall()
    return render(request,'adminShowStudentsList.html',{'students':students,'back':back})
@csrf_exempt
def deleteBloodData(request):
    id=request.POST['id']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('Delete FROM `requirement` where id= "'+id+'"')
    connection.commit()
    return renderAdminShowBloods(request)

def renderStudentProfile(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    email=request.session['email']
    cursor.execute('SELECT * FROM `students` where email="'+email+'"')
    users=cursor.fetchall()
    return render(request,'studentProfile.html',{'data':users[0]})
def studentBlog(request):
    return render(request,'studentBlog.html')
def studentFeedback(request):
    return render(request,'studentFeedback.html')
def renderStudentHomePage(request,user='None'):
    if request.session['email']:
        email=request.session['email']
        connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM `students` where email="'+email+'"')
        user=cursor.fetchall()[0]
        return render(request,'studentHome.html',{'user':user})
    else:
        return renderAdminLogin()
def viewStudentDetails(request):  # returns all the details of students
    students=studentDetails.objects.all()
    return render(request,'studentDetails.html',{'studentDetails':students})
def viewJobs(request):
    return render(request,'studentJobs.html')
def renderStudentBlood(request):
    return render(request,'studentBlood.html')
def renderStudentJobs(request):
    email=request.session['email']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM `jobs` where lastdate>"'+today+'"')
    jobs=cursor.fetchall()
    jobslist=[]
    for i in range(len(jobs)):
        job=jobs[i]
        job=list(job)
        jobid=jobs[i][0]
        check=cursor.execute('SELECT `jobid`, `studentid` FROM `jobregistrations` WHERE jobid='+str(jobid)+' AND studentId=(SELECT id from students WHERE email="'+email+'")')
        check=cursor.fetchall()
        if len(check)==0:
            job.append('false')
        else:
            job.append('true')
        jobslist.append(job)
    cursor.close()
    return render(request,'studentJobs.html',{'jobs':jobslist})
@csrf_exempt
def insertStudentFeedback(request):
    email=request.session['email']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    data=request.GET['feedback']
    print('INSERT INTO feedbacks(studentid,feedback) SELECT id,"'+data+'" FROM students WHERE email="'+email+'"')
    cursor.execute('INSERT INTO feedbacks(studentid,feedback) SELECT id,"'+data+'" FROM students WHERE email="'+email+'"')
    connection.commit()
    cursor.close()
    return HttpResponse('none')
def renderStudentEvents(request):
    email=request.session['email']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM `events` where eventDate>"'+today+'"')
    events=cursor.fetchall()
    eventslist=[]
    for i in range(len(events)):
        event=events[i]
        event=list(event)
        eventid=events[i][0]
        check=cursor.execute('SELECT `eventId`, `studentId` FROM `eventregistrations` WHERE eventId='+str(eventid)+' AND studentId=(SELECT id from students WHERE email="'+email+'")')
        check=cursor.fetchall()
        if len(check)==0:
            event.append('false')
        else:
            event.append('true')
        eventslist.append(event)
    cursor.close()
    return render(request,'studentEvents.html',{'events':eventslist})
@csrf_exempt
def applyStudentEvent(request):
    email=request.session['email']
    eventId=request.POST['eventid']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO `eventregistrations`(`eventId`, `studentId`) SELECT '+eventId+',s.id FROM students s where s.email="'+email+'"')
    connection.commit()
    cursor.close()
    return render(request,'studentEvents.html')
@csrf_exempt
def cancelStudentEvent(request):
    email=request.session['email']
    eventId=request.POST['eventid']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('DELETE FROM `eventregistrations` WHERE eventId='+str(eventId)+' AND studentId=(SELECT id from students WHERE email="'+email+'")')
    connection.commit()
    cursor.close()
    return render(request,'studentEvents.html')
@csrf_exempt
def applyStudentJob(request):
    email=request.session['email']
    jobId=request.POST['jobid']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO `jobregistrations`(`jobId`, `studentId`) SELECT '+jobId+',s.id FROM students s where s.email="'+email+'"')
    connection.commit()
    cursor.close()
    return render(request,'studentJobs.html')
@csrf_exempt
def cancelStudentJob(request):
    email=request.session['email']
    jobId=request.POST['jobid']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('DELETE FROM `jobregistrations` WHERE jobId='+str(jobId)+' AND studentId=(SELECT id from students WHERE email="'+email+'")')
    connection.commit()
    cursor.close()
    return render(request,'studentJobs.html')
def addStudentDetails(request):
    name=request.POST['name']
    phone=request.POST['phone']
    email=request.POST['email']
    newStudentData=studentDetails(name,email,phone)
    newStudentData.save()
    return render(request,'adminHome.html',{'status':'Student Data Successfully added'})
@csrf_exempt
def updateStudentProfile(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    name=request.POST['name']
    phone=request.POST['phone']
    email=request.POST['email']
    password=request.POST['password']
    print(name,phone,email,password)
    print("UPDATE `students` SET `name`='"+name+"',`email`='"+email+"',`password`='"+password+"',`phone`='"+phone+"' WHERE id='"+str(id)+"'")
    cursor.execute("UPDATE `students` SET `name`='"+name+"',`email`='"+email+"',`password`='"+password+"',`phone`='"+phone+"' WHERE id='"+str(id)+"'")
    connection.commit()
    return render(request,'studentProfile.html')

def renderStudentBlogs(request):
    email=request.session['email']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute("SELECT b.*,s.email FROM blogs b LEFT JOIN students s on b.studentid=s.id")
    blogs=cursor.fetchall()
    cursor.close()
    return render(request,'studentBlogs.html',{'blogs':blogs})
def renderSingleBlog(request):
    email=request.session['email']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    blogid=request.GET['blogid']
    cursor.execute("SELECT b.*,s.email FROM blogs b LEFT JOIN students s on b.studentid=s.id where b.id='"+blogid+"'")
    blog=cursor.fetchall()[0]
    cursor.close()
    return render(request,'showsingleblog.html',{'blog':blog})
@csrf_exempt
def updateStudentBlog(request):
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    title=request.POST['title']
    desc=request.POST['desc']
    blogid=request.POST['id']
    print("UPDATE blogs SET ,blogtitle='"+title+"',blogcontent='"+desc+"' WHERE id='"+blogid+"'")
    cursor.execute("UPDATE blogs SET blogtitle='"+title+"',blogcontent='"+desc+"' WHERE id='"+blogid+"'")
    connection.commit()
    return HttpResponse('success')
@csrf_exempt
def deleteStudentBlog(request):
    id=request.POST['id']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    cursor.execute('Delete FROM `blogs` where id= "'+id+'"')
    connection.commit()
    return HttpResponse('success')

def renderStudentBlogForm(request):
    return render(request,'newBlogForm.html')
@csrf_exempt
def insertNewBlog(request):
    title=request.POST['title']
    desc=request.POST['desc']
    connection=mysql.connector.connect(host='localhost',user='root',password='',database='race')
    cursor=connection.cursor()
    email=request.session['email']
    cursor.execute("select id from students where email='"+email+"'")
    sid=cursor.fetchall()[0][0]
    sid=str(sid)
    cursor.execute("INSERT INTO blogs( blogtitle, blogcontent, studentid) VALUES ('"+title+"','"+desc+"','"+sid+"')")
    connection.commit()
    return HttpResponse('Success')
def a(request):
    return render(request,'adminLeftPane.html')