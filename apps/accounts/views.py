from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView, View
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from .forms import RegisterForm, LoginForm, ProfileForm

User = get_user_model()

class LandingView(TemplateView):
    template_name = 'landing.html'

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'ثبت‌نام با موفقیت انجام شد. خوش آمدید!')
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'خوش آمدید!')
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.is_teacher:
            return ['accounts/dashboard_teacher.html']
        return ['accounts/dashboard_student.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_teacher:
            from apps.classes.models import Classroom
            from apps.exams.models import Exam
            classes = Classroom.objects.filter(teacher=user)
            ctx['classes'] = classes[:6]
            ctx['classes_count'] = classes.count()
            # students count
            from apps.classes.models import Classroom
            # total students across classes
            total_students = User.objects.filter(enrolled_classes__teacher=user).distinct().count()
            ctx['students_count'] = total_students
            ctx['recent_exams'] = Exam.objects.filter(classroom__teacher=user).order_by('-created_at')[:5]
            # avg score across all exams of teacher
            from apps.scores.models import Score
            avg = Score.objects.filter(exam__classroom__teacher=user).aggregate(avg=Avg('value'))['avg']
            ctx['avg_score'] = round(avg, 2) if avg else None
            ctx['exams_count'] = Exam.objects.filter(classroom__teacher=user).count()
        else:
            from apps.scores.models import Score
            ctx['my_classes'] = user.enrolled_classes.select_related('teacher').all()
            ctx['my_scores'] = Score.objects.filter(student=user).select_related('exam', 'exam__classroom').order_by('-created_at')[:5]
            avg = Score.objects.filter(student=user).aggregate(avg=Avg('value'))['avg']
            ctx['avg_score'] = round(avg, 2) if avg else None
            from apps.groups.models import Group
            ctx['my_groups'] = Group.objects.filter(members=user).select_related('classroom')[:5]
            # also fix related_name usage if needed - member_groups handled via filter
        # notifications
        from apps.notifications.models import Notification
        ctx['recent_notifications'] = Notification.objects.filter(user=user).order_by('-created_at')[:4]
        return ctx

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'پروفایل با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)

def handler400(request, exception):
    return render(request, '400.html', status=400)

def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
