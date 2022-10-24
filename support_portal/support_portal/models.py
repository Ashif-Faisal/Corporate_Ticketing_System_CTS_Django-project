from django.db import models


class userprofile(models.Model):

    sr_name = models.CharField(max_length=30, null=True)
    work_stream = models.CharField(max_length=30, null=True)
    task = models.CharField(max_length=300, null=True)
    value_hml = models.CharField(max_length=30, null=True)
    urgent_yn = models.BooleanField(max_length=30, null=True)
    # request_date = models.CharField(max_length=30, null=True)
    request_date = models.DateTimeField(null=True)
    needed_date = models.DateTimeField(max_length=30, null=True)
    etd = models.DateTimeField(max_length=30,null=True)
    acd = models.DateTimeField(max_length=30, null=True)
    request_by_actor = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True)
    maker1 = models.CharField(max_length=30)
    maker2 = models.CharField(max_length=30, null=True)
    checker = models.CharField(max_length=30, null=True)
    outside_office_time = models.CharField(max_length=30, null=True)
    url = models.CharField(max_length=100, null=True)
    add_to_google = models.DateTimeField(max_length=30, null=True)
    employee_id = models.CharField(max_length=30, null=True)
    comment = models.CharField(max_length=400, null=True)
    attachment = models.FileField(max_length=100, null=True)
    approval = models.CharField(max_length=50, null=True)
    team = models.CharField(max_length=50, null=True)
    #attachment = models.FileField(upload_to='media/')
    #attachment = models.ImageField(upload_to='media',null=True)

    def __str__(self):
        return self.sr_name


class infoUpdate(models.Model):
    latest_update = models.CharField(max_length=500, null=True)
    task_id = models.CharField(max_length=50, null=True)
    update_date = models.DateTimeField(max_length=50, null=True)



    def __str__(self):
        return self.latest_update