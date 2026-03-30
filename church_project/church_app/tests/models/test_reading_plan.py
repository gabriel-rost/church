# # tests/models/test_reading_plan.py
# from django.test import TestCase
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# from church_app.models.bible.plantask import (
#     ReadingPlan, PlanTask, UserPlanProgress, UserTaskProgress, get_progress_percentage
# )
# from church_app.models.bible.book import Book, Chapter

# User = get_user_model()


# class ReadingPlanModelTest(TestCase):

#     def setUp(self):
#         self.plan = ReadingPlan.objects.create(
#             title="Plano Anual",
#             description="Leitura completa da Bíblia",
#             author_id = 1
#         )

#     def test_str(self):
#         self.assertEqual(str(self.plan), "Plano Anual")

#     def test_draft_default_true(self):
#         self.assertTrue(self.plan.draft)

#     def test_publicar_plano(self):
#         self.plan.draft = False
#         self.plan.save()
#         self.plan.refresh_from_db()
#         self.assertFalse(self.plan.draft)

#     def test_description_pode_ser_vazia(self):
#         plan = ReadingPlan.objects.create(title="Sem descrição")
#         self.assertEqual(plan.description, "")

#     def test_created_at_preenchido_automaticamente(self):
#         self.assertIsNotNone(self.plan.created_at)


# class PlanTaskModelTest(TestCase):

#     def setUp(self):
#         self.plan = ReadingPlan.objects.create(title="Plano Teste")
#         self.book = Book.objects.create(name="Mateus", order=40)  # removido testament
#         self.chapter1 = Chapter.objects.create(book=self.book, number=1)
#         self.chapter2 = Chapter.objects.create(book=self.book, number=2)
#         self.task = PlanTask.objects.create(
#             plan=self.plan,
#             week_number=1,
#             day_number=1,
#         )
#         self.task.chapters.add(self.chapter1, self.chapter2)

#     def test_str(self):
#         self.assertEqual(str(self.task), "Plano Teste - S1 D1")

#     def test_ordering(self):
#         task2 = PlanTask.objects.create(plan=self.plan, week_number=1, day_number=2)
#         task3 = PlanTask.objects.create(plan=self.plan, week_number=2, day_number=1)
#         tasks = list(PlanTask.objects.filter(plan=self.plan))
#         self.assertEqual(tasks[0], self.task)
#         self.assertEqual(tasks[1], task2)
#         self.assertEqual(tasks[2], task3)

#     def test_chapter_summary_multiplos_capitulos(self):
#         self.assertEqual(self.task.chapter_summary, "Mateus 1-2")

#     def test_chapter_summary_capitulo_unico(self):
#         task = PlanTask.objects.create(plan=self.plan, week_number=1, day_number=3)
#         task.chapters.add(self.chapter1)
#         self.assertEqual(task.chapter_summary, "Mateus 1")

#     def test_chapter_summary_com_versiculos(self):
#         task = PlanTask.objects.create(
#             plan=self.plan,
#             week_number=1,
#             day_number=4,
#             start_verse=1,
#             end_verse=12,
#         )
#         task.chapters.add(self.chapter1)
#         self.assertEqual(task.chapter_summary, "Mateus 1:1-12")

#     def test_chapter_summary_sem_capitulos(self):
#         task = PlanTask.objects.create(plan=self.plan, week_number=2, day_number=2)
#         self.assertEqual(task.chapter_summary, "Nenhum capítulo definido")

#     def test_deletar_plano_deleta_tasks(self):
#         plan_id = self.plan.id
#         self.plan.delete()
#         self.assertFalse(PlanTask.objects.filter(plan_id=plan_id).exists())

#     def test_start_end_verse_opcionais(self):
#         self.assertIsNone(self.task.start_verse)
#         self.assertIsNone(self.task.end_verse)


# class UserPlanProgressTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="gabriel", password="123")
#         self.plan = ReadingPlan.objects.create(title="Plano Anual")
#         self.progress = UserPlanProgress.objects.create(user=self.user, plan=self.plan)

