# Generated by Django 4.2.6 on 2024-01-06 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_notice_notice_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff_notification',
            name='staff_id',
        ),
        migrations.AddField(
            model_name='staff_notification',
            name='school_teacehr_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.schoolteacher'),
        ),
    ]