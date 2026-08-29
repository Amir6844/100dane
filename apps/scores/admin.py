from django.contrib import admin
from .models import Score
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display=('student','exam','value','score','created_at')
    list_filter=('exam__classroom','exam')
    search_fields=('student__username','student__first_name','exam__title')
    ordering=['-created_at']
    list_select_related=('student','exam')
