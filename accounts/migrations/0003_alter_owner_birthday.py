# Generated by Django 3.2.4 on 2021-07-15 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210715_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]