from django.urls import path
from .views import GroupCreateView, GroupUpdateView, GroupDeleteView, GroupAddMemberView, GroupRemoveMemberView, GroupMoveStudentView

app_name = 'groups'

urlpatterns = [
    path('class/<int:class_pk>/create/', GroupCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', GroupUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', GroupDeleteView.as_view(), name='delete'),
    path('<int:pk>/add-member/', GroupAddMemberView.as_view(), name='add_member'),
    path('<int:pk>/remove-member/', GroupRemoveMemberView.as_view(), name='remove_member'),
    path('<int:pk>/move/', GroupMoveStudentView.as_view(), name='move'),
]
