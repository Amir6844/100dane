from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import JsonResponse
from apps.accounts.mixins import TeacherRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group
from .forms import GroupForm
from apps.classes.models import Classroom
from apps.notifications.models import Notification

class GroupCreateView(TeacherRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'], teacher=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.classroom = self.classroom
        messages.success(self.request, 'گروه ایجاد شد.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('classes:detail', args=[self.classroom.pk]) + '?tab=groups'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class GroupUpdateView(TeacherRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/form.html'

    def get_queryset(self):
        return Group.objects.filter(classroom__teacher=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'گروه بروزرسانی شد.')
        return reverse('classes:detail', args=[self.object.classroom.pk]) + '?tab=groups'

class GroupDeleteView(TeacherRequiredMixin, DeleteView):
    model = Group
    template_name = 'groups/confirm_delete.html'

    def get_queryset(self):
        return Group.objects.filter(classroom__teacher=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'گروه حذف شد.')
        return reverse('classes:detail', args=[self.object.classroom.pk]) + '?tab=groups'

class GroupAddMemberView(TeacherRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk, classroom__teacher=request.user)
        user_id = request.POST.get('user_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        student = get_object_or_404(User, pk=user_id)
        if student not in group.classroom.students.all():
            messages.error(request, 'این دانش‌آموز عضو کلاس نیست.')
        elif group.members.count() >= group.max_members:
            messages.error(request, 'ظرفیت گروه تکمیل است.')
        else:
            group.members.add(student)
            messages.success(request, f'{student.get_full_name() or student.username} به گروه اضافه شد.')
            Notification.objects.create(user=student, title='افزوده شدن به گروه', message=f'شما به گروه «{group.name}» در کلاس {group.classroom.name} اضافه شدید.', link=reverse('classes:detail', args=[group.classroom.pk]) + '?tab=groups')
        if request.headers.get('HX-Request'):
            return render(request, 'groups/_group_card.html', {'group': group, 'classroom': group.classroom})
        return redirect(reverse('classes:detail', args=[group.classroom.pk]) + '?tab=groups')

class GroupRemoveMemberView(TeacherRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk, classroom__teacher=request.user)
        user_id = request.POST.get('user_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        student = get_object_or_404(User, pk=user_id)
        group.members.remove(student)
        messages.success(request, 'عضو از گروه حذف شد.')
        if request.headers.get('HX-Request'):
            return render(request, 'groups/_group_card.html', {'group': group, 'classroom': group.classroom})
        return redirect(reverse('classes:detail', args=[group.classroom.pk]) + '?tab=groups')

class GroupMoveStudentView(TeacherRequiredMixin, View):
    def post(self, request, pk):
        # bulk move: student_id, target_group_id
        group = get_object_or_404(Group, pk=pk, classroom__teacher=request.user)
        target_id = request.POST.get('target_group')
        student_id = request.POST.get('student_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        student = get_object_or_404(User, pk=student_id)
        target = get_object_or_404(Group, pk=target_id, classroom=group.classroom)
        group.members.remove(student)
        target.members.add(student)
        messages.success(request, 'دانش‌آموز جابه‌جا شد.')
        return redirect(reverse('classes:detail', args=[group.classroom.pk]) + '?tab=groups')
