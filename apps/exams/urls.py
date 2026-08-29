from django.urls import path
from .views import ExamListView, ExamCreateView, ExamUpdateView, ExamDeleteView, ExamDetailView
app_name='exams'
urlpatterns=[
    path('class/<int:class_pk>/', ExamListView.as_view(), name='list'),
    path('class/<int:class_pk>/create/', ExamCreateView.as_view(), name='create'),
    path('<int:pk>/', ExamDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ExamUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ExamDeleteView.as_view(), name='delete'),
]
