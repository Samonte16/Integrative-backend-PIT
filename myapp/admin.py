from django.contrib import admin
from .models import User, Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'age', 'phone', 'email', 'password')
    search_fields = ('full_name', 'email')
    list_filter = ('gender',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'age', 'email', 'password')
    search_fields = ('full_name', 'email')
    list_filter = ('gender',)
