# Generated by Django 3.2.3 on 2021-05-26 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
    ]