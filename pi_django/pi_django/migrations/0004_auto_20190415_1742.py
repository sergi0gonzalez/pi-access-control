# Generated by Django 2.2 on 2019-04-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pi_django', '0003_auto_20190415_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissions',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
