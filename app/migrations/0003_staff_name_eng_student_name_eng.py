# Generated by Django 4.2.6 on 2024-01-02 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_staff_leave_school_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='name_eng',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='student',
            name='name_eng',
            field=models.CharField(default='', max_length=50),
        ),
    ]
