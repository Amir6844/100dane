from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='t1', password='pass12345', role=User.Role.TEACHER, first_name='معلم')
        self.student = User.objects.create_user(username='s1', password='pass12345', role=User.Role.STUDENT)
        self.teacher2 = User.objects.create_user(username='t2', password='pass12345', role=User.Role.TEACHER)

    def test_login(self):
        resp = self.client.post(reverse('accounts:login'), {'username': 't1', 'password': 'pass12345'})
        self.assertEqual(resp.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_protected_redirect(self):
        resp = self.client.get(reverse('classes:list'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login', resp.url)

    def test_logout(self):
        self.client.login(username='t1', password='pass12345')
        resp = self.client.post(reverse('accounts:logout'))
        # logout via POST with next_page
        self.assertIn(resp.status_code, [302, 200])

    def test_teacher_only_access(self):
        self.client.login(username='s1', password='pass12345')
        resp = self.client.get(reverse('classes:create'))
        # TeacherRequiredMixin redirects student to dashboard
        self.assertIn(resp.status_code, [302, 403])
