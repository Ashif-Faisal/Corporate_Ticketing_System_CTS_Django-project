# Generated by Django 4.1.2 on 2022-12-30 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_portal', '0030_userprofile_updated_task_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='customerinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('phonenumber', models.IntegerField(max_length=16, null=True)),
            ],
        ),
    ]