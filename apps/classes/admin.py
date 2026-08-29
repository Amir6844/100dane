from django.contrib import admin
from .models import Classroom

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'teacher', 'grade_level', 'academic_year', 'subject', 'is_active', 'invite_code', 'students_count', 'created_at')
    list_filter = ('grade_level', 'is_active', 'academic_year')
    search_fields = ('name', 'title', 'invite_code', 'subject')
    list_display_links = ('name',)
    ordering = ['-created_at']
    filter_horizontal = ('students',)
    list_editable = ('is_active',)
