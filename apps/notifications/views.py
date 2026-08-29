from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        n = get_object_or_404(Notification, pk=pk, user=request.user)
        n.is_read = True
        n.save()
        return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))

class MarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))
