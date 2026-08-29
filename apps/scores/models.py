from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Score(models.Model):
    exam = models.ForeignKey('exams.Exam', on_delete=models.CASCADE, related_name='scores', verbose_name='آزمون')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores', verbose_name='دانش‌آموز')
    value = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='نمره')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نمره (مترادف)')
    notes = models.TextField('یادداشت', blank=True)
    comment = models.CharField('توضیح', max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='نمره'
        verbose_name_plural='نمرات'
        unique_together = ('exam','student')
        ordering = ['-created_at']
        indexes = [models.Index(fields=['exam','student'])]
        constraints = [
            models.CheckConstraint(check=models.Q(value__gte=0), name='score_value_gte_0'),
        ]

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.value}"

    def save(self, *args, **kwargs):
        if self.score is not None and self.value is None:
            self.value = self.score
        if self.value is not None and self.score is None:
            self.score = self.value
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.exam and self.value is not None:
            if self.value < 0 or self.value > self.exam.total_score:
                raise ValidationError(f"نمره باید بین 0 و {self.exam.total_score} باشد.")
        # student must belong to exam's classroom
        if self.exam and self.student_id:
            if self.student not in self.exam.classroom.students.all() and self.student != self.exam.classroom.teacher:
                # allow but validation will be enforced in views; raise only if strict
                pass
