from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StudentSignupForm, TeacherSignupForm, CourseForm, GradeForm, GPAForm, SemesterForm, AttendanceForm
from django.forms import formset_factory
from .models import User, Course, Semester, CourseResult, SemesterResult, Attendance

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table


# Decorator Patterns

def student_required(function = None, redirect_field_name = REDIRECT_FIELD_NAME, login_url = "login"):
    actual_decorator = user_passes_test(
        lambda u:  u.is_active and u.is_student,
        login_url = login_url,
        redirect_field_name= redirect_field_name
    )
    
    if function: 
        return actual_decorator(function)
    return actual_decorator

def teacher_required(function = None, redirect_field_name = REDIRECT_FIELD_NAME, login_url = "login"):
    actual_decorator = user_passes_test(
        lambda u:  u.is_active and u.is_teacher,
        login_url = login_url,
        redirect_field_name= redirect_field_name
    )
    
    if function: 
        return actual_decorator(function)
    return actual_decorator

def admin_required(function = None, redirect_field_name = REDIRECT_FIELD_NAME, login_url = "login"):
    actual_decorator = user_passes_test(
        lambda u:  u.is_active and u.is_superuser,
        login_url = login_url,
        redirect_field_name= redirect_field_name
    )
    
    if function: 
        return actual_decorator(function)
    return actual_decorator


# Create your views here.

def signup_teacher(request):
    if(request.method == "GET"):
        form = TeacherSignupForm()

    if(request.method == "POST"):
        form = TeacherSignupForm(request.POST, request.FILES)

        if(form.is_valid()):

            user = form.save()
            user.refresh_from_db()  
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # redirect user to home page
            return redirect('login')
        
    return render(request, 'taalim/signup-teacher.html', {
        "form": form,
    })
        
def signup_student(request):
    if(request.method == "GET"):
        form = StudentSignupForm()

    if(request.method == "POST"):
        form = StudentSignupForm(request.POST, request.FILES)

        if(form.is_valid()):

            user = form.save()
            user.refresh_from_db()  
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # redirect user to home page
            return redirect('login')


    return render(request, 'taalim/signup-student.html', {
        "form": form,
    })


@login_required
@student_required
def dashboard_student(request, pk):
    user = User.objects.get(pk=pk)
    
    return render(request, 'taalim/dashboard-student.html', {
    })


@login_required
@teacher_required
def dashboard_teacher(request, pk):
    user = User.objects.get(pk=pk)
    
    return render(request, 'taalim/dashboard-teacher.html', {
    })

@login_required
def dashboard_admin(request, pk):
    user = User.objects.get(pk=pk)
    courses = len(Course.objects.all())
    students = len(User.objects.filter(is_student=True))
    faculty = len(User.objects.filter(is_teacher=True))


    return render(request, 'taalim/dashboard-admin.html', {
        "students": students,
        "courses": courses,
        "faculty": faculty
    })


class Settings(UpdateView):
    model = User
    fields = "__all__"
    template_name = "taalim/settings.html"
    fields = ['username', 'email', 'profile_pic']
    success_url = reverse_lazy("taalim:home")


@login_required
def index(request):
    return render(request, "taalim/index.html")

# Courses Logic

@student_required
@login_required
def enroll(request, pk, id):
    user = request.user
    course = Course.objects.get(pk=id)
    course.enroll(user)
    semester = Semester.objects.get(students=user.id)
    semester.enroll(course)
    semester.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@student_required
@login_required
def unroll(request, pk, id):
    user = request.user
    course = Course.objects.get(pk=id)
    course.unroll(user)
    semester = Semester.objects.get(students=user.id)
    semester.unroll(course)
    semester.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@teacher_required
def create_course(request, pk):
    if(request.method == "GET"):
        form = CourseForm()

    if(request.method == "POST"):
        form = CourseForm(request.POST)

        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.instructor = request.user
            user.save()

            # redirect user to home page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'taalim/course-create.html', {
        "form": form,
        "user": pk, 
    })


@login_required
def view_course(request, pk):
    if(request.method == "GET"):
        courses = Course.objects.all()
        search = request.GET.get("search", False)

        if(search):
            query = Q(course_name__contains=search)
            courses = Course.objects.filter(query)
        if(request.user.is_student):
            semester = Semester.objects.get(students=request.user.id)
            semester_courses = semester.courses.all()
            print(semester_courses)
        if(request.user.is_teacher):
            semester_courses = courses
        if(request.user.is_superuser):
            semester_courses = courses

    user = request.user
    return render(request, 'taalim/course-list.html', {
        "courses": courses,
        "user": user,
        "semester_courses": semester_courses
    })
   

@login_required
@teacher_required
def delete_course(request,pk, id):
    course = Course.objects.filter(pk=id)
    course.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@teacher_required
