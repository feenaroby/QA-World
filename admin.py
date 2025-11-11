from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.auth.models import Group
from django.contrib.auth.models import User



from .models import user,categry,expert_tbl,question,Pending,tbl_answer,tbl_chat



class adminuser(admin.ModelAdmin):
    list_display = ['f_name', 'l_name', 'mobile', 'email', 'gender']
    list_per_page = 10

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):




class adminexpert_tbl(admin.ModelAdmin):
     list_display = ['f_name', 'cat', 'mobile',  'interest','email']
     list_per_page = 10




     # def has_delete_permission(self, request, obj=None):
     #    return False



class adminpendings(admin.ModelAdmin):

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):

        return False



class adminquestion(admin.ModelAdmin):
         list_display = ['f_name']






# Register your models here.

admin.site.register(user, adminuser)
admin.site.register(expert_tbl,adminexpert_tbl)
admin.site.register(categry)
admin.site.register(tbl_answer)
admin.site.register(Pending,adminpendings)
admin.site.register(question)
admin.site.register(tbl_chat)




