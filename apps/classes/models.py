import string, random
from django.db import models
from django.conf import settings

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Classroom(models.Model):
    class GradeLevel(models.TextChoices):
        SEVEN = '7', 'پایه هفتم'
        EIGHT = '8', 'پایه هشتم'
        NINTH = '9', 'پایه نهم'
        TENTH = '10', 'پایه دهم'
        ELEVENTH = '11', 'پایه یازدهم'
        TWELFTH = '12', 'پایه دوازدهم'
        OTHER = 'other', 'سایر'

    # spec fields: owner/teacher, title(name), description, academic_year, grade, field/subject, is_active
    name = models.CharField('نام کلاس', max_length=120, help_text='عنوان کلاس')
    title = models.CharField('عنوان', max_length=120, blank=True, help_text='نام جایگزین - برای سازگاری با مستندات')
    description = models.TextField('توضیحات', blank=True)
    academic_year = models.CharField('سال تحصیلی', max_length=9, blank=True, help_text='مثال: 1403-1404', default='1403-1404')
    grade_level = models.CharField('پایه تحصیلی', max_length=10, choices=GradeLevel.choices, default=GradeLevel.TENTH)
    subject = models.CharField('رشته/درس', max_length=100, blank=True, help_text='مثال: ریاضی، علوم')
    cover = models.ImageField('تصویر کاور', upload_to='covers/', blank=True, null=True)
    color = models.CharField('رنگ', max_length=7, default='#C22A4E', help_text='HEX color')
    invite_code = models.CharField('کد دعوت', max_length=6, unique=True, default=generate_invite_code, db_index=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_classes', verbose_name='دبیر')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_classes', blank=True, verbose_name='دانش‌آموزان')
    is_active = models.BooleanField('فعال', default=True, help_text='کلاس فعال/غیرفعال')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس‌ها'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['invite_code']), models.Index(fields=['teacher'])]

    def __str__(self):
        return f"{self.name} ({self.get_grade_level_display()})"

    def students_count(self):
        return self.students.count()

    @property
    def display_title(self):
        return self.title or self.name

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = generate_invite_code()
        # ensure unique
        while Classroom.objects.filter(invite_code=self.invite_code).exclude(pk=self.pk).exists():
            self.invite_code = generate_invite_code()
        # sync title/name for compatibility
        if not self.title:
            self.title = self.name
        if not self.name:
            self.name = self.title
        super().save(*args, **kwargs)
