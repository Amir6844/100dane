from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_code', 'classroom', 'phone', 'is_active', 'created_at')
    list_filter = ('classroom', 'is_active')
    search_fields = ('first_name', 'last_name', 'student_code', 'phone')
    list_select_related = ('classroom', 'user')
    ordering = ['classroom', 'last_name']
