# Generated by Django 3.2.4 on 2021-07-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('Unlike', 'Unlike'), ('Like', 'Like')], default='Like', max_length=10),
        ),
    ]
