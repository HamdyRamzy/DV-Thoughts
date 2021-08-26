# Generated by Django 3.2.4 on 2021-08-18 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0010_auto_20210806_0517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('Terrorism', 'Terrorism'), ('Nudity', 'Nudity'), ('Something else', 'Something else'), ('Harassment', 'Harassment'), ('False information', 'False information'), ('Violence', 'Violence'), ('Suicide or self-injury', 'Suicide or self-injury'), ('Spam', 'Spam')], max_length=100)),
                ('description', models.TextField(max_length=400)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_sender', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10),
        ),
        migrations.AlterField(
            model_name='report_topic',
            name='description',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='report_topic',
            name='report_type',
            field=models.CharField(choices=[('Terrorism', 'Terrorism'), ('Nudity', 'Nudity'), ('Something else', 'Something else'), ('Harassment', 'Harassment'), ('False information', 'False information'), ('Violence', 'Violence'), ('Suicide or self-injury', 'Suicide or self-injury'), ('Spam', 'Spam')], max_length=100),
        ),
    ]