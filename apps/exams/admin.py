from django.contrib import admin
from .models import Exam, Question
class QuestionInline(admin.TabularInline):
    model=Question
    extra=1
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display=('title','classroom','group','exam_type','date','total_score','created_at')
    list_filter=('exam_type','classroom')
    search_fields=('title','description')
    ordering=['-date']
    inlines=[QuestionInline]
