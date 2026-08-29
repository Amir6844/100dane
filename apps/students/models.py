from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Student(models.Model):
    """
    Roster-based Student per spec: first_name, last_name, student_code, phone, notes, created_at, updated_at
    Linked to Classroom via FK, optionally linked to auth User for login.
    Teacher owns via classroom.teacher.
    """
    classroom = models.ForeignKey('classes.Classroom', on_delete=models.CASCADE, related_name='roster_students', verbose_name='کلاس')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile', verbose_name='حساب کاربری')
    first_name = models.CharField('نام', max_length=100)
    last_name = models.CharField('نام خانوادگی', max_length=100)
    student_code = models.CharField('کد دانش‌آموزی', max_length=20, blank=True, db_index=True)
    phone = models.CharField('شماره موبایل', max_length=11, blank=True, validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل باید با 09 شروع و 11 رقم باشد.')])
    notes = models.TextField('یادداشت', blank=True)
    is_active = models.BooleanField('فعال', default=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'دانش‌آموز (فهرست کلاس)'
        verbose_name_plural = 'دانش‌آموزان (فهرست)'
        ordering = ['last_name', 'first_name']
        unique_together = [('classroom', 'student_code')]
        indexes = [
            models.Index(fields=['classroom', 'last_name']),
            models.Index(fields=['student_code']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['classroom', 'student_code'], name='unique_student_code_per_class', condition=models.Q(student_code__isnull=False) & ~models.Q(student_code='')),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_code or self.classroom.name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_user(self):
        return self.user
