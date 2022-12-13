"""support_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings #add this
from django.conf.urls.static import static #add this

from django.conf import settings
from django.conf.urls.static import static


from .import views
from .views import infoview

urlpatterns = [
    path('', views.loginview, name='login'),
    path('admin/', admin.site.urls),
    path('info', views.infoview, name='info'),
    path('test',views.testpage, name='test'),
    path('error', views.errorpage, name='errorpage'),
    path('report', views.report, name='report'),
    path('reg', views.regview, name='regpage'),
    path('get_all_info', views.get_all_patient_info),
    path('report2/<str:acd>', views.report2, name='report2'),
    path('search', views.search, name='search'),
    path('searchview', views.searchview, name='searchview'),
    path('pendingtask', views.pendingTask, name='pendingtask'),
    path('taskview', views.taskview, name='taskview'),
    path('taskview1', views.taskview1, name='taskview1'),
    path('home', views.homepage, name='homepage'),
    path('taskinput', views.taskInput, name='taskinput'),
    path('index', views.indexview, name='index'),
    path('taskstatus', views.taskstatus, name='taskreport'),
    path('taskstatusPerson', views.taskstatusPerson, name='taskReportPerson'),
    path('wellcome', views.wellcome, name='wellcome'),
    path('action', views.action, name='action'),
    #path('taskclosed', views.taskclosed, name='taskclosed'),
    path('edit', views.edit, name='edit'),
    path('editupdate', views.editupdate, name='editupdate'),
    path('delete', views.delete, name='delete'),
    path('lastupdate', views.lastupdate, name='lastupdate'),
    path('details', views.details, name='details'),
    path('updateinfo', views.updateinfo, name='updateinfo'),
    path('Tasksearch', views.Tasksearch, name='Tasksearch'),
    path('newticket', views.newticket, name='newticket'),
    path('saveticket', views.saveticket, name='saveticket'),
    path('approved', views.approved, name='approved'),
    path('todayticket', views.todayticket, name='todayticket'),
    path('datewiseticket', views.datewiseticket, name='datewiseticket'),
    path('customerTicketStatus', views.customerTicketStatus, name='customerTicketStatus'),
    path('customerTicketInfo', views.customerTicketInfo, name='customerTicketInfo'),
    path('customerTaskView', views.customerTaskView, name='customerTaskView'),
    path('customerTicketApproval', views.customerTicketApproval, name='customerTicketApproval'),
    # path('unassignTask', views.unassignTask, name='unassignTask'),
    path('unassignTask', views.unassignTask, name='unassignTask'),
    path('unassignTaskV2', views.filterTask, name='unassignTaskV2'),
    path('pendingTicket', views.pendingTicket, name='pendingTicket'),
    path('allTask', views.allTask, name='allTask'),
    #path('test2', views.test2, name='test2'),
    path('TicketStatus', views.TicketStatus, name='TicketStatus'),
    path('sysnewticket', views.sysnewticket, name='sysnewticket'),
    path('SysTicketSaved', views.SysTicketSaved, name='SysTicketSaved'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('test', views.test, name='test'),
    path('sample1', views.sample1, name='sample1'),
    path('_send_mail', views._send_mail, name='_send_mail'),
    path('techticket', views.techticket, name='techticket'),
    path('techTicketStatus', views.techTicketStatus, name='techTicketStatus'),
    path('techAssignedTicket', views.techAssignedTicket, name='techAssignedTicket'),
    path('dataticket', views.dataticket, name='dataticket'),
    path('techTicketsave', views.techTicketsave, name='techTicketsave'),
    path('techEdit', views.techEdit, name='techEdit'),
    path('techEditUpdate', views.techEditUpdate, name='techEditUpdate'),
    path('techTicketLastUpdate', views.techTicketLastUpdate, name='techTicketLastUpdate'),
    path('techTicketLastUpdate', views.techTicketLastUpdate, name='techTicketLastUpdate'),
    path('techUpdatePage', views.techUpdatePage, name='techUpdatePage'),
    path('dataTicketSave', views.dataTicketSave, name='dataTicketSave'),
    path('dataTicketStatus', views.dataTicketStatus, name='dataTicketStatus'),
    path('dataEdit', views.dataEdit, name='dataEdit'),
    path('dataEditUpdate', views.dataEditUpdate, name='dataEditUpdate'),
    path('dataTicketLastUpdate', views.dataTicketLastUpdate, name='dataTicketLastUpdate'),
    path('dataUpdatePage', views.dataUpdatePage, name='dataUpdatePage'),
    path('techTicketState', views.techTicketState, name='techTicketState'),
    path('dataTicketState', views.dataTicketState, name='dataTicketState'),
    path('sysTicketState', views.sysTicketState, name='sysTicketState'),
    path('filterTask', views.filterTask, name='filterTask'),
    path('searchResult', views.searchResult, name='searchResult'),
    path('searchResultV2', views.searchResultV2, name='searchResultV2'),
    path('companyReg', views.companyReg, name='companyReg'),
    path('dbAccess', views.dbAccess, name='dbAccess'),
    path('DbTicketSaved', views.DbTicketSaved, name='DbTicketSaved'),
    path('tableFormate', views.tableFormate, name='tableFormate'),
    path('ticketDashBoard', views.ticketDashBoard, name='ticketDashBoard'),
]

