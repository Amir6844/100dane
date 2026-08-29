from django.contrib import admin
from .models import Lesson
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=('title','classroom','group','date','order','created_at')
    list_filter=('classroom','group')
    search_fields=('title','description','homework')
    ordering = ['classroom','order']
