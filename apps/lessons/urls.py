from django.urls import path
from .views import LessonListView, LessonCreateView, LessonUpdateView, LessonDeleteView, LessonDetailView

app_name = 'lessons'

urlpatterns = [
    path('class/<int:class_pk>/', LessonListView.as_view(), name='list'),
    path('class/<int:class_pk>/create/', LessonCreateView.as_view(), name='create'),
    path('<int:pk>/', LessonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', LessonUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', LessonDeleteView.as_view(), name='delete'),
]
