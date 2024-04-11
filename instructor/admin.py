from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http import HttpRequest
from .models import Exam_Model, Module, Page,ExamResult, PageCompletion, ModelQuestion, TestQuestion, Test,CourseProgress    
from accounts.models import User 
from EECommittee.models import Course, Department 

class ModuleModelAdmin(admin.ModelAdmin):
     list_display = ('name','instructor','course','updated','No_pages') 
     model = Module 
     list_filter = ('course','instructor__username')
     search_fields = ('course__name','instructor__username','name')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user)
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 

          if db_field.name == 'course':
                kwargs['queryset'] = Course.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
     
 
admin.site.register(Module, ModuleModelAdmin) 

class PageModelAdmin(admin.ModelAdmin):
     list_display = ('title','modules','updated','noteStatus') 
     model = Page  
     list_filter = ('module',)
     search_fields = ('title','status')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user) 
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 
          if db_field.name == 'module':
                kwargs['queryset'] = Module.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Page, PageModelAdmin)

class ModelExamModelAdmin(admin.ModelAdmin):
     list_display = ('title','dept','questions') 
     model = Exam_Model 
     list_filter = ('dept',)
     search_fields = ('title','dept')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser:
               return qs
          
          return  qs.filter(dept=request.user.department)
        
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'dept':
               kwargs['queryset'] =  Department.objects.filter(users=request.user)

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(Exam_Model, ModelExamModelAdmin)

class TestExamModelAdmin(admin.ModelAdmin):
     list_display = ('title','course','instructor','questions') 
     model = Test 
     search_fields = ('title','course','instructor')
     list_filter = ['course__name','instructor__username']
     exclude = ['slug',]

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
                   
          return qs.filter(instructor=request.user) 
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'course':
               kwargs['queryset'] =  Course.objects.filter(instructor=request.user) 
          
          if db_field.name == 'instructor':
                kwargs['queryset'] =  User.objects.filter(username=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
 
admin.site.register(Test, TestExamModelAdmin)


class PageCompletionModelAdmin(admin.ModelAdmin):
     list_display = ('student','completed_page','module','course',"department","completed_date") 
     model = PageCompletion  
     list_filter = ('student__username','page__title')
     search_fields = ('student','page')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          

          return qs  
     
     
admin.site.register(PageCompletion, PageCompletionModelAdmin) 

class ModelQuestionModelAdmin(admin.ModelAdmin):
     list_display = ('instructor','question_field','answer_field','ans_description_field') 
     model = ModelQuestion 
     list_filter = ('instructor__username',)
     search_fields = ('instructor',) 
     exclude = ["optionA_slug","optionB_slug","optionC_slug","optionD_slug"]

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user)
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          print(db_field) 

          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 
          if db_field.name == 'modeExam':
               kwargs['queryset'] = Exam_Model.objects.filter(dept=request.user.department) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(ModelQuestion, ModelQuestionModelAdmin) 

class TestQuestionModelAdmin(admin.ModelAdmin):
     list_display = ('instructor','question_field','answer_field','ans_description_field','testExam') 
     model = TestQuestion 
     list_filter = ('instructor__username','testExam__title')
     search_fields = ('instructor',) 
     exclude = ["optionA_slug","optionB_slug","optionC_slug","optionD_slug"]
     
     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser:
               return qs
          return  qs.filter(instructor=request.user)
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 
          if db_field.name == 'testExam':
               kwargs['queryset'] = Test.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(TestQuestion, TestQuestionModelAdmin) 

class CourseProgressModelAdmin(admin.ModelAdmin):
     list_display = ('course','student',"progress","department")  
     model = CourseProgress 
     list_filter = ('course__name','progress') 
     search_fields = ('student__username',) 

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser:
               return qs
          return  qs.filter(course=request.user.courses.all()[0]) 
     
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'course':
               kwargs['queryset'] = request.user.courses   
          if db_field.name == 'testExam':
               kwargs['queryset'] = Test.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(CourseProgress, CourseProgressModelAdmin) 
from .models import ModelExamStatus 

class ModelExamStatusModelAdmin(admin.ModelAdmin):
     list_display = ('student','department','question_name',"response","response_status","question_category","category_name")  
     model = ModelExamStatus
     list_filter = ('student__username','category_name','question_category','department')  
     search_fields = ('student__username',) 

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser:
               return qs
          return  qs.filter(department=request.user.department) 
     
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'course':
               kwargs['queryset'] = request.user.courses   
          if db_field.name == 'testExam':
               kwargs['queryset'] = Test.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(ModelExamStatus, ModelExamStatusModelAdmin) 
from instructor.models import TestExamStatus

class TestExamStatusModelAdmin(admin.ModelAdmin):
     list_display = ('student','department','question_name',"response","response_status","question_category","category_name")  
     model = TestExamStatus
     list_filter = ('student__username','category_name','question_category','department')  
     search_fields = ('student__username',) 

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser:
               return qs
          return  qs.filter(department=request.user.department) 
     
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'course':
               kwargs['queryset'] = request.user.courses   
          if db_field.name == 'testExam':
               kwargs['queryset'] = Test.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(TestExamStatus, TestExamStatusModelAdmin) 

class StudentExamResultAdminModel(admin.ModelAdmin):
    
     list_display = ("student",'exam_name','score','total_mark',"exam_type")  
     model = ExamResult
     list_filter = ('student__username','exam_name','exam_type')  
     search_fields = ('student__username',) 

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          

         
          if request.user.is_superuser:
               model_exam_status = ModelExamStatus.objects.filter(department=request.user.department)
               dept_student = {}
               model_result = [] 
              
               for student in User.objects.filter(user_type='student',department=request.user.department):
                    dept_student[student.username] = [student,0,None,0]

                              
               for  status in model_exam_status:
                    for stud in dept_student:
                         if status.student.username == dept_student[stud][0].username and status.response == 'correct':
                              dept_student[student.username][1] += 1
                              dept_student[student.username][2] =  status.question.modeExam.title
                              dept_student[student.username][3] =  status.question.modeExam.question.all().count() 

                               

               for std in dept_student:
                    
                    if dept_student[std][2] is not None:

                         ExamResult(student=dept_student[std][0],score=dept_student[std][1], exam_name=dept_student[std][2], exam_type="model",total_mark=dept_student[std][3]).save()               
                             
          qs = super().get_queryset(request) 
          return  qs 
     
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'course':
               kwargs['queryset'] = request.user.courses   
          if db_field.name == 'testExam':
               kwargs['queryset'] = Test.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
admin.site.register(ExamResult, StudentExamResultAdminModel)  
