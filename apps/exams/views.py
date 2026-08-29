from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.mixins import TeacherRequiredMixin
from .models import Exam
from .forms import ExamForm
from apps.classes.models import Classroom
from apps.notifications.models import Notification

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/list.html'
    context_object_name = 'exams'
    def get_queryset(self):
        self.classroom = get_object_or_404(Classroom, pk=self.kwargs['class_pk'])
        return Exam.objects.filter(classroom=self.classroom)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class ExamCreateView(TeacherRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/form.html'
    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'], teacher=request.user)
        return super().dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['classroom'] = self.classroom
        return kwargs
    def form_valid(self, form):
        form.instance.classroom = self.classroom
        resp = super().form_valid(form)
        # notify students
        for s in self.classroom.students.all():
            Notification.objects.create(user=s, title='آزمون جدید', message=f"آزمون «{form.instance.title}» در کلاس {self.classroom.name} ایجاد شد.", link=reverse('classes:detail', args=[self.classroom.pk]) + '?tab=exams')
        messages.success(self.request, 'آزمون ایجاد شد.')
        return resp
    def get_success_url(self):
        return reverse('classes:detail', args=[self.classroom.pk]) + '?tab=exams'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class ExamUpdateView(TeacherRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/form.html'
    def get_queryset(self):
        return Exam.objects.filter(classroom__teacher=self.request.user)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['classroom'] = self.object.classroom
        return kwargs
    def get_success_url(self):
        messages.success(self.request, 'آزمون بروزرسانی شد.')
        return reverse('classes:detail', args=[self.object.classroom.pk]) + '?tab=exams'

class ExamDeleteView(TeacherRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/confirm_delete.html'
    def get_queryset(self):
        return Exam.objects.filter(classroom__teacher=self.request.user)
    def get_success_url(self):
        messages.success(self.request, 'آزمون حذف شد.')
        return reverse('classes:detail', args=[self.object.classroom.pk]) + '?tab=exams'

class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/detail.html'
    context_object_name = 'exam'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.scores.models import Score
        ctx['scores'] = Score.objects.filter(exam=self.object).select_related('student')
        return ctx
