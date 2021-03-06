# Generated by Django 4.0.2 on 2022-04-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChiefuserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chiefUserId', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('phone_no', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=25)),
                ('employee_id', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=10)),
                ('confirm_password', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=80)),
            ],
        ),
    ]