#     def test_str(self):
#         self.assertIn("gabriel", str(self.progress))
#         self.assertIn("Plano Anual", str(self.progress))

#     def test_started_at_preenchido(self):
#         self.assertIsNotNone(self.progress.started_at)

#     def test_completed_at_nulo_por_padrao(self):
#         self.assertIsNone(self.progress.completed_at)

#     def test_unique_together_user_plan(self):
#         from django.db import IntegrityError
#         with self.assertRaises(IntegrityError):
#             UserPlanProgress.objects.create(user=self.user, plan=self.plan)

#     def test_deletar_usuario_deleta_progresso(self):
#         user_id = self.user.id
#         self.user.delete()
#         self.assertFalse(UserPlanProgress.objects.filter(user_id=user_id).exists())


# class UserTaskProgressTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="gabriel", password="123")
#         self.plan = ReadingPlan.objects.create(title="Plano")
#         self.task = PlanTask.objects.create(plan=self.plan, week_number=1, day_number=1)
#         self.progress = UserTaskProgress.objects.create(user=self.user, task=self.task)

#     def test_str(self):
#         self.assertIn("gabriel", str(self.progress))

#     def test_completed_false_por_padrao(self):
#         self.assertFalse(self.progress.completed)

#     def test_completed_at_nulo_por_padrao(self):
#         self.assertIsNone(self.progress.completed_at)

#     def test_complete_marca_como_concluido(self):
#         self.progress.complete()
#         self.assertTrue(self.progress.completed)
#         self.assertIsNotNone(self.progress.completed_at)

#     def test_complete_nao_sobrescreve_se_ja_completo(self):
#         self.progress.complete()
#         primeiro_completed_at = self.progress.completed_at
#         self.progress.complete()  # segunda chamada não deve alterar
#         self.assertEqual(self.progress.completed_at, primeiro_completed_at)

#     def test_unique_together_user_task(self):
#         from django.db import IntegrityError
#         with self.assertRaises(IntegrityError):
#             UserTaskProgress.objects.create(user=self.user, task=self.task)

#     def test_completed_at_aproximadamente_agora(self):
#         before = timezone.now()
#         self.progress.complete()
#         after = timezone.now()
#         self.assertGreaterEqual(self.progress.completed_at, before)
#         self.assertLessEqual(self.progress.completed_at, after)


# class GetProgressPercentageTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="gabriel", password="123")
#         self.plan = ReadingPlan.objects.create(title="Plano")
#         self.task1 = PlanTask.objects.create(plan=self.plan, week_number=1, day_number=1)
#         self.task2 = PlanTask.objects.create(plan=self.plan, week_number=1, day_number=2)
#         self.task3 = PlanTask.objects.create(plan=self.plan, week_number=1, day_number=3)

#     def test_zero_percent_sem_progresso(self):
#         self.assertEqual(get_progress_percentage(self.user, self.plan), 0)

#     def test_zero_percent_plano_sem_tasks(self):
#         plan_vazio = ReadingPlan.objects.create(title="Vazio")
#         self.assertEqual(get_progress_percentage(self.user, plan_vazio), 0)

#     def test_33_percent(self):
#         UserTaskProgress.objects.create(user=self.user, task=self.task1, completed=True)
#         self.assertEqual(get_progress_percentage(self.user, self.plan), 33)

#     def test_100_percent(self):
#         for task in [self.task1, self.task2, self.task3]:
#             UserTaskProgress.objects.create(user=self.user, task=task, completed=True)
#         self.assertEqual(get_progress_percentage(self.user, self.plan), 100)

#     def test_nao_conta_tasks_incompletas(self):
#         UserTaskProgress.objects.create(user=self.user, task=self.task1, completed=True)
#         UserTaskProgress.objects.create(user=self.user, task=self.task2, completed=False)
#         self.assertEqual(get_progress_percentage(self.user, self.plan), 33)

#     def test_progresso_isolado_por_usuario(self):
#         outro_user = User.objects.create_user(username="maria", password="123")
#         UserTaskProgress.objects.create(user=outro_user, task=self.task1, completed=True)
#         self.assertEqual(get_progress_percentage(self.user, self.plan), 0)