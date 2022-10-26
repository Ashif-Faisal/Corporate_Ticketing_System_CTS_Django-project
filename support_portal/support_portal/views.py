import os
import requests
import mysql.connector
from bs4 import BeautifulSoup
from datetime import date
from tabulate import tabulate
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import userProfileForm, createUserForm
from .functions import handle_uploaded_file
from .models import userprofile
from .serializers import PatientSerializer
from django.contrib.auth import logout
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.base import MIMEBase
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def _send_mail(my_body, employee, comment, id, team, creatoremail,latest_update):
        message = MIMEMultipart()
        # filename = ''
        # # attachment = open(os.path.dirname(os.path.abspath("__file__")), "rb")
        # attachment = ''
        # p = MIMEBase('application', 'octet-stream')
        # p.set_payload((attachment).read())
        # encoders.encode_base64(p)  # updated
        # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        # message.attach(p)
        sample_str = str(my_body)
        require_chars = sample_str[0:50]
        print(team)
        creatorEmail= creatoremail
        task_id = id
        message['Subject'] = '[TT- '+str(task_id)+'] ''' +require_chars
        message['From'] = 'sys.support@progoti.com'
        To_receiver = [team]
        Cc_receiver = [creatoremail]
        message['To'] = ";".join(To_receiver)
        message['Cc'] = ";".join(Cc_receiver)
        print(message['Cc'])
        receiver = To_receiver + Cc_receiver

        body = ''' Ticket Initiated by: <br>'''+ str(employee)+ ''' <br><br>Details: <br>'''+ sample_str+'''<br><br> Comments: <br>'''+str(comment)+'''<br><br> Last Updae: <br>'''+str(latest_update)
        message.attach(MIMEText(body, "html"))
        msg_body = message.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(message['From'], 'dzyofyvrmljnseby')
        server.sendmail(message['From'], receiver, msg_body)
        server.quit()
        return "Mail sent successfully."


@login_required
def Tasksearch(request):
    task_list = userprofile.objects.all()
    user_filter = userprofile(request.GET, work_Stream=task_list)
    return render(request, 'taskview1.html', {'filter': user_filter})


@login_required
def action(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print("ok")
        cursor = connection.cursor()
       # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s', [task])
        x = cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
    return render(request, 'unassignTask.html')

@login_required
def edit(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        context = {'data': data,'owner':x}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'edit.html', context)

@login_required
def editupdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        sr_name = request.POST.get("sr_name")
        work_stream = request.POST.get("work_stream")
        task = request.POST.get("task")
        value_hml = request.POST.get("value_hml")
        urgent_yn = request.POST.get("urgent_yn")
        request_by_actor = request.POST.get("request_by_actor")
        needed_date = request.POST.get("needed_date")
        etd = request.POST.get("etd")
        status = request.POST.get("status")
        maker1 = request.POST.get("maker1")
        maker2 = request.POST.get("maker2")
        checker = request.POST.get("checker")
        outside_office_time = request.POST.get("outside_office_time")
        add_to_google = request.POST.get("add_to_google")
        approval = request.POST.get("approval")
        cursor = connection.cursor()
        x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,work_stream= %s, task= %s, value_hml= %s, urgent_yn= %s,request_by_actor= %s,needed_date= %s,etd= %s,status= %s,maker1= %s,maker2= %s,checker= %s,outside_office_time= %s,add_to_google= %s,approval= %s  WHERE id= %s", [sr_name, work_stream,task, value_hml,urgent_yn,request_by_actor,needed_date,etd,status,maker1,maker2,checker,outside_office_time,add_to_google,approval, id])
        # y = cursor.execute('SELECT * FROM support_portal_userprofile WHERE task_id=')
        if x:
            messages.success(request, "Assigned successfully..!!")
        print(x)
        return render(request, 'edit.html')


@login_required
def lastupdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data,'user':x, 'report': report, 'current_datetime':current_datetime}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'update.html', context)


# def ticketLastUpdate(request):
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s ORDER BY update_date DESC limit 1', [task_id])
#     report = cursor.fetchall()
#     print(report)
#     context = {'info': report}
#     return render(request, 'customerTicketStatus.html',context)

