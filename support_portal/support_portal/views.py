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
        x= cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
        return render(request, 'update.html')


# def taskclosed(request):
#     if request.method == 'POST':
#         id = request.POST.get("id")
#         print(id)

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

        context = {'data': data,'user':x}
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
        return render(request, 'edit.html')

       # cursor = connection.cursor()
        #cursor.execute('UPDATE support_portal_userprofile set sr_name=sr_name,work_stream=work_stream,task=task,value_hml=value_hml,urgent_yn=urgent_yn,request_by_actor=request_by_actor,request_date=request_date,needed_date=needed_date,etd=etd,acd=acd,prog=prog,status=status,maker1=maker1,maker2=maker2,checker=checker,maker1time=maker1time,maker2time=maker2time,checker_time=checker_time,mahid_time=mahid_time,outside_office_time=outside_office_time,url=url,remarks=remarks,task_details=task_details,email=email,add_to_google=add_to_google,task_id=task_id  WHERE task_id= %s', [task_id])
       # cursor.execute('UPDATE support_portal_userprofile SET sr_name= WHERE task_id= %s', [task_id])
       #  data = cursor.fetchall()
       #  context = {'data': data}
       #  return render(request, 'edit.html', context)

# @login_required
# def lastupdate(request):
#     if request.method == 'POST':
#         sr_name = request.POST.get("sr_name")
#         work_stream = request.POST.get("work_stream")
#         remarks = request.POST.get("remarks")
#         task = request.POST.get("task")
#         value_hml = request.POST.get("value_hml")
#         urgent_yn = request.POST.get("urgent_yn")
#         request_date = request.POST.get("request_date")
#         needed_date = request.POST.get("needed_date")
#         etd = request.POST.get("etd")
#         acd = request.POST.get("acd")
#         request_by_actor = request.POST.get("request_by_actor")
#         prog = request.POST.get("prog")
#         status = request.POST.get("status")
#         maker1 = request.POST.get("maker1")
#         maker2 = request.POST.get("maker2")
#         checker = request.POST.get("checker")
#         maker1time = request.POST.get("maker1time")
#         maker2time = request.POST.get("maker2time")
#         checker_time = request.POST.get("checker_time")
#         mahid_time = request.POST.get("mahid_time")
#         outside_office_time = request.POST.get("outside_office_time")
#         url = request.POST.get("url")
#         task_details = request.POST.get("task_details")
#         email = request.POST.get("email")
#         add_to_google = request.POST.get("add_to_google")
#         task_id = request.POST.get("task_id")
#         print(email)
#         print(task_details)
#         print(work_stream)
#         cursor = connection.cursor()
#         #x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,remarks= %s WHERE task_id= %s", [update_data1, latest_update, update_data2])
#         #y = cursor.execute("INSERT INTO support_portal_userprofile (acd= %s, add_to_google= %s, checker= %s, checker_time= %s, email= %s, etd= %s, mahid_time= %s, maker1= %s, maker1time= %s, maker2= %s, maker2time= %s, needed_date= %s, outside_office_time= %s, prog= %s, remarks= %s, request_by_actor= %s, request_date= %s, sr_name= %s, status= %s, task= %s, task_details= %s, urgent_yn= %s, url= %s, value_hml= %s, work_stream= %s, task_id= %s)", [acd, add_to_google, checker, checker_time, email, etd, mahid_time, maker1, maker1time, maker2, maker2time, needed_date, outside_office_time, prog, remarks, request_by_actor, request_date, sr_name, status, task, task_details, urgent_yn, url, value_hml, work_stream, task_id])
#         z = cursor.execute("INSERT INTO support_portal_userprofile (acd, add_to_google, checker, checker_time, email, etd, mahid_time, maker1, maker1time, maker2, maker2time, needed_date, outside_office_time, prog, remarks, request_by_actor, request_date, sr_name, status, task, task_details, urgent_yn, url, value_hml, work_stream, task_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [acd, add_to_google, checker, checker_time, email, etd, mahid_time, maker1, maker1time, maker2, maker2time, needed_date, outside_office_time, prog, remarks, request_by_actor, request_date, sr_name, status, task, task_details, urgent_yn, url, value_hml, work_stream, task_id])
#         print(z)
#         return render(request, 'report.html')

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
        return render(request, 'update.html', context)


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


# def sample(request):
#     return render(request, 'sample.html')


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
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE employee_id = %s and status='Pending'", [employee_id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        info = cursor.fetchall()
        context = {'data': data, 'info': info}
        return render(request, 'taskstatus.html',  context)


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

            if group == 'data':
                return redirect('newticket')

            # if group == 'systems':
            #     return redirect('newticket')

            # return redirect('dashboard')
            return redirect('index')

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
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval) VALUES (%s, %s,  %s, %s, %s)",[employee_id, task, comment,request_date,approval])
        # if y:
        #     with open('media', 'wb+') as destination:
        #         for chunk in f.chunks():
        #             destination.write(chunk)
        # task_id= cursor.execute('select id from support_portal_userprofile where id= %s')

        messages.success(request, "Ticket entry successfully..!!")
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
    user = request.POST.get("employee_id")
    print(user)

    id = request.POST.get("id")
    print(id)



    cursor = connection.cursor()
    cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE (approval="Not Started yet" or approval= "On Going" or approval= "Complete") and employee_id= %s order by request_date DESC',[user])
    #cursor.execute('SELECT * FROM support_portal_userprofile WHERE approval="Waiting_For_Appoval" and employee_id= "{{ user }}"')
    data = cursor.fetchall()
    # print(data)


    # cursor.execute('SELECT latest_update from support_portal_infoupdate where task_id= %s ORDER BY update_date DESC limit 1',)
    # lastUpdate= cursor.fetchall()
    # print(lastUpdate)
    # cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s ORDER BY update_date DESC limit 1',[id])
    # lastupdate= cursor.fetchall()
    # print("Lastdate"+lastupdate)

    context = {'data': data}
    #return render(request, 'customerTicketStatus.html', context)
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
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and employee_id= %s', [status,employee_id])
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
        # return render(request, 'approved.html', context)
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
    if request.method == 'POST':
        # form_date = request.POST.get("form_date")
        # to_date = request.POST.get("to_date")
        # print(form_date)
        # print(to_date)
        cursor = connection.cursor()
        cursor.execute('select *,datediff(etd,current_date) as pending_days from support_portal_userprofile where approval= "Not Started yet" or approval="On Going" order by request_date DESC')
        data = cursor.fetchall()
        print(data)
        context = {'data': data}
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
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval) VALUES (%s, %s,  %s, %s, %s)",[employee_id, task, comment,request_date,approval])
        # if y:
        #     with open('media', 'wb+') as destination:
        #         for chunk in f.chunks():
        #             destination.write(chunk)
        # task_id= cursor.execute('select id from support_portal_userprofile where id= %s')

        messages.success(request, "Ticket entry successfully..!!")

        return render(request, 'sysnewticket.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")




def test(request):
    return render(request, 'test.html')


