# Generated by Django 4.2.6 on 2024-01-02 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_studentresult_result_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='result',
            field=models.CharField(default=0, max_length=50, null=True),
        ),
    ]
