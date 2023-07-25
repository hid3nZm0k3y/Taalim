from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StudentSignupForm, TeacherSignupForm, CourseForm, GradeForm, GPAForm, SemesterForm
from .models import User, Course, Semester, CourseResult, SemesterResult

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
    semester = Semester.objects.get(students=user.id)
    semester.enroll(course)
    semester.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@student_required
@login_required
def unroll(request, pk, id):
    user = request.user
    course = Course.objects.get(pk=id)
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
def grade_course(request,pk):
    if(request.method == "GET"):
        form = GradeForm()

    if(request.method == "POST"):
        form = GradeForm(request.POST)

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
        form = GradeForm(request.POST, instance=grade)

        if(form.is_valid()):
            form.save()
            url = reverse('taalim:dashboard_teacher', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    if(request.method == "GET"):
        form = GradeForm(instance=grade)

    return render(request, 'taalim/grade-edit.html', {
        "form": form
    })


@login_required
@teacher_required
def roster(request, pk, id):
    if(request.method == "GET"):
        course = Course.objects.get(pk=id).course_name
        semesters = Semester.objects.filter(courses__course_name__icontains = course)

    user = request.user
    return render(request, 'taalim/roster.html', {
        "course": course,
        "semesters": semesters,
        "user": user
    })


@login_required
@admin_required
def assign_gpa(request,pk):
    if(request.method == "GET"):
        form = GPAForm()

    if(request.method == "POST"):
        form = GPAForm(request.POST)

        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.save()

            # redirect user to home page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = request.user
    return render(request, 'taalim/semester-grade.html', {
        "form": form,
        "user": user
    })

@login_required
@admin_required
def edit_gpa(request,pk, id):
    gpa = get_object_or_404(SemesterResult, pk=id)
    
    if(request.method == "POST"):
        form = GPAForm(request.POST, instance=gpa)

        if(form.is_valid()):
            form.save()
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