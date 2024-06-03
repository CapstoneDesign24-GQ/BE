from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['userId', 'email', 'nickname', 'ageRange', 'nationality']
    search_fields = ['email', 'nickname']

admin.site.register(User, UserAdmin)