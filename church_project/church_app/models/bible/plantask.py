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

    class Meta:
        # Ordena automaticamente por semana e depois por dia
        ordering = ['week_number', 'day_number']
        # Garante que não existam dois "Dia 1" na mesma "Semana 1" para o mesmo plano
        #unique_together = ('plan', 'week_number', 'day_number')

    def __str__(self):
        return f"{self.plan.title} - S{self.week_number} D{self.day_number}"

    @property
    def chapter_summary(self):
        """Retorna um texto amigável como 'Gênesis 1-3' ou 'João 3, 4'"""
        chapters = self.chapters.all().order_by('number')
        if not chapters:
            return "Nenhum capítulo definido"
        
        book_name = chapters[0].book.name
        nums = [str(c.number) for c in chapters]
        
        if len(nums) > 1:
            return f"{book_name} {nums[0]}-{nums[-1]}"
        return f"{book_name} {nums[0]}"