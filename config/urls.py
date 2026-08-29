from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import LandingView
from apps.scores.views import ReportsDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='landing'),
    path('accounts/', include('apps.accounts.urls')),
    path('classes/', include('apps.classes.urls')),
    path('students/', include('apps.students.urls')),
    path('groups/', include('apps.groups.urls')),
    path('lessons/', include('apps.lessons.urls')),
    path('exams/', include('apps.exams.urls')),
    path('scores/', include('apps.scores.urls')),
    path('reports/', ReportsDashboardView.as_view(), name='reports'),
    path('notifications/', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'apps.accounts.views.handler400'
handler403 = 'apps.accounts.views.handler403'
handler404 = 'apps.accounts.views.handler404'
handler500 = 'apps.accounts.views.handler500'
