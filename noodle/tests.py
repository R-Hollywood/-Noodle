from django.test import TestCase
from django.contrib.staticfiles import finders
from noodle.models import Staff

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class GeneralTests(TestCase):
    def test_serving_static_files(self):
        result = finders.find('images/logo.gif')
        self.assertIsNotNone(result)

    def test_serving_static_files(self):
        result = finders.find('images/homepage_image.jpg')
        self.assertIsNotNone(result)

class NoodleViewTestCase(TestCase):
    def test_welcome_message(self):
        resp = self.client.get('/noodle/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Welcome To Noodle', resp.content)

    def test_template(self):
        resp = self.client.get('/noodle/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'noodle/homepage_extends_base.html')

    def test_logo_displayed(self):
        resp = self.client.get('/noodle/')
        self.assertIn('img src="/static/images/logo.gif', resp.content)

    def test_contains_message(self):
        resp = self.client.get('/noodle/')
        self.assertIn('Not The Learning Management Service You Need.', resp.content)

class LoginViewTestCase(TestCase):
    def test_login(self):
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)

class RegisterViewTestCase(TestCase):
    def test_register(self):
        resp = self.client.get('/accounts/register/')
        self.assertEqual(resp.status_code, 200)

class teachHomeViewTestCase(TestCase):
    def test_teachhome(self):
        resp = self.client.get('/teachhome/')
        self.assertEqual(resp.status_code, 200)

class teachHomeAdd_assessmentViewTestCase(TestCase):
    def test_add_assessment(self):
        resp = self.client.get('/teachhome/add_assessment/')
        self.assertEqual(resp.status_code, 200)

class studenthHomeViewTestCase(TestCase):
    def test_studenthome(self):
        resp = self.client.get('/studenthome/')
        self.assertEqual(resp.status_code, 200)

class studentHomeAdd_assessmentViewTestCase(TestCase):
    def test_add_asessment(self):
        resp = self.client.get('/studenthome/add_assessment/')
        self.assertEqual(resp.status_code, 200)

class logoutViewTestCase(TestCase):
    def test_logout(self):
        resp = self.client.get('/accounts/logout/')
        self.assertEqual(resp.status_code, 200)

class ModelsTest(TestCase):

    def test_setUp(self):
        try:
            from population_script import populate
            populate()
        except ImportError:
            print('The module population_script does not exist')
        except NameError:
            print('Function populate() does not exist or has error')
        except:
            print('An error occured with populate() function')

    def get_subject(self, name):

        from noodle.models import Subject
        try:
            subject = Subject.objects.get(name=name)
        except Subject.DoesNotExist:
                subject = None
        return subject

    def test_history_added(self):
        subject = self.get_subject('History')
        self.assertIsNotNone(subject)

    def test_maths_added(self):
        subject = self.get_subject('Mathematics')
        self.assertIsNotNone(subject)
