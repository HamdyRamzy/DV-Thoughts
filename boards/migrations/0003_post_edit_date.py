# Generated by Django 3.2.4 on 2021-07-23 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_alter_like_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edit_date',
            field=models.DateTimeField(null=True),
        ),
    ]
