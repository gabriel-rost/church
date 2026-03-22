from django.db import models
from church_app.models.bible.book import Chapter  # Importando seu modelo de capítulos
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ReadingPlan(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #draft = models.BooleanField(default=True)  # Indica se o plano está em rascunho ou publicado
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)

    def publish(self):
            if not self.is_published:
                self.is_published = True
                self.published_at = timezone.now()
                self.save()
                
                # Lógica extra aqui:
                # 1. Criar Postagem no Feed
                # 2. Chamar função de Notificação

    def get_absolute_url(self):
        # Substitua 'plan_detail' pelo nome da sua rota no urls.py
        # Se sua rota for path('plans/<int:plan_id>/', ...)
        return reverse('plan_detail', kwargs={'plan_id': self.id})

    def __str__(self):
        return self.title

class PlanTask(models.Model):
    plan = models.ForeignKey(
        ReadingPlan, 
        related_name='tasks', 
        on_delete=models.CASCADE
    )
    week_number = models.PositiveIntegerField()
    day_number = models.PositiveIntegerField()
    
    # ManyToMany permite que um dia tenha vários capítulos (ex: Mateus 1 e 2)
    chapters = models.ManyToManyField(
        Chapter, 
        related_name='plan_tasks'
    )

    # Campos opcionais para versículos específicos
    # Se start_verse existir, chapters deve ter apenas um capítulo
    start_verse = models.PositiveIntegerField(null=True, blank=True)
    end_verse = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        # Ordena automaticamente por semana e depois por dia
        ordering = ['week_number', 'day_number']
        # Garante que não existam dois "Dia 1" na mesma "Semana 1" para o mesmo plano
        #unique_together = ('plan', 'week_number', 'day_number')

    def __str__(self):
        return f"{self.plan.title} - S{self.week_number} D{self.day_number}"

    @property
    def chapter_summary(self):
        chapters = self.chapters.all().order_by('number')
        if not chapters:
            return "Nenhum capítulo definido"

        book = chapters[0].book.name

        if self.start_verse:
            return f"{book} {chapters[0].number}:{self.start_verse}-{self.end_verse}"

        nums = [c.number for c in chapters]
        if len(nums) > 1:
            return f"{book} {nums[0]}-{nums[-1]}"
        return f"{book} {nums[0]}"


class UserPlanProgress(models.Model):
    '''
    - saber se o usuário iniciou o plano
    - saber quando terminou
    - evitar iniciar duas vezes
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(ReadingPlan, on_delete=models.CASCADE)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "plan")

    def __str__(self):
        return f"{self.user} - {self.plan}"

class UserTaskProgress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(PlanTask, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "task")

    def complete(self):
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.user} - {self.task}"
    
def get_progress_percentage(user, plan):
    '''
    Cálculo do progresso do plano
    '''
    total = plan.tasks.count()

    completed = UserTaskProgress.objects.filter(
        user=user,
        task__plan=plan,
        completed=True
    ).count()

    if total == 0:
        return 0

    return int((completed / total) * 100)