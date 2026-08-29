from django.db import models
from django.conf import settings

class Group(models.Model):
    classroom = models.ForeignKey('classes.Classroom', on_delete=models.CASCADE, related_name='groups', verbose_name='کلاس')
    name = models.CharField('نام گروه', max_length=100)
    description = models.TextField('توضیحات', blank=True)
    color = models.CharField('رنگ', max_length=7, default='#3E9B4F')
    max_members = models.PositiveIntegerField('حداکثر اعضا', default=5)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='member_groups', blank=True, verbose_name='اعضا')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'گروه'
        verbose_name_plural = 'گروه‌ها'
        unique_together = ('classroom', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.classroom.name}"

    def members_count(self):
        return self.members.count()
