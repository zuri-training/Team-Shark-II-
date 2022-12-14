from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core import models


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username',  'email', 'first_name', 'last_name', 'is_staff', 'is_student', 'is_teacher', 'mailing_address', 'phone', 'state', 'country')
    search_fields =['username', 'status']

    
    fieldsets = ( 
                 ( None, { 'fields': ('username', 'password') }),
                 
                 ('Personal info', { 'fields' : ('first_name', 'last_name', 'email') }),
                 
                ('Permissions', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),

                 ('Important dates', {'fields': ('last_login', 'date_joined') }),
                 
                 ('Additional info:', {'fields': ( 'is_student','full_name')}),
                 
                 )
    
    add_fieldsets = ( 
                     
                 ( None, { 'fields': ('username', 'password1', 'password2') }),
                 
                 ('Personal info', { 'fields' : ('first_name', 'last_name', 'email') }),
                 
                ('Permissions', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),
                 
                 ('Important dates', {'fields': ('last_login', 'date_joined') }),
                 
                 ('Additional info:', {'fields': ( 'is_student','full_name' )}),
                 
                 )

admin.site.register([
    models.Reel, models.Comment, models.Like, models.Dislike, models.View,
    models.Category, models.CustomUser, models.Posts, models.PostComments
])