def edit_course(request,pk, id):
    course = get_object_or_404(Course, pk=id)
    
    if(request.method == "POST"):
        form = CourseForm(request.POST, instance=course)

        if(form.is_valid()):
            form.save()
            url = reverse('taalim:view_course', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    if(request.method == "GET"):
        form = CourseForm(instance=course)

    return render(request, 'taalim/course-edit.html', {
        "form": form
    })

@login_required
@teacher_required
def grade_course(request,pk, id):
    if(request.method == "GET"):
        user = request.user
        course = Course.objects.get(pk=id)
        form = GradeForm(course, id)

    if(request.method == "POST"):
        user = request.user
        course = Course.objects.get(pk=id)
        form = GradeForm(course, id, request.POST)

        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.save()

            # redirect user to home page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = request.user
    return render(request, 'taalim/course-grade.html', {
        "form": form,
        "user": user
    })

@login_required
def view_grades(request, pk):
    if(request.method == "GET"):
        grades = CourseResult.objects.all()

        search = request.GET.get("search", False)
        if(search):
            query = Q(course__course_name__contains = search)
            grades = CourseResult.objects.filter(query)

    user = request.user
    return render(request, 'taalim/grade-list.html', {
        "grades": grades,
        "user": user,
    })
   
@student_required
@login_required
def view_semester(request, pk):
    if(request.method == "GET"):
        semesters = Semester.objects.all()

    user = request.user
    return render(request, 'taalim/semester-view.html', {
        "semesters": semesters,
        "user": user,
    })

@admin_required
@login_required
def view_semesters(request, pk):
    if(request.method == "GET"):
        semesters = Semester.objects.all()
        search = request.GET.get("search", False)
        if(search):
            query = Q(students__username__contains = search)
            semesters = Semester.objects.filter(query)


    user = request.user
    return render(request, 'taalim/semester-view.html', {
        "semesters": semesters,
        "user": user,
    })

@login_required
@admin_required
def edit_semester(request,pk, id):
    semester = get_object_or_404(Semester, pk=id)
    
    if(request.method == "POST"):
        form = SemesterForm(request.POST, instance=semester)

        if(form.is_valid()):
            form.save()
            url = reverse('taalim:dashboard_admin', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    if(request.method == "GET"):
        form = SemesterForm(instance=semester)

    return render(request, 'taalim/semester-edit.html', {
        "form": form
    })

   
@login_required
@admin_required
def delete_semester(request,pk, id):
    semester = Semester.objects.filter(pk=id)
    semester.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@admin_required
def create_semester(request, pk):
    if(request.method == "GET"):
        form = SemesterForm()

    if(request.method == "POST"):
        form = SemesterForm(request.POST)

        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.save()

            # redirect user to home page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'taalim/semester-create.html', {
        "form": form,
        "user": pk, 
    })

