from django.contrib import admin
from userauths.models import Profile,User


class UserAdmin(admin.ModelAdmin):
    list_display=['fullname','email','phone']
    
class ProfileAdmin(admin.ModelAdmin):
    list_display=['fullname','gender','country']
    list_editable=['gender','country']
    search_fields=['fullname','date']
    list_filter=['date','fullname']

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
# Register your models here.
