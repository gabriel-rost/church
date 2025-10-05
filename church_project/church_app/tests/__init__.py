from django.test import TestCase

from .forms.signup_test import SignUpFormTest
from .models.post_test import PostModelTest
from .views.home_test import HomeViewTest

def run_all_tests():
    SignUpFormTest()
    PostModelTest()
    HomeViewTest()