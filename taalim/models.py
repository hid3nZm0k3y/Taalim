from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    GENDERS = (
    ("M", "Male"),
    ("F", "Female"),)
    gender = models.CharField(max_length=1, choices=GENDERS, default="M")
    profile_pic = models.ImageField(null=True)
    address = models.TextField(max_length=100, default="")

class Course(models.Model):
    course_code = models.CharField(max_length=5)
    course_name = models.CharField(max_length=255)
    credit_hours = models.IntegerField( validators=[
        MinValueValidator(0), MaxValueValidator(30)
    ])
    instructor = models.ForeignKey(User, related_name='teaches', on_delete=models.CASCADE, limit_choices_to={"is_teacher": True})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_name}"

class Semester(models.Model):
    term = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    courses = models.ManyToManyField(Course, related_name="offered_in", blank=True)
    students = models.ForeignKey(User, related_name="current_semester", on_delete=models.CASCADE, limit_choices_to={"is_student": True})

    def __str__(self):
        return f"Semester {self.term}: {self.students}"
    
    def enroll(self, course):
        self.courses.add(course)

    def unroll(self, course):
        self.courses.remove(course)

class CourseResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_student": True})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Result: {self.course}"


class SemesterResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_student": True})
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    cgpa = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(4)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
