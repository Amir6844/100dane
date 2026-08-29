from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed demo data for 100dane'

    def handle(self, *args, **options):
        from apps.classes.models import Classroom
        from apps.groups.models import Group
        from apps.lessons.models import Lesson
        from apps.exams.models import Exam
        from apps.scores.models import Score

        # teacher
        teacher, created = User.objects.get_or_create(username='teacher', defaults={
            'first_name': 'مریم', 'last_name': 'احمدی', 'email': 'teacher@100dane.ir',
            'role': User.Role.TEACHER, 'phone': '09123456780'
        })
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(self.style.SUCCESS('Teacher created: teacher / teacher123'))
        else:
            self.stdout.write('Teacher exists')

        # students
        students = []
        names = [('علی','رضایی'),('سارا','محمدی'),('حسین','کریمی'),('نگار','حسینی'),('امیر','جعفری'),('فاطمه','نوری'),('محمد','صادقی'),('زهرا','موسوی')]
        for i, (fn, ln) in enumerate(names, 1):
            u, c = User.objects.get_or_create(username=f'student{i}', defaults={
                'first_name': fn, 'last_name': ln, 'role': User.Role.STUDENT, 'phone': f'0912000000{i}'
            })
            if c:
                u.set_password('student123')
                u.save()
            students.append(u)
        self.stdout.write(f'{len(students)} students ready')

        # classroom
        classroom, _ = Classroom.objects.get_or_create(name='ریاضی پایه دهم', teacher=teacher, defaults={
            'description': 'کلاس ریاضی پایه دهم - دبیر مریم احمدی. انار دانش، دانه‌های کنجکاوی!',
            'grade_level': '10',
            'color': '#C22A4E'
        })
        for s in students:
            classroom.students.add(s)
        # avoid unicode issue on Windows cp1252 console
        try:
            self.stdout.write(f'Classroom: {classroom.name} invite={classroom.invite_code}')
        except UnicodeEncodeError:
            self.stdout.write(f'Classroom invite={classroom.invite_code}')

        # groups
        g1, _ = Group.objects.get_or_create(classroom=classroom, name='گروه ستاره‌ها', defaults={'color':'#C22A4E', 'max_members':4})
        g2, _ = Group.objects.get_or_create(classroom=classroom, name='گروه انار', defaults={'color':'#3E9B4F', 'max_members':4})
        g1.members.set(students[:4])
        g2.members.set(students[4:])
        self.stdout.write('Groups created')

        # lesson
        lesson, _ = Lesson.objects.get_or_create(classroom=classroom, title='مثلثات - جلسه اول', defaults={
            'description': 'آشنایی با نسبت‌های مثلثاتی سینوس، کسینوس و تانژانت. تعریف دایره مثلثاتی و کاربرد آن.',
            'date': timezone.now().date(),
            'order': 1
        })
        Lesson.objects.get_or_create(classroom=classroom, title='معادله درجه دوم', defaults={'description':'حل معادله درجه دوم با دلتا و رسم نمودار سهمی','date':timezone.now().date(), 'order':2})

        # exam
        exam, _ = Exam.objects.get_or_create(classroom=classroom, title='کوییز فصل اول', defaults={
            'description': 'کوییز مثلثات - 5 سوال تستی',
            'total_score': 20,
            'exam_type': 'quiz',
            'date': timezone.now().date()
        })
        exam2, _ = Exam.objects.get_or_create(classroom=classroom, title='میان‌ترم نوبت اول', defaults={
            'total_score': 20, 'exam_type':'midterm', 'date': timezone.now().date()
        })

        # scores
        for e in [exam, exam2]:
            for s in students:
                Score.objects.update_or_create(exam=e, student=s, defaults={'value': round(random.uniform(10,20),1)})

        self.stdout.write(self.style.SUCCESS('Demo seeded! Login: teacher/teacher123 or student1/student123'))
