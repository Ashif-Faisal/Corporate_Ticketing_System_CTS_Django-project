# Generated by Django 4.1.2 on 2022-11-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_portal', '0027_userprofile_team_alter_userprofile_maker1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='maker1',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
