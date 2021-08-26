# Generated by Django 3.2.4 on 2021-08-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0011_auto_20210818_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='progress',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='report_topic',
            name='report_type',
            field=models.CharField(choices=[('Something else', 'Something else'), ('Nudity', 'Nudity'), ('Harassment', 'Harassment'), ('Violence', 'Violence'), ('False information', 'False information'), ('Spam', 'Spam'), ('Terrorism', 'Terrorism'), ('Suicide or self-injury', 'Suicide or self-injury')], max_length=100),
        ),
        migrations.AlterField(
            model_name='report_user',
            name='report_type',
            field=models.CharField(choices=[('Something else', 'Something else'), ('Nudity', 'Nudity'), ('Harassment', 'Harassment'), ('Violence', 'Violence'), ('False information', 'False information'), ('Spam', 'Spam'), ('Terrorism', 'Terrorism'), ('Suicide or self-injury', 'Suicide or self-injury')], max_length=100),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_picture',
            field=models.ImageField(null=True, upload_to='topic_picture/%y/%m/%d'),
        ),
    ]