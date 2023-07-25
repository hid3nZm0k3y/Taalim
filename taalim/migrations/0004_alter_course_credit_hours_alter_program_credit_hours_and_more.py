# Generated by Django 4.2.3 on 2023-07-15 11:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taalim', '0003_programresult_courseresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='credit_hours',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='program',
            name='credit_hours',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)]),
        ),
        migrations.AlterField(
            model_name='program',
            name='semesters',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)]),
        ),
    ]