from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg, Max, Min, Count
from apps.accounts.mixins import TeacherRequiredMixin
from apps.classes.models import Classroom
from .models import Student
from .forms import StudentForm, EnrolledStudentForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Roster-based students (spec Student model)
class RosterStudentListView(TeacherRequiredMixin, ListView):
    model = Student
    template_name = 'students/roster_list.html'
    context_object_name = 'students'

    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'], teacher=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Student.objects.filter(classroom=self.classroom).select_related('user')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class RosterStudentCreateView(TeacherRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/roster_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'], teacher=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['classroom'] = self.classroom
        return kwargs

    def form_valid(self, form):
        form.instance.classroom = self.classroom
        messages.success(self.request, 'دانش‌آموز به فهرست اضافه شد.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('students:roster_list', args=[self.classroom.pk])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        return ctx

class RosterStudentUpdateView(TeacherRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/roster_form.html'

    def get_queryset(self):
        return Student.objects.filter(classroom__teacher=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['classroom'] = self.object.classroom
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'اطلاعات دانش‌آموز بروزرسانی شد.')
        return reverse('students:roster_list', args=[self.object.classroom.pk])

class RosterStudentDeleteView(TeacherRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/roster_confirm_delete.html'

    def get_queryset(self):
        return Student.objects.filter(classroom__teacher=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'دانش‌آموز از فهرست حذف شد.')
        return reverse('students:roster_list', args=[self.object.classroom.pk])

class RosterStudentDetailView(TeacherRequiredMixin, DetailView):
    model = Student
    template_name = 'students/roster_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.filter(classroom__teacher=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.object
        # if linked to User, show score stats via User
        if student.user:
            from apps.scores.models import Score
            scores = Score.objects.filter(student=student.user).select_related('exam', 'exam__classroom')
            agg = scores.aggregate(avg=Avg('value'), mx=Max('value'), mn=Min('value'), cnt=Count('id'))
            ctx['stats'] = agg
            ctx['scores'] = scores.order_by('-created_at')[:20]
        else:
            ctx['stats'] = {'avg': None, 'mx': None, 'mn': None, 'cnt': 0}
            ctx['scores'] = []
        return ctx

# Enrolled (auth User) students management
class EnrolledStudentListView(LoginRequiredMixin, ListView):
    template_name = 'students/enrolled_list.html'
    context_object_name = 'students'

    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'])
        # check ownership or enrollment
        if not (request.user == self.classroom.teacher or request.user in self.classroom.students.all()):
            from django.http import Http404
            raise Http404("دسترسی غیرمجاز")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.classroom.students.all().order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['classroom'] = self.classroom
        # stats per student using aggregation
        from apps.scores.models import Score
        ctx['report'] = Score.objects.filter(exam__classroom=self.classroom).values('student').annotate(avg=Avg('value'))
        return ctx

class EnrolledStudentDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'students/detail.html'
    context_object_name = 'student'
    pk_url_kwarg = 'user_pk'

    def dispatch(self, request, *args, **kwargs):
        self.classroom = get_object_or_404(Classroom, pk=kwargs['class_pk'])
        user = request.user
        if not (user == self.classroom.teacher or user in self.classroom.students.all() or str(user.pk) == str(kwargs.get('user_pk'))):
            # allow teacher or self
            if user != self.classroom.teacher:
                from django.http import Http404
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # only students of this classroom or teacher
        return User.objects.filter(enrolled_classes=self.classroom) | User.objects.filter(pk=self.classroom.teacher.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.object
        ctx['classroom'] = self.classroom
        from apps.scores.models import Score
        scores = Score.objects.filter(student=student, exam__classroom=self.classroom).select_related('exam').order_by('-created_at')
        agg = scores.aggregate(avg=Avg('value'), mx=Max('value'), mn=Min('value'), cnt=Count('id'))
        # convert None handling
        ctx['avg'] = round(agg['avg'], 2) if agg['avg'] else None
        ctx['highest'] = agg['mx']
        ctx['lowest'] = agg['mn']
        ctx['exam_count'] = agg['cnt']
        ctx['scores'] = scores
        # groups of student
        from apps.groups.models import Group
        ctx['groups'] = Group.objects.filter(classroom=self.classroom, members=student)
        return ctx

class EnrolledStudentRemoveView(TeacherRequiredMixin, View):
    def post(self, request, class_pk, user_pk):
        classroom = get_object_or_404(Classroom, pk=class_pk, teacher=request.user)
        student = get_object_or_404(User, pk=user_pk)
        classroom.students.remove(student)
        # also remove from groups
        for g in classroom.groups.filter(members=student):
            g.members.remove(student)
        messages.success(request, 'دانش‌آموز از کلاس حذف شد.')
        return redirect('classes:detail', pk=classroom.pk)
