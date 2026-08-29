from django.db import models

class Exam(models.Model):
    class ExamType(models.TextChoices):
        QUIZ = 'quiz', 'کوییز'
        MIDTERM = 'midterm', 'میان‌ترم'
        FINAL = 'final', 'پایانی'
        HOMEWORK = 'homework', 'تمرین'
        OTHER = 'other', 'سایر'

    classroom = models.ForeignKey('classes.Classroom', on_delete=models.CASCADE, related_name='exams', verbose_name='کلاس')
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='exams', verbose_name='گروه (اختیاری)')
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='exams', verbose_name='درس مرتبط')
    title = models.CharField('عنوان آزمون', max_length=200)
    description = models.TextField('توضیحات', blank=True)
    date = models.DateField('تاریخ برگزاری', null=True, blank=True)
    exam_date = models.DateField(null=True, blank=True, verbose_name='تاریخ آزمون', help_text='نام جایگزین برای date')
    total_score = models.DecimalField('نمره کل', max_digits=4, decimal_places=2, default=20)
    maximum_score = models.DecimalField(max_digits=4, decimal_places=2, default=20, blank=True, null=True, verbose_name='حداکثر نمره (مترادف)')
    exam_type = models.CharField('نوع آزمون', max_length=10, choices=ExamType.choices, default=ExamType.QUIZ)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='آزمون'
        verbose_name_plural='آزمون‌ها'
        ordering=['-date','-created_at']

    def save(self, *args, **kwargs):
        if self.exam_date and not self.date:
            self.date = self.exam_date
        if self.date and not self.exam_date:
            self.exam_date = self.date
        # sync maximum_score / total_score
        if self.maximum_score is None:
            self.maximum_score = self.total_score
        else:
            self.total_score = self.maximum_score
        super().save(*args, **kwargs)

    @property
    def max_score(self):
        return self.total_score

    def __str__(self):
        return f"{self.title} - {self.classroom.name}"

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name='آزمون')
    text = models.TextField('متن سوال')
    score = models.DecimalField('بارم', max_digits=4, decimal_places=2, default=1)
    is_multiple_choice = models.BooleanField('چهارگزینه‌ای؟', default=False)
    choices = models.TextField('گزینه‌ها (هر خط یک گزینه)', blank=True)

    class Meta:
        verbose_name='سوال'
        verbose_name_plural='سوال‌ها'

    def __str__(self):
        return self.text[:50]
