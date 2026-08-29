from django.urls import path
from .views import (
    RosterStudentListView, RosterStudentCreateView, RosterStudentUpdateView, RosterStudentDeleteView, RosterStudentDetailView,
    EnrolledStudentListView, EnrolledStudentDetailView, EnrolledStudentRemoveView
)

app_name = 'students'

urlpatterns = [
    # Roster (spec Student model)
    path('class/<int:class_pk>/roster/', RosterStudentListView.as_view(), name='roster_list'),
    path('class/<int:class_pk>/roster/create/', RosterStudentCreateView.as_view(), name='roster_create'),
    path('roster/<int:pk>/', RosterStudentDetailView.as_view(), name='roster_detail'),
    path('roster/<int:pk>/edit/', RosterStudentUpdateView.as_view(), name='roster_edit'),
    path('roster/<int:pk>/delete/', RosterStudentDeleteView.as_view(), name='roster_delete'),
    # Enrolled (auth User)
    path('class/<int:class_pk>/', EnrolledStudentListView.as_view(), name='list'),
    path('class/<int:class_pk>/user/<int:user_pk>/', EnrolledStudentDetailView.as_view(), name='detail'),
    path('class/<int:class_pk>/user/<int:user_pk>/remove/', EnrolledStudentRemoveView.as_view(), name='remove'),
]
