from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.mixins import TeacherRequiredMixin
from .models import Lesson
from .forms import LessonForm
from apps.classes.models import Classroom

class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'lessons/list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        self.classroom = get_object_or_404(Classroom, pk=self.kwargs['class_pk'])
        # check access
        user = self.request.user
        if not (user == self.classroom.teacher or user in self.classroom.students.all()):
            return Lesson.objects.none()
        return Lesson.objects.filter(classroom=self.classroom)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class LessonCreateView(TeacherRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'], teacher=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['classroom'] = self.classroom
        return kwargs

    def form_valid(self, form):
        form.instance.classroom = self.classroom
        # sync lesson_date/date
        if form.instance.lesson_date and not form.instance.date:
            form.instance.date = form.instance.lesson_date
        if form.instance.date and not form.instance.lesson_date:
            form.instance.lesson_date = form.instance.date
        messages.success(self.request, 'درس ایجاد شد.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('classes:detail', args=[self.classroom.pk]) + '?tab=lessons'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class LessonUpdateView(TeacherRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/form.html'

    def get_queryset(self):
        return Lesson.objects.filter(classroom__teacher=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['classroom'] = self.object.classroom
        return kwargs

    def form_valid(self, form):
        if form.instance.lesson_date and not form.instance.date:
            form.instance.date = form.instance.lesson_date
        if form.instance.date and not form.instance.lesson_date:
            form.instance.lesson_date = form.instance.date
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'درس بروزرسانی شد.')
        return reverse('classes:detail', args=[self.object.classroom.pk]) + '?tab=lessons'

class LessonDeleteView(TeacherRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'lessons/confirm_delete.html'

    def get_queryset(self):
        return Lesson.objects.filter(classroom__teacher=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'درس حذف شد.')
        return reverse('classes:detail', args=[self.object.classroom.pk]) + '?tab=lessons'

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lessons/detail.html'
    context_object_name = 'lesson'