@login_required
@teacher_required
def edit_grade(request,pk, id):
    grade = get_object_or_404(CourseResult, pk=id)
    
    if(request.method == "POST"):
        course = grade.course
        course_id = grade.course.id
        form = GradeForm(course, course_id, request.POST, instance=grade)

        if(form.is_valid()):
            form.save()
            url = reverse('taalim:dashboard_teacher', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    if(request.method == "GET"):
        course = grade.course
        course_id = grade.course.id
        form = GradeForm(course, course_id, instance=grade)

    return render(request, 'taalim/grade-edit.html', {
        "form": form
    })


@admin_required
@login_required
def roster_admin(request,pk, id):
    if(request.method == "GET"):
            course = Course.objects.get(pk=id).course_name
            semesters = Semester.objects.filter(courses__course_name__icontains = course)

            user = request.user
            percentages = []
            if(semesters):
                for semester in semesters:
                    student = semester.students
                    present = Attendance.objects.filter(course=id).filter(student=student).filter(status=True)
                    absent = Attendance.objects.filter(course=id).filter(student=student).filter(status=False)

                    p_count = present.count()
                    a_count = absent.count()
                    total = p_count + a_count
                    if (total == 0):
                        total = 1
                    n = round((p_count * 100)/total,2)
                    percentages.append(n)

    return render(request, 'taalim/roster.html', {
        "course": course,
        "semesters": semesters,
        "user": user,
        "percentages": percentages,
        "data": zip(semesters, percentages)

    })


@login_required
@teacher_required
def roster(request, pk, id):
    if(request.method == "GET"):
        course = Course.objects.get(pk=id).course_name
        semesters = Semester.objects.filter(courses__course_name__icontains = course)

        user = request.user
        percentages = []
        if(semesters):
            for semester in semesters:
                student = semester.students
                present = Attendance.objects.filter(course=id).filter(student=student).filter(status=True)
                absent = Attendance.objects.filter(course=id).filter(student=student).filter(status=False)

                p_count = present.count()
                a_count = absent.count()
                total = p_count + a_count
                if (total == 0):
                    total = 1
                n = round((p_count * 100)/total,2)
                percentages.append(n)

    return render(request, 'taalim/roster.html', {
        "course": course,
        "semesters": semesters,
        "user": user,
        "percentages": percentages,
        "data": zip(semesters, percentages)

    })


@login_required
@student_required
def request_gpa(request,pk):
    user = User.objects.get(pk=pk)
    semester = Semester.objects.get(students=user.id)

    if(request.method == "GET"):
        form = GPAForm()
        form.fields.pop("cgpa")
        form.fields.pop("student")
        form.fields.pop("semester")


    if(request.method == "POST"):
        form = GPAForm(request.POST)
        form.fields.pop("cgpa")
        form.fields.pop("student")
        form.fields.pop("semester")

        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.student = User.objects.get(pk=pk)
            user.semester = Semester.objects.get(students=user.student)

            total_credit = 0
            earned_credit = 0

            for course in semester.courses.all():
                total_credit += course.credit_hours

            results = CourseResult.objects.filter(student=user.student)

            for result in results.all():
                earned_credit += result.gpa

            user.cgpa = (earned_credit * 4)/(total_credit)
            print(earned_credit, total_credit)
            user.save()

            # redirect user to home page
            url = reverse('taalim:home')
            return HttpResponseRedirect(url)

    user = request.user
    return render(request, 'taalim/semester-grade.html', {
        "form": form,
        "user": user
    })

@login_required
def delete_gpa(request,pk, id):
    gpa = SemesterResult.objects.filter(pk=id)
    gpa.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@admin_required
def edit_gpa(request,pk, id):
    gpa = get_object_or_404(SemesterResult, pk=id)
    
    if(request.method == "POST"):
        form = GPAForm(request.POST, instance=gpa)

        if(form.is_valid()):
            obj = form.save(commit=False)
            obj.save()

            url = reverse('taalim:dashboard_admin', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    if(request.method == "GET"):
        form = GPAForm(instance=gpa)

    return render(request, 'taalim/semester-grade.html', {
        "form": form
    })

@login_required
def view_gpa(request, pk):
    if(request.method == "GET"):
        gpas = SemesterResult.objects.all()

    user = request.user
    return render(request, 'taalim/final-list.html', {
        "gpas": gpas,
        "user": user,
    })

@admin_required
@login_required
def view_gpas(request, pk):
    if(request.method == "GET"):
        gpas = SemesterResult.objects.all()
        search = request.GET.get("search", False)
        if(search):
            query = Q(student__username__contains = search)
            gpas = SemesterResult.objects.filter(query)


    user = request.user
    return render(request, 'taalim/final-list.html', {
        "gpas": gpas,
        "user": user,
    })


@login_required
@student_required
def generate_report(request, pk, id):
    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    text_object = canv.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont("Helvetica", 14)

    lines = []

    canv.setFont('Helvetica', 20)
    canv.drawString(3*inch, 0.5*inch, 'Unofficial Transcript')

    course_results = CourseResult.objects.filter(student=pk)
    for result in course_results.all():
        lines.append(result.course.course_name)
        lines.append("Marks: " + str(result.marks) + "/" + str(100))
        lines.append("Grade: " + str(round(result.gpa, 2)) + "/" + str(result.course.credit_hours))
        lines.append("")

    semester_result = SemesterResult.objects.get(pk=id)
    lines.append("CGPA: " + str(round(semester_result.cgpa, 2)) + "/" + str(4))

    for line in lines:
        text_object.textLine(line)

    canv.drawText(text_object)
    canv.showPage()
    canv.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="result.pdf")

@login_required
@teacher_required
def take_attendance(request, pk, id):
    if(request.method == "GET"):
        course = Course.objects.get(pk=id)
        n = 0
        students= []

        for student in course.students.all():
            n = n + 1
            students.append(student)

        AttendanceFormset = formset_factory(AttendanceForm ,max_num=n)
        some_formset = AttendanceFormset(initial=[{'course': course, "student": x.id} for x in students])

    if request.method == "POST":

        course = Course.objects.get(pk=id)
        n = 0
        students= []

        for student in course.students.all():
            n = n + 1
            students.append(student)

        AttendanceFormset = formset_factory(AttendanceForm, max_num=n)
        some_formset = AttendanceFormset(initial=[{'course': course, "student": x.id} for x in students])
        formset = AttendanceFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                form.save()
        
            url = reverse('taalim:dashboard_teacher', kwargs={'pk': pk})
            return HttpResponseRedirect(url)

    return render(request, 'taalim/attendance_create.html', {
        "formset": some_formset,
    })


@login_required
def view_attendance(request, pk, id):
    if(request.method == "GET"):    
        attendances = Attendance.objects.filter(course=id)
        n = 0

        search = request.GET.get("search", False)
        if(search):
            query = Q(student__username__contains = search)
            attendances = Attendance.objects.filter(query)

        if(attendances and request.user.is_student):

            present = Attendance.objects.filter(course=id).filter(student=request.user.id).filter(status=True)
            absent = Attendance.objects.filter(course=id).filter(student=request.user.id).filter(status=False)

            p_count = present.count()
            a_count = absent.count()
            total = p_count + a_count
            n = round((p_count * 100)/total,2)

    user = request.user
    return render(request, 'taalim/attendance_view.html', {
        "attendances": attendances,
        "user": user,
        "n": n
    })