@login_required
def updateinfo(request):
    if request.method == 'POST':
        latest_update = request.POST.get("task_details")
        task = request.POST.get("task")
        task_id = request.POST.get("id")
        update_date = request.POST.get("update_Date")
        comment = request.POST.get("comment")

        user=  request.user
        print(user)
        # user = request.POST.get("{{ user }}")
        # print("Ok"+user)
        # print(latest_update)
        # print(task_id)
        # print(update_date)
        cursor = connection.cursor()
        y= cursor.execute("INSERT INTO support_portal_infoupdate (latest_update, task_id, update_Date) VALUES (%s, %s, %s)",[latest_update, task_id, update_date])
        if y:
            messages.success(request, "Last update entry successfully..!!")

        cursor.execute("UPDATE support_portal_userprofile SET approval= 'On Going', maker1= %s WHERE id= %s", [user,task_id])

        user = request.user
        print(user)


        cursor.execute('select email from auth_user where username= %s', [user])
        email = cursor.fetchall()
        for email in email:
            print(email[0])
        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        team='systems@surecash.net'




        print(latest_update)
        print(user)
        print(task_id)
        print(creatoremail)
        print(comment)

        _send_mail(task, user,comment, task_id,team, creatoremail,latest_update)
        context = {'updatedata': y}
        return render(request, 'unassignTask.html', context)


@login_required
def details(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [id])
        data = cursor.fetchall()
        context = {'data': data}
        return render(request, 'details.html', context)

