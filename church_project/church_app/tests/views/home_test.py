from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="joao", password="123456")

    def test_home_redirect_for_anonymous(self):
        response = self.client.get(reverse("home"))
        # redireciona para login
        self.assertEqual(response.status_code, 302)

    def test_home_authenticated(self):
        self.client.login(username="joao", password="123456")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")