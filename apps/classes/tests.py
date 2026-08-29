from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.classes.models import Classroom
from apps.groups.models import Group
from apps.lessons.models import Lesson
from apps.exams.models import Exam
from apps.scores.models import Score

User = get_user_model()

class ClassroomTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher', password='pass123', role=User.Role.TEACHER)
        self.teacher2 = User.objects.create_user(username='teacher2', password='pass123', role=User.Role.TEACHER)
        self.student = User.objects.create_user(username='student', password='pass123', role=User.Role.STUDENT)
        self.classroom = Classroom.objects.create(name='ریاضی 10', teacher=self.teacher, grade_level='10', academic_year='1403-1404', subject='ریاضی')
        self.classroom.students.add(self.student)

    def test_create_class(self):
        self.client.login(username='teacher', password='pass123')
        resp = self.client.post(reverse('classes:create'), {'name': 'کلاس جدید', 'grade_level': '10', 'academic_year': '1403-1404', 'subject': 'علوم', 'color': '#C22A4E'})
        self.assertIn(resp.status_code, [302, 200])
        self.assertTrue(Classroom.objects.filter(name='کلاس جدید').exists())

    def test_list_ownership(self):
        self.client.login(username='teacher2', password='pass123')
        resp = self.client.get(reverse('classes:list'))
        self.assertNotContains(resp, 'ریاضی 10')

    def test_edit_ownership(self):
        self.client.login(username='teacher2', password='pass123')
        resp = self.client.post(reverse('classes:edit', args=[self.classroom.pk]), {'name': 'hacked', 'grade_level': '10', 'color': '#000000'})
        self.assertIn(resp.status_code, [302, 403, 404])
        self.classroom.refresh_from_db()
        self.assertNotEqual(self.classroom.name, 'hacked')

    def test_delete(self):
        self.client.login(username='teacher', password='pass123')
        resp = self.client.post(reverse('classes:delete', args=[self.classroom.pk]))
        self.assertIn(resp.status_code, [302])
        self.assertFalse(Classroom.objects.filter(pk=self.classroom.pk).exists())

    def test_toggle_active(self):
        self.client.login(username='teacher', password='pass123')
        self.assertTrue(self.classroom.is_active)
        resp = self.client.post(reverse('classes:toggle_active', args=[self.classroom.pk]))
        self.classroom.refresh_from_db()
        self.assertFalse(self.classroom.is_active)

    def test_detail_stats(self):
        self.client.login(username='teacher', password='pass123')
        # create related objects
        Group.objects.create(classroom=self.classroom, name='گروه الف')
        Lesson.objects.create(classroom=self.classroom, title='درس 1')
        exam = Exam.objects.create(classroom=self.classroom, title='آزمون 1', total_score=20)
        Score.objects.create(exam=exam, student=self.student, value=15)
        resp = self.client.get(reverse('classes:detail', args=[self.classroom.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('stats', resp.context)

    def test_idor(self):
        self.client.login(username='teacher2', password='pass123')
        resp = self.client.get(reverse('classes:detail', args=[self.classroom.pk]))
        self.assertEqual(resp.status_code, 404)

class GroupMembershipTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='t', password='p', role=User.Role.TEACHER)
        self.s1 = User.objects.create_user(username='s1', password='p', role=User.Role.STUDENT)
        self.s2 = User.objects.create_user(username='s2', password='p', role=User.Role.STUDENT)
        self.outsider = User.objects.create_user(username='out', password='p', role=User.Role.STUDENT)
        self.classroom = Classroom.objects.create(name='کلاس', teacher=self.teacher)
        self.classroom.students.add(self.s1, self.s2)
        self.group = Group.objects.create(classroom=self.classroom, name='گروه')

    def test_add_member(self):
        self.client.login(username='t', password='p')
        resp = self.client.post(reverse('groups:add_member', args=[self.group.pk]), {'user_id': self.s1.id})
        self.assertIn(resp.status_code, [302, 200])
        self.assertIn(self.s1, self.group.members.all())

    def test_prevent_outsider(self):
        self.client.login(username='t', password='p')
        resp = self.client.post(reverse('groups:add_member', args=[self.group.pk]), {'user_id': self.outsider.id})
        self.group.refresh_from_db()
        self.assertNotIn(self.outsider, self.group.members.all())

    def test_duplicate_prevention(self):
        self.group.members.add(self.s1)
        self.client.login(username='t', password='p')
        self.client.post(reverse('groups:add_member', args=[self.group.pk]), {'user_id': self.s1.id})
        self.assertEqual(self.group.members.filter(pk=self.s1.pk).count(), 1)

    def test_remove(self):
        self.group.members.add(self.s1)
        self.client.login(username='t', password='p')
        self.client.post(reverse('groups:remove_member', args=[self.group.pk]), {'user_id': self.s1.id})
        self.assertNotIn(self.s1, self.group.members.all())

    def test_move(self):
        g2 = Group.objects.create(classroom=self.classroom, name='گروه2')
        self.group.members.add(self.s1)
        self.client.login(username='t', password='p')
        self.client.post(reverse('groups:move', args=[self.group.pk]), {'student_id': self.s1.id, 'target_group': g2.pk})
        self.assertNotIn(self.s1, self.group.members.all())
        self.assertIn(self.s1, g2.members.all())

    def test_unauthorized_group_edit(self):
        t2 = User.objects.create_user(username='t2', password='p', role=User.Role.TEACHER)
        self.client.login(username='t2', password='p')
        resp = self.client.get(reverse('groups:edit', args=[self.group.pk]))
        self.assertIn(resp.status_code, [404, 403, 302])

class LessonTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='t', password='p', role=User.Role.TEACHER)
        self.classroom = Classroom.objects.create(name='ک', teacher=self.teacher)
        self.group = Group.objects.create(classroom=self.classroom, name='گ')

    def test_create_lesson(self):
        self.client.login(username='t', password='p')
        resp = self.client.post(reverse('lessons:create', args=[self.classroom.pk]), {'title': 'درس', 'description': 'توضیح', 'order': 1, 'group': self.group.pk})
        self.assertIn(resp.status_code, [302, 200])
        self.assertTrue(Lesson.objects.filter(title='درس').exists())

    def test_homework_field(self):
        self.client.login(username='t', password='p')
        self.client.post(reverse('lessons:create', args=[self.classroom.pk]), {'title': 'درس2', 'homework': 'تمرین صفحه 10', 'order': 2})
        self.assertEqual(Lesson.objects.get(title='درس2').homework, 'تمرین صفحه 10')

class ExamTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='t', password='p', role=User.Role.TEACHER)
        self.classroom = Classroom.objects.create(name='ک', teacher=self.teacher)

    def test_create_exam_valid(self):
        self.client.login(username='t', password='p')
        resp = self.client.post(reverse('exams:create', args=[self.classroom.pk]), {'title': 'آزمون', 'total_score': 20, 'exam_type': 'quiz', 'date': '2024-01-01'})
        self.assertIn(resp.status_code, [302, 200])
        self.assertTrue(Exam.objects.filter(title='آزمون').exists())

    def test_create_exam_invalid_score(self):
        self.client.login(username='t', password='p')
        resp = self.client.post(reverse('exams:create', args=[self.classroom.pk]), {'title': 'آزمون بد', 'total_score': -5, 'exam_type': 'quiz'})
        self.assertEqual(resp.status_code, 200)  # form error
        self.assertFalse(Exam.objects.filter(title='آزمون بد').exists())

    def test_exam_group_optional(self):
        g = Group.objects.create(classroom=self.classroom, name='گ')
        self.client.login(username='t', password='p')
        self.client.post(reverse('exams:create', args=[self.classroom.pk]), {'title': 'آزمون گروهی', 'total_score': 20, 'exam_type': 'quiz', 'group': g.pk})
        ex = Exam.objects.get(title='آزمون گروهی')
        self.assertEqual(ex.group, g)
