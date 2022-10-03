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
    path('admin/', admin.site.urls),
    path('info', views.infoview, name='info'),
    path('test',views.testpage, name='test'),
    path('',views.loginview, name='login'),
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
    #path('task_id', views.task_id, name='task_id'),
    # path('admin/', admin.site.urls),
    # path('', include('main.urls'))
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
