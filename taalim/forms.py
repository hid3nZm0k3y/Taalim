from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import User, Course, Semester, SemesterResult, CourseResult

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
        exclude = ['instructor']

class GradeForm(forms.ModelForm):
    class Meta:
        model = CourseResult
        fields = '__all__'

class GPAForm(forms.ModelForm):
    class Meta:
        model = SemesterResult
        fields = '__all__'

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'