from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('اطلاعات تکمیلی', {'fields': ('role', 'phone', 'student_code', 'national_code', 'bio', 'notes', 'avatar')}),)
    list_display = ('username', 'get_full_name', 'role', 'phone', 'student_code', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'phone', 'student_code')
    ordering = ['-date_joined']
