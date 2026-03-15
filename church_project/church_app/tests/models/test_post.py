from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from church_app.models import Post, Channel

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="123456")
        self.channel = Channel.objects.create(name="Canal de Teste")
        self.title="Título teste"
        self.text="Teste de post"
        self.post = Post.objects.create(user=self.user, channel=self.channel)

    def test_post_content(self):
        self.assertEqual(self.text, "Teste de post")

    def test_post_user(self):
        self.assertEqual(self.user.username, "joao")