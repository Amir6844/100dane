from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.db.models import Avg, Q
from .models import Classroom
from .forms import ClassroomForm, JoinClassForm
from apps.accounts.mixins import TeacherRequiredMixin
from apps.notifications.models import Notification

class ClassListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = 'classes/list.html'
    context_object_name = 'classes'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        q = self.request.GET.get('q')
        if user.is_teacher:
            qs = Classroom.objects.filter(teacher=user)
        else:
            qs = user.enrolled_classes.all()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['join_form'] = JoinClassForm()
        return ctx

class ClassCreateView(TeacherRequiredMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classes/form.html'
    success_url = reverse_lazy('classes:list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'کلاس با موفقیت ایجاد شد.')
        return super().form_valid(form)

class ClassUpdateView(TeacherRequiredMixin, UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classes/form.html'

    def get_queryset(self):
        return Classroom.objects.filter(teacher=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'کلاس بروزرسانی شد.')
        return reverse('classes:detail', args=[self.object.pk])

class ClassDeleteView(TeacherRequiredMixin, DeleteView):
    model = Classroom
    template_name = 'classes/confirm_delete.html'
    success_url = reverse_lazy('classes:list')

    def get_queryset(self):
        return Classroom.objects.filter(teacher=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'کلاس حذف شد.')
        return super().delete(request, *args, **kwargs)

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Classroom
    template_name = 'classes/detail.html'
    context_object_name = 'classroom'

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Classroom.objects.filter(teacher=user)
        return user.enrolled_classes.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        classroom = self.object
        # optimized tabs data with select_related/prefetch
        ctx['students'] = classroom.students.prefetch_related().all()
        from apps.groups.models import Group
        ctx['groups'] = Group.objects.filter(classroom=classroom).prefetch_related('members')
        from apps.lessons.models import Lesson
        ctx['lessons'] = Lesson.objects.filter(classroom=classroom).select_related('group').order_by('order', '-date')
        from apps.exams.models import Exam
        ctx['exams'] = Exam.objects.filter(classroom=classroom).select_related('group', 'lesson').order_by('-date')
        # scores matrix for report
        from apps.scores.models import Score
        ctx['scores'] = Score.objects.filter(exam__classroom=classroom).select_related('student', 'exam')
        # use reusable stats service
        from apps.scores.services import class_stats
        ctx['stats'] = class_stats(classroom)
        # keep report for backward compat but use efficient query
        from django.db.models import Avg
        students = classroom.students.all()
        report = []
        for s in students:
            avg = Score.objects.filter(student=s, exam__classroom=classroom).aggregate(avg=Avg('value'))['avg']
            report.append({'student': s, 'avg': round(avg,2) if avg else None})
        report.sort(key=lambda x: (x['avg'] is None, - (x['avg'] or 0)))
        for i, r in enumerate(report, 1):
            r['rank'] = i if r['avg'] is not None else '-'
        ctx['report'] = report
        ctx['active_tab'] = self.request.GET.get('tab', 'students')
        return ctx

class JoinClassView(LoginRequiredMixin, View):
    def post(self, request):
        form = JoinClassForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['invite_code'].upper()
            try:
                classroom = Classroom.objects.get(invite_code=code)
            except Classroom.DoesNotExist:
                messages.error(request, 'کد دعوت نامعتبر است.')
                return redirect('classes:list')
            if request.user in classroom.students.all() or classroom.teacher == request.user:
                messages.warning(request, 'شما قبلا عضو این کلاس هستید.')
            else:
                classroom.students.add(request.user)
                messages.success(request, f'به کلاس «{classroom.name}» پیوستید.')
                Notification.objects.create(user=classroom.teacher, title='دانش‌آموز جدید', message=f'{request.user.get_full_name() or request.user.username} به کلاس {classroom.name} پیوست.', link=reverse('classes:detail', args=[classroom.pk]))
        else:
            messages.error(request, 'کد دعوت را صحیح وارد کنید.')
        return redirect('classes:list')

class LeaveClassView(LoginRequiredMixin, View):
    def post(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk)
        if request.user in classroom.students.all():
            classroom.students.remove(request.user)
            messages.success(request, 'از کلاس خارج شدید.')
        return redirect('classes:list')

class RegenerateInviteView(TeacherRequiredMixin, View):
    def post(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
        import string, random
        classroom.invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        classroom.save()
        messages.success(request, 'کد دعوت جدید ایجاد شد.')
        return redirect('classes:detail', pk=pk)

class ToggleActiveView(TeacherRequiredMixin, View):
    def post(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
        classroom.is_active = not classroom.is_active
        classroom.save(update_fields=['is_active'])
        status = 'فعال' if classroom.is_active else 'غیرفعال'
        messages.success(request, f'کلاس {status} شد.')
        return redirect('classes:detail', pk=pk)
