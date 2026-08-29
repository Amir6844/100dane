from django.db import models

class Lesson(models.Model):
    classroom = models.ForeignKey('classes.Classroom', on_delete=models.CASCADE, related_name='lessons', verbose_name='کلاس')
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons', verbose_name='گروه (اختیاری)')
    title = models.CharField('عنوان درس', max_length=200)
    description = models.TextField('توضیحات', blank=True)
    date = models.DateField(null=True, blank=True, verbose_name='تاریخ جلسه')
    lesson_date = models.DateField(null=True, blank=True, verbose_name='تاریخ درس', help_text='نام جایگزین برای date - سازگار با مستندات')
    homework = models.TextField('تکالیف', blank=True, help_text='تکالیف مربوط به این جلسه')
    order = models.PositiveIntegerField('ترتیب', default=0)
    attachment = models.FileField('فایل پیوست', upload_to='lessons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'درس'
        verbose_name_plural = 'درس‌ها'
        ordering = ['order', '-date', '-created_at']
        indexes = [models.Index(fields=['classroom', 'group']), models.Index(fields=['date'])]

    def __str__(self):
        return f"{self.title} - {self.classroom.name}"
