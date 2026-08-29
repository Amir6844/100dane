def notifications_count(request):
    if request.user.is_authenticated:
        from .models import Notification
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
        recent = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        return {'notifications_unread': unread, 'notifications_recent': recent}
    return {}