@login_required
def delete(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        x= cursor.execute('DELETE FROM support_portal_userprofile WHERE id= %s', [id])
        if x:
            messages.success(request, "Task Deleted Successfully..!!")
        return render(request, 'taskview1.html')


def taskInput(request):
    return render(request,'taskinput.html')


def homepage(request):
    return render(request, 'home.html')


def sample1(request):
    return render(request, 'sample1.html')


def taskview1(request):
    return render(request, 'taskview1.html')

@login_required
def taskstatusPerson(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM auth_user')
        data = cursor.fetchall()
        context = {'data': data}
        print(data)
        return render(request, 'taskstatusPerson.html',context)

@login_required
def taskstatus(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM auth_user')
        data = cursor.fetchall()
        context = {'info': data}
        print(data)
        # return render(request, 'taskstatusPerson.html', context)
        return render(request, 'taskstatus.html', context)

@login_required
def taskview(request):
    if request.method == 'POST':

        work_stream=request.POST.get("work_stream")
        print(work_stream)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE work_stream= %s ', [work_stream])
        data = cursor.fetchall()

        context = {'data': data}
        return render(request, 'taskview1.html',  context)

@login_required
def searchview(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        cursor = connection.cursor()
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        info = cursor.fetchall()
        context = {'data': data, 'info': info}
        return render(request, 'taskstatus.html',  context)


def diff_time(created_date, cursor):
    current_date = datetime.now()
    for item in created_date:
        x = item[0].strftime("%Y-%m-%d")
        cursor.execute(f'''select datediff('{current_date}','{x}') from support_portal_userprofile''')
        yield cursor.fetchall()


@login_required
def pendingTask(request):
    if request.method == 'POST':

        employee_id=request.POST.get("employee_id")
        print(employee_id)
        cursor = connection.cursor()
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE maker1 = %s and status='Pending'", [employee_id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        alluser = cursor.fetchall()
        context = {'data': data, 'alluser': alluser}
        return render(request, 'unassignTask.html',  context)


# def pendingTask(request):
#     if request.method == 'POST':
#
#         pendingTask = request.POST.get("Pending")
#         userlist = userprofile.objects.filter(status=pendingTask)
#         context = {'data': userlist}
#         return render(request, 'pendingTask.html', context)


def search(request):
    return render(request, 'search.html')


def wellcome(request):
    return render(request, 'wellcome.html')

@login_required
def get_all_patient_info(request):
    # get all data from database
    all_patient_info = userprofile.objects.all()
    serializer = PatientSerializer(all_patient_info, many=True)
    return JsonResponse(serializer.data, safe=False)


# def report3(request):
#     cursor=connection.cursor()
#     cursor.execute('SELECT * FROM support_portal_userprofile')
#     userlist= cursor.fetchall()
#     context = {'data': userlist}
#     return render(request, 'report3.html', context)

# def report3(request):
#     datalist = userprofile.objects.all()
#     context = {'data': datalist}
#     return render(request, 'report3.html', context)

#
@login_required
def report2(request, acd):
    userlist=userprofile.objects.filter(acd=acd)
    context = {'data': userlist}
    return render(request, 'report.html', context)

@login_required
def report(request):
    userlist = userprofile.objects.all()
    context = {'data': userlist}
    return render(request, 'report3.html', context)

@login_required
def regview(request):
    form = createUserForm()

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'userReg.html', context)


def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
            if group == 'systems':
                return redirect('sysnewticket')

            if group == 'DataTeam':
                return redirect('dataticket')

            if group == 'TechOps':
                return redirect('techticket')

            # if group == 'systems':
            #     return redirect('newticket')

            # return redirect('dashboard')
            return redirect('newticket')

        else:
            messages.success(request, "Incorrect Username or Password..")

    context = {}
    return render(request, 'login.html', context)


def bootstrap(request):
    return render(request, 'boot.html')


def testpage(request):
    return render(request, 'test.html')


def errorpage(request):
    return render(request, 'error.html')

@login_required
def newticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'newticket.html',context)


@login_required
def indexview(request):
    return render(request, 'index.html')


# @login_required
# @login_required(views.loginview())
@login_required
def infoview(request):
    form = userProfileForm()
    if request.method == 'POST':
        print(request.POST)
        form = userProfileForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            if form.save():
                messages.success(request, "Task Added Successfully..!!")

    cursor = connection.cursor()
    cursor.execute('SELECT username FROM auth_user')
    x = cursor.fetchall()

    #current_datetime = datetime.now()

    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'form': form, 'data': x,'current_datetime': current_datetime}
    return render(request, 'info.html', context)


# def saveticket(request):
#     form = newticket()
#     if request.method == 'POST':
#         print(request.POST)
#         form = newticket(request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             if form.save():
#                 messages.success(request, "Task Added Successfully..!!")
#
#     cursor = connection.cursor()
#     cursor.execute('SELECT username FROM auth_user')
#     x = cursor.fetchall()
#
#     context = {'form': form, 'data': x}
#     return render(request, 'newticket.html', context)


def saveticket(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        # attachment = request.POST.get("attachment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        x= cursor.execute("INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team) VALUES (%s, %s,  %s, %s, %s, %s)",[employee_id, task, comment,request_date,approval, team])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id= i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s',[employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail= email[0]
        print("creatoremailll"+creatoremail)

        latest_update=''

        messages.success(request, "Ticket entry successfully..!!")
        if team == 'systems':
            team = 'systems@surecash.net'
        elif team=='TechOps':
            team = 'tech_ops@surecash.net'
        elif team=='DataTeam':
            team = 'data@surecash.net'
        _send_mail(task, employee_id, comment, id, team,creatoremail,latest_update)
        return render(request, 'newticket.html')

#
# def task_id(request):
#     if request.method == 'POST':
#         cursor = connection.cursor()
#         cursor.execute('select id from support_portal_userprofile')
#         data = cursor.fetchall()
#         print(data)
#
#     return render(request, 'newticket.html')


def approved(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'approved.html',context)


def todayticket(request):
    if request.method == 'POST':

        cursor = connection.cursor()
        cursor.execute("select * from support_portal_userprofile where current_date and current_date order by request_date")
        data = cursor.fetchall()
        print(data)
        context = {'data': data}
        return render(request, 'approved.html',context)


@login_required
def datewiseticket(request):
    if request.method == 'POST':
        form_date = request.POST.get("form_date")
        to_date = request.POST.get("to_date")
        print(form_date)
        print(to_date)
        cursor = connection.cursor()
        cursor.execute('select * from support_portal_userprofile where request_date>= %s and request_date<= %s order by request_date DESC',[form_date, to_date])
        data = cursor.fetchall()
        print(data)
        context = {'data': data}
        return render(request, 'approved.html',context)


@login_required
def customerTicketStatus(request):
    user = request.user
    print(user)





    cursor = connection.cursor()
    cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE (approval="Not Started yet" or approval= "On Going" or approval= "Complete") and employee_id= %s order by request_date DESC',[user])
    data = cursor.fetchall()
    context = {'data': data}
    return render(request, 'customerTicketStatus.html',context)


# def all_id(request):
#
#     cursor = connection.cursor()
#     # cursor.execute('SELECT id from support_portal_userprofile')
#     # all_id= cursor.fetchall()
#     # print(all_id)




@login_required
def customerTicketInfo(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and employee_id= %s and team="systems"', [status,employee_id])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        # return render(request, 'approved.html', context)
        return render(request, 'customerTicketStatus.html',context)

@login_required
def TicketStatus(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        return render(request, 'unassignTask.html',context)

@login_required
def customerTaskView(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data,'user':x, 'report': report, 'current_datetime':current_datetime}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'customerTaskView.html', context)
       # return render(request,'customerTaskView.html')

@login_required
def customerTicketApproval(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        print(employee_id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE approval="Waiting_For_Appoval" and employee_id= %s',[employee_id])
        data = cursor.fetchall()
        print(data)
        context = {'approval': data}
        return render(request, 'customerTicketStatus.html', context)

@login_required
def unassignTask(request):

    user = request.POST.get("employee_id")
    print(user)
    id = request.POST.get("id")
    print(id)

    cursor = connection.cursor()
    cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left join (select	* from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE team="systems" and (approval="Not Started yet" or approval= "On Going") order by request_date DESC;')
    data = cursor.fetchall()
    cursor.execute('select username from auth_user')
    alluser = cursor.fetchall();
    print(alluser)

    context = {'data': data,'alluser': alluser}
    return render(request, 'unassignTask.html', context)

    cursor.execute('select username from auth_user')
    alluser = cursor.fetchall();
    print(alluser)

    context = {'data': data,'alluser': alluser}
    return render(request, 'unassignTask.html', context)


@login_required
def pendingTicket(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        cursor = connection.cursor()
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status='Pending'")
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        info = cursor.fetchall()
        context = {'data': data, 'info': info}
        return render(request, 'pendingTicket.html',  context)

@login_required
def allTask(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE status= %s')
        data = cursor.fetchall()
        context = {'data': data}
        return render(request, 'taskstatus.html',  context)

@login_required
def sysnewticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'sysnewticket.html', context)

@login_required
def SysTicketSaved(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        # attachment = request.POST.get("attachment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team) VALUES (%s, %s,  %s, %s, %s, %s)",
            [employee_id, task, comment, request_date, approval, team])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id = i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s', [employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        messages.success(request, "Ticket entry successfully..!!")
        if team == 'systems':
            team = 'systems@surecash.net'
        elif team == 'TechOps':
            team = 'tech_ops@surecash.net'
        elif team == 'DataTeam':
            team = 'data@surecash.net'

        latest_update=''
        _send_mail(task, employee_id, comment, id, team, creatoremail,latest_update)
        return render(request, 'sysnewticket.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def test(request):
    return render(request, 'test.html')


def techTicketStatus(request):
    user = request.POST.get("employee_id")
    print(user)

    id = request.POST.get("id")
    print(id)

    cursor = connection.cursor()
    cursor.execute(
        'SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE team="TechOps" or (approval="Not Started yet" or approval= "On Going" or approval= "Complete")  and employee_id= %s order by request_date DESC',
        [user])
    data = cursor.fetchall()
    context = {'data': data}
    return render(request, 'techTicketStatus.html', context)


def techAssignedTicket(request):
    cursor = connection.cursor()
    cursor.execute('select *,datediff(etd,current_date) as pending_days from support_portal_userprofile where (approval= "Not Started yet" or approval="On Going") and team="TechOps" order by request_date DESC')
    data = cursor.fetchall()
    print(data)
    context = {'data': data}
    return render(request, 'techAssignedTicket.html', context)


def dataticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'dataticket.html', context)


def techticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'techticket.html', context)

def techTicketsave(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        # attachment = request.POST.get("attachment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team) VALUES (%s, %s,  %s, %s, %s, %s)",
            [employee_id, task, comment, request_date, approval, team])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id = i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s', [employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        messages.success(request, "Ticket entry successfully..!!")
        if team == 'systems':
            team = 'systems@surecash.net'
        elif team == 'TechOps':
            team = 'tech_ops@surecash.net'
        elif team == 'DataTeam':
            team = 'data@surecash.net'
        _send_mail(task, employee_id, comment, id, team, creatoremail)
        return render(request, 'techticket.html')

def techEdit(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        context = {'data': data,'owner':x}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'techEdit.html', context)

def techEditUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        sr_name = request.POST.get("sr_name")
        work_stream = request.POST.get("work_stream")
        task = request.POST.get("task")
        value_hml = request.POST.get("value_hml")
        urgent_yn = request.POST.get("urgent_yn")
        request_by_actor = request.POST.get("request_by_actor")
        needed_date = request.POST.get("needed_date")
        etd = request.POST.get("etd")
        status = request.POST.get("status")
        maker1 = request.POST.get("maker1")
        maker2 = request.POST.get("maker2")
        checker = request.POST.get("checker")
        outside_office_time = request.POST.get("outside_office_time")
        add_to_google = request.POST.get("add_to_google")
        approval = request.POST.get("approval")
        # print(sr_name)
        # print(work_stream)
        # print(task)
        # print(value_hml)
        # print(request_by_actor)
        # print(request_date)
        # print(needed_date)
        # print(etd)
        # print(acd)
        # print(status)
        # print(maker1)
        # print(maker2)
        # print(checker)
        # print(outside_office_time)
        # print(add_to_google)
        cursor = connection.cursor()
        x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,work_stream= %s, task= %s, value_hml= %s, urgent_yn= %s,request_by_actor= %s,needed_date= %s,etd= %s,status= %s,maker1= %s,maker2= %s,checker= %s,outside_office_time= %s,add_to_google= %s,approval= %s  WHERE id= %s", [sr_name, work_stream,task, value_hml,urgent_yn,request_by_actor,needed_date,etd,status,maker1,maker2,checker,outside_office_time,add_to_google,approval, id])
        # y = cursor.execute('SELECT * FROM support_portal_userprofile WHERE task_id=')
        if x:
            messages.success(request, "Assigned successfully..!!")

        print(x)
        return render(request, 'techEdit.html')



def techTicketLastUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data,'user':x, 'report': report, 'current_datetime':current_datetime}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'techUpdatePage.html', context)


def techUpdatePage(request):
    if request.method == 'POST':
        latest_update = request.POST.get("task_details")
        task_id = request.POST.get("id")
        update_date = request.POST.get("update_Date")

        user=  request.user
        print(user)
        # user = request.POST.get("{{ user }}")
        # print("Ok"+user)
        # print(latest_update)
        # print(task_id)
        # print(update_date)
        cursor = connection.cursor()
        y= cursor.execute("INSERT INTO support_portal_infoupdate (latest_update, task_id, update_Date) VALUES (%s, %s, %s)",[latest_update, task_id, update_date])
        if y:
            messages.success(request, "Last update entry successfully..!!")

        cursor.execute("UPDATE support_portal_userprofile SET approval= 'On Going', maker1= %s WHERE id= %s", [user,task_id])

        context = {'updatedata': y}
        return render(request, 'techTicketStatus.html', context)


def dataTicketSave(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        # attachment = request.POST.get("attachment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team) VALUES (%s, %s,  %s, %s, %s, %s)",
            [employee_id, task, comment, request_date, approval, team])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id = i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s', [employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        messages.success(request, "Ticket entry successfully..!!")
        if team == 'systems':
            team = 'systems@surecash.net'
        elif team == 'TechOps':
            team = 'tech_ops@surecash.net'
        elif team == 'DataTeam':
            team = 'data@surecash.net'
        _send_mail(task, employee_id, comment, id, team, creatoremail)
        return render(request, 'dataticket.html')



def dataTicketStatus(request):
    user = request.POST.get("employee_id")
    print(user)

    id = request.POST.get("id")
    print(id)

    cursor = connection.cursor()
    cursor.execute(
        'SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE team="DataTeam" or (approval="Not Started yet" or approval= "On Going" or approval= "Complete")  and employee_id= %s order by request_date DESC',
        [user])
    data = cursor.fetchall()
    context = {'data': data}
    return render(request, 'dataTicketStatus.html', context)


def dataEdit(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        context = {'data': data,'owner':x}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'dataEdit.html', context)


def dataEditUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        sr_name = request.POST.get("sr_name")
        work_stream = request.POST.get("work_stream")
        task = request.POST.get("task")
        value_hml = request.POST.get("value_hml")
        urgent_yn = request.POST.get("urgent_yn")
        request_by_actor = request.POST.get("request_by_actor")
        needed_date = request.POST.get("needed_date")
        etd = request.POST.get("etd")
        status = request.POST.get("status")
        maker1 = request.POST.get("maker1")
        maker2 = request.POST.get("maker2")
        checker = request.POST.get("checker")
        outside_office_time = request.POST.get("outside_office_time")
        add_to_google = request.POST.get("add_to_google")
        approval = request.POST.get("approval")

        cursor = connection.cursor()
        x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,work_stream= %s, task= %s, value_hml= %s, urgent_yn= %s,request_by_actor= %s,needed_date= %s,etd= %s,status= %s,maker1= %s,maker2= %s,checker= %s,outside_office_time= %s,add_to_google= %s,approval= %s  WHERE id= %s", [sr_name, work_stream,task, value_hml,urgent_yn,request_by_actor,needed_date,etd,status,maker1,maker2,checker,outside_office_time,add_to_google,approval, id])
        # y = cursor.execute('SELECT * FROM support_portal_userprofile WHERE task_id=')
        if x:
            messages.success(request, "Assigned successfully..!!")

        print(x)
        return render(request, 'dataEdit.html')


def dataTicketLastUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data, 'user': x, 'report': report, 'current_datetime': current_datetime}
        # cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'dataUpdatePage.html', context)


def dataUpdatePage(request):
    if request.method == 'POST':
        latest_update = request.POST.get("task_details")
        task_id = request.POST.get("id")
        update_date = request.POST.get("update_Date")

        user=  request.user
        print(user)
        cursor = connection.cursor()
        y= cursor.execute("INSERT INTO support_portal_infoupdate (latest_update, task_id, update_Date) VALUES (%s, %s, %s)",[latest_update, task_id, update_date])
        if y:
            messages.success(request, "Last update entry successfully..!!")

        cursor.execute("UPDATE support_portal_userprofile SET approval= 'On Going', maker1= %s WHERE id= %s", [user,task_id])

        context = {'updatedata': y}
        return render(request, 'dataTicketStatus.html', context)



def techTicketState(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and team='TechOps'", [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        # return render(request, 'approved.html', context)
        return render(request, 'techTicketState.html',context)


def dataTicketState(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and team='DataTeam'", [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        # return render(request, 'approved.html', context)
        return render(request, 'dataTicketState.html',context)



def sysTicketState(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and team='systems'", [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        cursor.execute('select username from auth_user')
        alluser = cursor.fetchall();
        print(alluser)

        context = {'data': data,'alluser':alluser}
        # return render(request, 'approved.html', context)
        return render(request, 'sysTicketState.html',context)


def actionForData(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print("ok")
        cursor = connection.cursor()
       # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s', [task])
        x= cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
    return render(request, 'dataTicketStatus.html')


def actionForTech(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print("ok")
        cursor = connection.cursor()
       # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s', [task])
        x= cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
    return render(request, 'techTicketStatus.html')
