# Generated by Django 3.2.4 on 2021-07-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210715_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]