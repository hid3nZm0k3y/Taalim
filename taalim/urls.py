from django.urls import path
from . import views

app_name = "taalim"

urlpatterns = [
    
    path("", views.index, name="home"),
    path("signup_student", views.signup_student, name="signup_student"),
    path("signup_teacher", views.signup_teacher, name="signup_teacher"),
    path("settings/<int:pk>", views.Settings.as_view(), name="settings"),

    path("dashboard_teacher/<int:pk>", views.dashboard_teacher, name="dashboard_teacher"),
    path("dashboard_teacher/<int:pk>/courses", views.view_course, name="view_course"),
    path("dashboard_teacher/<int:pk>/courses/roster/<int:id>", views.roster, name="roster"),
    path("dashboard_teacher/<int:pk>/courses/edit/<int:id>", views.edit_course, name="edit_course"),
    path("dashboard_teacher/<int:pk>/courses/delete/<int:id>", views.delete_course, name="delete_course"),
    path("dashboard_teacher/<int:pk>/create_course/", views.create_course, name="create_course"),
    path("dashboard_teacher/<int:pk>/grade_course/<int:id>", views.grade_course, name="grade_course"),
    path("dashboard_teacher/<int:pk>/grades/", views.view_grades, name="view_grades"),
    path("dashboard_teacher/<int:pk>/grades/<int:id>", views.edit_grade, name="edit_grade"),
    path("dashboard_teacher/<int:pk>/attendance/<int:id>", views.take_attendance, name="take_attendance"),

    
    path("dashboard_student/<int:pk>/courses", views.view_course, name="view_course_student"),
    path("dashboard_student/<int:pk>/enroll/<int:id>", views.enroll, name="enroll"),
    path("dashboard_student/<int:pk>/unroll/<int:id>", views.unroll, name="unroll"),
    path("dashboard_student/<int:pk>", views.dashboard_student, name="dashboard_student"),
    path("dashboard_student/<int:pk>/grades/", views.view_grades, name="view_grades"),
    path("dashboard_student/<int:pk>/semester/", views.view_semester, name="view_semester"),
    path("dashboard_student/<int:pk>/gpa/", views.view_gpa, name="view_gpa"),
    path("dashboard_student/<int:pk>/gpa/delete/<int:id>", views.delete_gpa, name="delete_gpa"),
    path("dashboard_student/<int:pk>/gpa/<int:id>", views.generate_report, name="generate_report"),
    path("dashboard_student/<int:pk>/request_gpa", views.request_gpa, name="request_gpa"),
    path("dashboard_student/<int:pk>/semester/<int:id>/attendance", views.view_attendance, name="view_attendance"),


    path("dashboard_admin/<int:pk>", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard_admin/<int:pk>/courses", views.view_course, name="view_course_admin"),
    path("dashboard_admin/<int:pk>/courses/roster/<int:id>", views.roster_admin, name="roster_admin"),
    path("dashboard_admin/<int:pk>/edit_gpa/<int:id>", views.edit_gpa, name="edit_gpa"),
    path("dashboard_admin/<int:pk>/gpa/", views.view_gpas, name="view_gpas"),
    path("dashboard_admin/<int:pk>/semester/", views.create_semester, name="create_semester"),
    path("dashboard_admin/<int:pk>/semesters/", views.view_semesters, name="view_semesters"),
    path("dashboard_admin/<int:pk>/semester/edit/<int:id>", views.edit_semester, name="edit_semester"),
    path("dashboard_admin/<int:pk>/semester/delete/<int:id>", views.delete_semester, name="delete_semester"),


]
