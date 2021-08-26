# Generated by Django 3.2.4 on 2021-08-04 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_auto_20210803_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report_topic',
            name='description',
            field=models.TextField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='report_topic',
            name='report_type',
            field=models.CharField(choices=[('Something else', 'Something else'), ('Harassment', 'Harassment'), ('Nudity', 'Nudity'), ('Terrorism', 'Terrorism'), ('Violence', 'Violence'), ('Spam', 'Spam'), ('False information', 'False information'), ('Suicide or self-injury', 'Suicide or self-injury')], max_length=100),
        ),
    ]
