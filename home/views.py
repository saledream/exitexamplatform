from django.shortcuts import render
from django.http import HttpResponse
from instructor.models import Module, Exam_Model, Page,  ModelQuestion, TestQuestion, Test
from accounts.models import User 
from EECommittee.models import Course, Department 


# Create your views here.

def home(request):
    students = User.objects.filter(user_type="instructor").count()
    instructors = User.objects.filter(user_type="student").count() 
    courses = Course.objects.all().count() 
    modules =Module.objects.all().count() 
    modelExams = Exam_Model.objects.all().count()
    testExam = Test.objects.all().count() 
    testQ = TestQuestion.objects.all().count()
    modelQ =    ModelQuestion.objects.all().count() 

    return render(request, "home/index.html", {"students": students,"instructors":instructors,"courses":courses,"modules":modules,"questions":testQ+modelQ,"models":modelExams,"tests":testExam})

def about(request):
    return HttpResponse("<h1> About </h1>")  