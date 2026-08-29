from django.contrib import admin
from .models import Group
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','classroom','members_count','max_members','created_at')
    list_filter = ('classroom',)
    search_fields = ('name', 'description')
    filter_horizontal = ('members',)
    ordering = ['classroom', 'name']
