# Generated by Django 4.2.6 on 2024-01-06 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_webnotice_notice_notice_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='notice_link',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]