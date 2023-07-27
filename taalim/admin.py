from django.contrib import admin
from .models import User, Course, Semester, CourseResult, SemesterResult, Attendance

# Register your models here.

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(CourseResult)
admin.site.register(SemesterResult)
admin.site.register(Attendance)


