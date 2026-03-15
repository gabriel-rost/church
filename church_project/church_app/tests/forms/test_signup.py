from django.test import TestCase
from church_app.forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'joao',
            'email': 'joao@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': '',
            'email': 'joao@example.com',
            'password1': '123',
            'password2': '321'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())