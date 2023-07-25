# Generated by Django 4.2.3 on 2023-07-17 07:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taalim', '0008_remove_classattendance_student_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='SemesterResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cgpa', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taalim.semester')),
                ('student', models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='courseclass',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='courseclass',
            name='students',
        ),
        migrations.RemoveField(
            model_name='programresult',
            name='program_id',
        ),
        migrations.RemoveField(
            model_name='programresult',
            name='student_id',
        ),
        migrations.RenameField(
            model_name='courseresult',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RemoveField(
            model_name='courseresult',
            name='assignment_marks',
        ),
        migrations.RemoveField(
            model_name='courseresult',
            name='exam_marks',
        ),
        migrations.RemoveField(
            model_name='courseresult',
            name='student_id',
        ),
        migrations.AddField(
            model_name='courseresult',
            name='marks',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='courseresult',
            name='student',
            field=models.ForeignKey(limit_choices_to={'is_student': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(limit_choices_to={'is_teacher': True}, on_delete=django.db.models.deletion.CASCADE, related_name='teaches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ClassAttendance',
        ),
        migrations.DeleteModel(
            name='CourseClass',
        ),
        migrations.DeleteModel(
            name='Program',
        ),
        migrations.DeleteModel(
            name='ProgramResult',
        ),
        migrations.AddField(
            model_name='semester',
            name='courses',
            field=models.ManyToManyField(related_name='offered_in', to='taalim.course'),
        ),
        migrations.AddField(
            model_name='semester',
            name='students',
            field=models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, related_name='current_semester', to=settings.AUTH_USER_MODEL),
        ),
    ]