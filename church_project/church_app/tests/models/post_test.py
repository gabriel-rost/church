from django.test import TestCase
from django.contrib.auth.models import User
from church_app.models import Post, Content, Channel

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="123456")
        self.channel = Channel.objects.create(name="Canal de Teste")
        self.content = Content.objects.create(title="Título teste", text="Teste de post")
        self.post = Post.objects.create(content=self.content, user=self.user, channel=self.channel)

    def test_post_content(self):
        self.assertEqual(self.post.content.text, "Teste de post")

    def test_post_user(self):
        self.assertEqual(self.post.user.username, "joao")