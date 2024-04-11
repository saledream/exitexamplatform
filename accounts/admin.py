from collections.abc import Callable, Sequence
from typing import Any, Set
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import User 
from instructor.models import CourseProgress 

class CustomUserAdmin(UserAdmin):
      list_display = ('username','email','department','user_type','date_joined')
      model = User
      list_filter = ("user_type", 'department')
      fieldsets = (
        (None, {"fields": ("email", 'username',"password",'department')}),
        ('Personal Info',{'fields':('first_name','last_name','user_type','bio','avtar')}),
         ("Permissions", {"fields": ("is_staff", "groups", "user_permissions")}),
         ('Important Dates', {'fields':('last_login','date_joined')})
        )
      add_fieldsets = (
         (None, {
             "classes": ("wide",),
             "fields": (
                 "email", 'username', "password1", "password2",'department', 
                 'user_type', "groups", "user_permissions",
             )}
         ),
     )
      search_fields = ("email",'username','department')
      ordering = ("email",)


    #   def get_fieldsets(self, request, obj=None):
            
    #         if  request.user.is_superuser:
        
    #                 return (
    #                     (None, {"fields": ("email", 'username',"password",'department','user_type')}),
    #                     ('Personal Info',{'fields':('first_name','last_name','bio','avtar')}),
    #                     ("Permissions", {"fields": ("is_active","is_staff", "groups", "user_permissions")}),
    #                     ('Important Dates', {'fields':('last_seen','joined_date')})
    #                     )
    #         elif request.user.user_type == 'instructor':

    #                  return (
    #                        ('Personal Info',{'fields':('first_name','last_name','bio','avtar')}),
    #                  ) 
                   
              
    #         else:
    #                return (
    #                    (None, {"fields": ("email", 'username',"password",'department','user_type')}),
    #                     ('Personal Info',{'fields':('first_name','last_name','bio','avtar')})
    #                 )
            

    #   def get_form(self, request,obj=None, **kwargs):
            
    #         form = super(CustomUserAdmin,self).get_form(request,obj,**kwargs) 
    #         print(form.base_fields)  
    #         print(dir(form)) 

    #         disabled_fileds = ['username',
    #                     'email',
    #                     'password',
    #                     'user_type',
    #                     'department', 
    #                     ] 
          
    #         if not (request.user.is_superuser or request.user.user_type == 'admin'):
    #               for f in disabled_fileds:
    #                    if f in form.base_fields:
    #                         form.base_fields[f].disabled = True 

    #         return form 
    #   def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
            

    #         return super().get_readonly_fields(request, obj)
      
    #   def formfield_for_foreignkey(self, db_field, request, **kwargs):
          
    #       if db_field.name == 'instructor':
    #            kwargs['queryset'] = User.objects.filter(username=request.user) 

    #       return super().formfield_for_foreignkey(db_field, request, **kwargs)

            
admin.site.register(User, CustomUserAdmin)


