from django.test import TestCase, Client
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from noodle.models import Staff
from noodle.models import Student
from noodle.models import User
from noodle.models import Course
from django.contrib.auth.models import User
from django.contrib.auth import login
from noodle.models import UserProfile
from noodle.models import Subject
from noodle.models import Assessment
from noodle.models import Material

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

#Test serving static files
class GeneralTests(TestCase):
    def test_serving_static_files(self):
        result = finders.find('images/logo.gif')
        self.assertIsNotNone(result)

    def test_serving_static_files(self):
        result = finders.find('images/homepage_image.jpg')
        self.assertIsNotNone(result)

#Test home page
class NoodleViewTestCase(TestCase):
    def test_welcome_message(self):
        resp = self.client.get('/noodle/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Welcome To Noodle', resp.content)

    def test_homepage(self):
        resp = self.client.get('/')
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

#test Register view
class RegisterViewTestCase(TestCase):
    def test_register(self):
        resp = self.client.get('/noodle/register/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Staff Register here!', resp.content)
        self.assertIn('Students Register here!', resp.content)
        self.assertIn('Registration', resp.content)

#Test login view
class LoginViewTestCase(TestCase):
    def test_login(self):
        resp = self.client.get('/noodle/login/')
        self.assertEqual(resp.status_code, 200)

class teachHomeViewTestCase(TestCase):
    def test_teachhome(self):
        resp = self.client.post('/noodle/teachhome/',follow=True)
        self.assertEqual(resp.status_code, 200)

class teachHomeAdd_assessmentViewTestCase(TestCase):
    def test_add_assessment(self):
        resp = self.client.post('/noodle/teachhome/add_assessment/',follow=True)
        self.assertEqual(resp.status_code, 200)

# Create test user and register
class TestRegisterStudentTestCase(TestCase):
    def test_register_student(self):
        resp = self.client.post(reverse('noodle/register/student'),
                                    {'username': 'test', 'password': 'testpassword',
                                     'email': 'test@gmail.com',
                                     'subject':'asd,',
                                     'yearOfStudy':'1'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Thank you for Registering with Noodle.', resp.content)

class TestRegisterStaffTestCase(TestCase):
    def test_register_staff(self):
        resp = self.client.post(reverse('noodle/register/staff'),
                                    {'username': 'test', 'password': 'testpassword',
                                     'email': 'test@gmail.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Thank you for Registering with Noodle.', resp.content)

class studentHomeAdd_assessmentViewTestCase(TestCase):
    def test_add_asessment(self):
        resp = self.client.get('/noodle/studenthome/add_assessment/')
        self.assertEqual(resp.status_code, 200)

class logoutViewTestCase(TestCase):
    def test_logout(self):
        self.client.post(reverse('noodle/register/student'),
                         {'username': 'test', 'password': 'testpassword',
                          'email': 'test@gmail.com',
                          'subject': 'asd,',
                          'yearOfStudy': '1'})
        resp = self.client.get('/noodle/logout/')
        self.assertEqual(resp.status_code, 200)


# Test population script and add subjects
class PopulateTest(TestCase):

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
            subject = Subject.objects.get_or_create(name=name)
        except Subject.DoesNotExist:
                subject = None
        return subject

    def test_history_added(self):
        subject = self.get_subject('History')
        self.assertIsNotNone(subject)

    def test_maths_added(self):
        subject = self.get_subject('Mathematics')
        self.assertIsNotNone(subject)

# Test course model
class CourseTest(TestCase):

    def test_Course(self):
        course = Course(name = 'WAD2')
        self.assertEqual(unicode(course), course.name)

# Test the forms
class FormsTesting(TestCase):
    def test_forms(self):
        try:
            from forms import SubjectForm
            from forms import CourseForm
            from forms import MaterialForm
            from forms import FileForm
            from forms import AssignmentForm
            from forms import StudentSubmissionForm
            from forms import AnnouncementForm
            from forms import UserForm
            from forms import StudentUserProfileForm
            from forms import StaffUserProfileForm
            from forms import MarkingForm
            from forms import StudentSearchForm

            pass
        except ImportError:
            print('Error importing the module')

        except:
            print('Error')

#slug test
class SlugFieldTests(TestCase):

    # tests if slug field works
    def test_slug_field(self):
        from noodle.models import Subject
        subject = Subject(name='subject')
        subject.save()
        self.assertEqual(subject.slug,'subject')



