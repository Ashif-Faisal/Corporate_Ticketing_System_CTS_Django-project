# Generated by Django 4.1.2 on 2022-12-30 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support_portal', '0031_customerinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='customerinfo',
            new_name='companyinfo',
        ),
    ]
