from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelChoiceField
from .models import User, Course, Semester, SemesterResult, CourseResult, Attendance

class StudentSignupForm(UserCreationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'profile_pic', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student= True
        if commit:
            user.save()
        return user

class TeacherSignupForm(UserCreationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'profile_pic', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['instructor', 'students']

class GradeForm(forms.ModelForm):
    class Meta:
        model = CourseResult
        fields = '__all__'
        exclude = ['gpa']
        
    def __init__(self, course, id, *args, **kwargs):
        super(GradeForm, self).__init__( *args, **kwargs)    
        qs1 = Course.objects.filter(pk=id)
        qs2 =  course.students

        self.fields['course'] = ModelChoiceField(queryset=qs1)
        self.fields['student'] = ModelChoiceField(queryset=qs2)

class GPAForm(forms.ModelForm):
    class Meta:
        model = SemesterResult
        fields = '__all__'
        exclude = []


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        widgets = {"course": forms.HiddenInput()}
        fields = '__all__'
        


