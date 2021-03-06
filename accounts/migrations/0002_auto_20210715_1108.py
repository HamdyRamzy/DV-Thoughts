# Generated by Django 3.2.4 on 2021-07-15 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='experiences',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='accounts.experience'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='courses',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='accounts.course'),
        ),
    ]
