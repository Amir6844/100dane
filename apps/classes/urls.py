from django.urls import path
from .views import ClassListView, ClassCreateView, ClassUpdateView, ClassDeleteView, ClassDetailView, JoinClassView, LeaveClassView, RegenerateInviteView, ToggleActiveView

app_name = 'classes'

urlpatterns = [
    path('', ClassListView.as_view(), name='list'),
    path('create/', ClassCreateView.as_view(), name='create'),
    path('<int:pk>/', ClassDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ClassUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ClassDeleteView.as_view(), name='delete'),
    path('join/', JoinClassView.as_view(), name='join'),
    path('<int:pk>/leave/', LeaveClassView.as_view(), name='leave'),
    path('<int:pk>/regenerate-invite/', RegenerateInviteView.as_view(), name='regenerate_invite'),
    path('<int:pk>/toggle-active/', ToggleActiveView.as_view(), name='toggle_active'),
]
