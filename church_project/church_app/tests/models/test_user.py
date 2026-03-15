from django.test import TestCase
from django.contrib.auth import get_user_model
from church_app.models import Archive

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="joao",
            email="joao@example.com",
            password="senha123",
            first_name="João",
            last_name="Silva",
        )

    # --- __str__ ---

    def test_str_retorna_nome_completo(self):
        self.assertEqual(str(self.user), "João Silva")

    def test_str_retorna_username_quando_sem_nome(self):
        user = User.objects.create_user(username="anonimo", password="senha123")
        self.assertEqual(str(user), "anonimo")

    # --- Campos opcionais ---

    def test_campos_opcionais_sao_nulos_por_padrao(self):
        self.assertIsNone(self.user.avatar)
        self.assertIsNone(self.user.birth_date)
        self.assertIsNone(self.user.bio)
        self.assertEqual(self.user.phone, "")
        self.assertEqual(self.user.location, "")

    def test_salvar_bio(self):
        self.user.bio = "Membro desde 2020."
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "Membro desde 2020.")

    def test_salvar_phone(self):
        self.user.phone = "51999999999"
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "51999999999")

    def test_salvar_location(self):
        self.user.location = "Porto Alegre, RS"
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.location, "Porto Alegre, RS")

    def test_salvar_birth_date(self):
        from datetime import date
        self.user.birth_date = date(1990, 5, 20)
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.birth_date, date(1990, 5, 20))

    # --- Avatar (FK para Archive) ---

    def test_associar_avatar(self):
        archive = Archive.objects.create(file="avatars/foto.jpg")
        self.user.avatar = archive
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.avatar, archive)

    def test_deletar_archive_nao_deleta_usuario(self):
        archive = Archive.objects.create(file="avatars/foto.jpg")
        self.user.avatar = archive
        self.user.save()
        archive.delete()
        self.user.refresh_from_db()
        self.assertIsNone(self.user.avatar)  # SET_NULL

    # --- Herança AbstractUser ---

    def test_usuario_pode_autenticar(self):
        from django.contrib.auth import authenticate
        user = authenticate(username="joao", password="senha123")
        self.assertIsNotNone(user)

    def test_senha_incorreta_nao_autentica(self):
        from django.contrib.auth import authenticate
        user = authenticate(username="joao", password="errada")
        self.assertIsNone(user)

    def test_username_unico(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="joao", password="outrasenha")