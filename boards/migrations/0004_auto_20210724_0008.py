# Generated by Django 3.2.4 on 2021-07-23 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_post_edit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='edit_date',
            field=models.DateField(null=True),
        ),
    ]