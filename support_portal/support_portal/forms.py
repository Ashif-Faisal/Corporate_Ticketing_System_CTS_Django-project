from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import userprofile, infoUpdate


class createUserForm(UserCreationForm):
    class Meta:
        model = User #python User models
        fields = ['username', 'email', 'password1', 'password2']


class userProfileForm(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = [
           # "first_name",
          #  "last_name",
            "sr_name",
            "work_stream",
            "task",
            "value_hml",
            "urgent_yn",
            "request_date",
            "needed_date",
            "etd",
            "acd",
            "request_by_actor",
            "status",
            "maker1",
            "maker2",
            "checker",
            "outside_office_time",
            "url",
            "add_to_google",

        ]


class newticket(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = [

            "employee_id",
            "task",
            "comment",
            "attachment",
            "approval",


        ]


class infoUpdate(forms.ModelForm):
    class Meta:
        model = infoUpdate
        fields = [
            "latest_update",
            "update_date",
            "task_id",

        ]