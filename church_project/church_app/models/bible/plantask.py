from django.db import models
from church_app.models.bible.book import Chapter  # Importando seu modelo de capítulos

class ReadingPlan(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
