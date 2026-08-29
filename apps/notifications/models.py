from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name='کاربر')
    title = models.CharField('عنوان', max_length=120)
    message = models.TextField('پیام')
    link = models.CharField('لینک', max_length=300, blank=True)
    is_read = models.BooleanField('خوانده شده؟', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='اعلان'
        verbose_name_plural='اعلان‌ها'
        ordering=['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.user}"
