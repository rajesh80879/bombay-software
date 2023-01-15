# Generated by Django 4.1.5 on 2023-01-15 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bombay', '0005_user_groups_user_is_superuser_user_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=datetime.datetime(2023, 1, 15, 15, 59, 24, 136138)),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default=None, max_length=10),
        ),
    ]
