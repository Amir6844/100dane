import re
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        TEACHER = 'teacher', 'دبیر'
        STUDENT = 'student', 'دانش‌آموز'
        ADMIN = 'admin', 'مدیر'

    role = models.CharField('نقش', max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField('شماره موبایل', max_length=11, blank=True,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل باید با 09 شروع شود و 11 رقم باشد.')],
        help_text='مثال: 09123456789')
    student_code = models.CharField('کد دانش‌آموزی', max_length=20, blank=True, db_index=True, help_text='کد یکتا برای دانش‌آموز')
    national_code = models.CharField('کد ملی', max_length=10, blank=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد.')])
    bio = models.TextField('درباره من', blank=True)
    notes = models.TextField('یادداشت', blank=True, help_text='یادداشت معلم درباره دانش‌آموز')
    avatar = models.ImageField('تصویر پروفایل', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True, null=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        # default pomegranate avatar svg data uri handled in template; return None
        return None
